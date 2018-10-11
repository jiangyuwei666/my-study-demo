class Student(object):

    def __init__(self, name, score):
        self.name = name
        self.score = score

    def get_grade(self):
        if isinstance(self.score, int):
            if self.score > 100 or self.score < 0:
                raise ValueError
            elif self.score < 60:
                return "C"
            elif self.score < 90:
                return "B"
            elif self.score <= 100:
                return "A"
        else:
            raise TypeError

