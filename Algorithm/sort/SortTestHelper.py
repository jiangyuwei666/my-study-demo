import numpy as np


class Helper:
    @classmethod
    def get_int_list(cls, n):
        return list(np.random.randint(low=-n, high=n, size=n))