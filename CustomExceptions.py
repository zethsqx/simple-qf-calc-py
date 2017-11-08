
class StockNotFoundException(Exception):
    def __init__(self,message, errors):
        super()