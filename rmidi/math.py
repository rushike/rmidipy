import math
class  sequences:
    @classmethod
    def fibonacci(cls, nth):
        return int(1 / math.sqrt(5) * (math.pow((1 + math.sqrt(5)) / 2, nth + 1) - math.pow((1 - math.sqrt(5)) / 2, nth + 1)))