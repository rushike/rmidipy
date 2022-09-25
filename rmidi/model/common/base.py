class BaseModel:
    def __init__(self) -> None:
        pass

    def validate(self, left, right, ret = True):
        if left == right and ret : return left
        return left
        raise AttributeError(f"Passed invalid attribute, expected : {right} got : {left}")

    def validatein(self, left, rightlist, ret = True):
        if left in rightlist and ret : return left
        return left
        raise AttributeError(f"Passed invalid attribute, expected in {rightlist} got : {left}")

    def __repr__(self) -> str:
        return str(self.__dict__)
    

class BaseByte:
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return str(self.__dict__)

