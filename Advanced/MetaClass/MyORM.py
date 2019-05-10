# 需求
import numbers
class CharFiled:
    def __init__(self,db_column,max_length):
        pass
    def __get__(self, instance, owner):
        pass


class IntFiled:
    def __init__(self,db_column,min_value=None,max_value=None):
        self._value = None
        self.min_value = min_value
        self.max_value = max_value
        if not isinstance(min_value, numbers.Integral):
            raise ValueError('min_value must be int')
        if not isinstance(max_value, numbers.Integral):
            raise ValueError('max_value must be int')
        if min_value > max_value:
            raise ValueError('max_value must bigger than min_value')
    def __get__(self, instance, owner):
        return self._value
    def __set__(self, instance, value):
        if not isinstance(self._value):
            pass


class User:
    name = CharFiled(db_column="", max_length=10)
    age = IntFiled(db_column="", min_value=0,max_value=100)
    class Meta:
        db_table=""

if __name__ == "__main__":