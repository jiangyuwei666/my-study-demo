import unittest
from UnitTest_my_class import Student

class TestStudent(unittest.TestCase):
    def test_90_to_100(self):
        s1 = Student("Jiang", 90)
        s2 = Student("Tom", 100)
        self.assertEqual(s1.get_grade(), "A")
        self.assertEqual(s2.get_grade(), "A")

    def test_60_to_90(self):
        s1 = Student('Jiang', 60)
        s2 = Student('Tom', 89)
        self.assertEqual(s1.get_grade(), 'B')
        self.assertEqual(s2.get_grade(), 'B')

    def test_below_60(self):
        s1 = Student('Jiang', 0)
        s2 = Student('Tom', 59)
        self.assertEqual(s1.get_grade(), 'C')
        self.assertEqual(s2.get_grade(), 'C')

    def test_invalid(self):
        s1 = Student("Jiang", (-1))
        s2 = Student("Tom", "101")
        with self.assertRaises(ValueError):
            s1.get_grade()
        with self.assertRaises(TypeError):
            s2.get_grade()

if __name__ == '__main__':
    unittest.main()
