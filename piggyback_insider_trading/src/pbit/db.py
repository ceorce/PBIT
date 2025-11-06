from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, Numeric, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import settings

engine = create_engine(settings.DB_URL, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

class Filing(Base):
    __tablename__ = "filings"
    id = Column(Integer, primary_key=True)
    ticker = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    insider_cik = Column(String, nullable=False)
    insider_name = Column(String, nullable=False)
    insider_title = Column(String, nullable=False)
    transaction_date = Column(Date, nullable=False)
    is_acquisition = Column(Boolean, nullable=False)
    transaction_code = Column(String, nullable=False)
    shares = Column(Integer, nullable=False)
    price_per_share = Column(Numeric(18, 4), nullable=False)
    total_value = Column(Numeric(18, 2), nullable=False)
    is_open_market = Column(Boolean, nullable=False)
    is_10b51 = Column(Boolean, nullable=False)
    filing_url = Column(Text, nullable=False)

def init_db():
    Base.metadata.create_all(engine)
