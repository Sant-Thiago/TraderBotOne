from enum import Enum
from typing import Dict
from pandas.core.series import Series

class _Trend(Enum):
    UP = "Upward trend"
    SIDEWAYS = "Sydeways trend"
    DOWN = "Downward trend"

class _Market(Enum):
    BULL = "Bull market"
    BEAR = "Bear market"

class _Type():
    trend = _Trend
    market = _Market

class Analysis:

    def __init__(self):
        self.strength: int = 0
        self.value: Series = None
        self.trend: _Trend = None
        self.market: _Market = None
        self.type: _Type = _Type
        self.id: str = None
        self.top: Series = None
        self.bottom: Series = None

    
    def more(self, points: int) -> int:
        """
            Força máxima é 3.
            Adiciona pontos de força à análise.
        """
        self.strength += points
        return self.strength
    
    def minus(self, points: int) -> int:
        """
            Força mínima é -3.
            Remove pontos de força da análise.
        """
        if self.strength == -3:
            return self.strength
        
        self.strength -= points
        return self.strength
    
    def __repr__(self):
        return f"Analysis(id={self.id}, trend={self.trend}, strength={self.strength}, top={self.top}, bottom={self.bottom} )"
