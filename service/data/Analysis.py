class Analysis:
    def __init__(self):
        self.status: str = None
        self.value: float = None
        self.trend: str = None

    def get_status(self):
        return self.status
    
    def set_status(self, status):
        self.status = status
    
    def get_value(self):
        return self.value
    
    def set_value(self, value):
        self.value = value
    
    def get_trend(self):
        return self.trend
    
    def set_trend(self, trend):
        self.trend = trend
