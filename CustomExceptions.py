
class StockNotFoundException(Exception):
    '''Custom Exception when stock symbol not found'''
    def __init__(self,message, errors):
        super().__init__(message)
        self.e = errors