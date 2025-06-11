"""
Необходимо реализовать декоратор @strict
Декоратор проверяет соответствие типов переданных в вызов функции аргументов типам аргументов, объявленным в прототипе
функции. (подсказка: аннотации типов аргументов можно получить из атрибута объекта функции func.__annotations__ или
с помощью модуля inspect). При несоответствии типов бросать исключение TypeError
Гарантируется, что параметры в декорируемых функциях будут следующих типов: bool, int, float, str
Гарантируется, что в декорируемых функциях не будет значений параметров, заданных по умолчанию.

Задачу реализовать, используя встроенные средства языка. К задаче должны быть написаны тесты.
"""
import unittest


def strict(func):
    """
    Декоратор для проверки соответствия типов переданных в вызов функции аргументов типам аргументов, объявленным
    в прототипе функции. В случае несовпадения типов вызывает исключение TypeError
    """
    def wrapper(*args):
        # Получаем список объявленных в прототипе функции типов аргументов, сохраняем в список, исключаем тип возвращаемого
        # функцией значения
        types_list = [value for value in func.__annotations__.values()][:-1]
        # Попарно сравниваем типы аргументов, в случае несовпадения вызываем исключение TypeError
        for item in range(len(args)):
            if type(args[item]) != types_list[item]:
                raise TypeError
        return func(*args)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


class TestFunction(unittest.TestCase):
    """ Тестирование декоратора strict """
    def test_0(self):
        self.assertEqual(sum_two(1, 2), 3)

    def test_1(self):
        with self.assertRaises(TypeError):
            sum_two(1, 2.4)

    def test_2(self):
        with self.assertRaises(TypeError):
            sum_two(1.0, 2)

    def test_3(self):
        with self.assertRaises(TypeError):
            sum_two(1.0, 2.9)

    def test_4(self):
        with self.assertRaises(TypeError):
            sum_two(3, True)

    def test_5(self):
        with self.assertRaises(TypeError):
            sum_two(False, 2)

    def test_6(self):
        with self.assertRaises(TypeError):
            sum_two(False, False)

    def test_7(self):
        with self.assertRaises(TypeError):
            sum_two(5, '2')

    def test_8(self):
        with self.assertRaises(TypeError):
            sum_two(1, 'word')

    def test_9(self):
        with self.assertRaises(TypeError):
            sum_two('a', 'b')


if __name__ == '__main__':
    unittest.main()