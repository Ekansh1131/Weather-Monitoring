from sqlalchemy import create_engine, Column, Integer, Float, String, Date, UniqueConstraint, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from .config import DATABASE_URL

Base = declarative_base()

class DailyWeatherSummary(Base):
    __tablename__ = 'daily_weather_summary'

    id = Column(Integer, primary_key=True)
    city = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    avg_temp = Column(Float)
    max_temp = Column(Float)
    min_temp = Column(Float)
    dominant_weather = Column(String(50))
    avg_humidity = Column(Float)
    avg_pressure = Column(Float)
    avg_wind_speed = Column(Float)
    max_wind_speed = Column(Float)
    wind_direction = Column(String(10))
    total_rain = Column(Float, default=0.0)
    total_snow = Column(Float, default=0.0)
    avg_clouds = Column(Float)
    avg_visibility = Column(Float)
    description = Column(Text)
    last_updated = Column(Float, default=lambda: datetime.now().timestamp())

    __table_args__ = (UniqueConstraint('city', 'date', name='_city_date_uc'),)

class DatabaseManager:
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(self.engine)

    def save_daily_summary(self, city, summary):
        """Save or update daily summary for a city"""
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=self.engine)
        session = Session()

        try:
            # Check if record exists
            existing = session.query(DailyWeatherSummary).filter_by(
                city=city,
                date=summary['date']
            ).first()

            current_time = datetime.now().timestamp()

            if existing:
                # Update existing record
                for key, value in summary.items():
                    if hasattr(existing, key) and key != 'date':
                        setattr(existing, key, value)
                existing.last_updated = current_time
            else:
                # Create new record
                new_summary = DailyWeatherSummary(
                    city=city,
                    date=summary['date'],
                    avg_temp=summary.get('avg_temp'),
                    max_temp=summary.get('max_temp'),
                    min_temp=summary.get('min_temp'),
                    dominant_weather=summary.get('dominant_weather'),
                    avg_humidity=summary.get('avg_humidity'),
                    avg_pressure=summary.get('avg_pressure'),
                    avg_wind_speed=summary.get('avg_wind_speed'),
                    max_wind_speed=summary.get('max_wind_speed'),
                    wind_direction=summary.get('dominant_wind_direction'),
                    total_rain=summary.get('total_rain', 0.0),
                    total_snow=summary.get('total_snow', 0.0),
                    avg_clouds=summary.get('avg_clouds'),
                    avg_visibility=summary.get('avg_visibility'),
                    description=summary.get('detailed_description'),
                    last_updated=current_time
                )
                session.add(new_summary)

            session.commit()
            print(f"Successfully saved/updated summary for {city} on {summary['date']}")
            return True

        except Exception as e:
            session.rollback()
            print(f"Error saving summary for {city}: {str(e)}")
            raise
        finally:
            session.close()

    def get_daily_summaries(self, start_date, end_date):
        """Get daily summaries for all cities between dates"""
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=self.engine)
        session = Session()

        try:
            summaries = session.query(DailyWeatherSummary).filter(
                DailyWeatherSummary.date.between(start_date, end_date)
            ).order_by(
                DailyWeatherSummary.date,
                DailyWeatherSummary.city
            ).all()
            return summaries
        finally:
            session.close()

    def get_city_summaries(self, city, start_date, end_date):
        """Get daily summaries for a specific city"""
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=self.engine)
        session = Session()

        try:
            summaries = session.query(DailyWeatherSummary).filter(
                DailyWeatherSummary.city == city,
                DailyWeatherSummary.date.between(start_date, end_date)
            ).order_by(DailyWeatherSummary.date).all()
            return summaries
        finally:
            session.close()

    def get_latest_summary(self, city):
        """Get the most recent summary for a city"""
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=self.engine)
        session = Session()

        try:
            summary = session.query(DailyWeatherSummary).filter(
                DailyWeatherSummary.city == city
            ).order_by(
                DailyWeatherSummary.date.desc()
            ).first()
            return summary
        finally:
            session.close()