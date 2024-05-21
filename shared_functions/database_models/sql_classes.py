""" This module is to declarative the SQL classes for the database """

from sqlalchemy import Column, Integer, String, DateTime, Text, TIMESTAMP, Boolean, Float 
from sqlalchemy.orm import declarative_base

BASE = declarative_base()


class Happiness(BASE):
    """ This class is to create the table for the happiness data """

    __tablename__ = "happiness"

    id = Column(Integer, primary_key=True)
    country = Column(String(60), nullable=True, default=None)
    region = Column(String(60), nullable=True, default=None)
    happinnes_rank = Column(Integer(), nullable=True, default=None)
    happinnes_score = Column(Float(), nullable=True, default=None)
    happinnes_predicted = Column(Float(), nullable=True, default=None)
    economy_per_capita = Column(Float(), nullable=True, default=None)
    family = Column(Float(), nullable=True, default=None)
    life_expectancy = Column(Float(), nullable=True, default=None)
    freedom = Column(Float(), nullable=True, default=None)
    government_corruption = Column(Float(), nullable=True, default=None)
    generosity = Column(Float(), nullable=True, default=None)
    dystopia_residual = Column(Float(), nullable=True, default=None)
    standard_error = Column(Float(), nullable=True, default=None) #!
    lower_confidence_interval = Column(Float(), nullable=True, default=None) #!
    upper_confidence_interval = Column(Float(), nullable=True, default=None) #!
    whisker_low = Column(Float(), nullable=True, default=None) #!
    whisker_high = Column(Float(), nullable=True, default=None) #!

    def __str__(self) -> str:
        return f"{self.happinnes_rank} vs. {self.happinnes_predicted}"
