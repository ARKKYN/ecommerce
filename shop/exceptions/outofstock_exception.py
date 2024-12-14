

class OutOfStockException(Exception):
  def __init__(self, message="Out of stock"):
    self.message = message
    super().__init__(self.message)


