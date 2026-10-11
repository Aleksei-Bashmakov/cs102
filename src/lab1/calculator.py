"""Простой консольный калькулятор: + - * / **."""


def addiction(first: float, second: float) -> float:
    """Возвращает сумму двух чисел."""
    return first + second

def subtract(first: float, second: float) -> float:
    """Возвращает разность двух чисел."""
    return first - second


def multiply(first: float, second: float) -> float:
    """Возвращает произведение двух чисел."""
    return first * second


def divide(first: float, second: float) -> float | str:
    """Возвращает частное или сообщение об ошибке при делении на ноль."""
    if second == 0:
        return "Ошибка: на ноль делить нельзя"
    return first / second


def power(first: float, second: float) -> float | str:
    """Возводит первое число в степень второго или возвращает сообщение об ошибке."""
    try:
        result = first**second
    except ZeroDivisionError:
        return "Ошибка: ноль нельзя возводить в отрицательную степень!"
    except OverflowError:
        return "Ошибка: слишком большое число!"
    if isinstance(result, complex):
        return "Ошибка: результат не является вещественным числом!"
    return result


def calculator() -> None:
    """Запускает интерактивный калькулятор в консоли."""
    print('Калькулятор с оперциями "+" "-" "*" "/" "**" ')
    print('Для выхода нажмите "q" \n')
    while True:
        operation = input("Выберите операцию (+, -, *, /,**) или 'q' для выхода: ")
        if operation == "q":
            print("До свидания!")
            break
        if operation not in ["+", "-", "*", "/", "**"]:
            print("Неизвестная операция, попробуйте снова.\n")
            continue
        try:
            a = float(input("Введите первое число: "))
            b = float(input("Введите второе число: "))
        except ValueError:
            print("Нужно вводить числа!\n")
            continue
        if operation == "+":
            result = addiction(a, b)
        elif operation == "-":
            result = subtract(a, b)
        elif operation == "*":
            result = multiply(a, b)
        elif operation == "/":
            result = divide(a, b)
        elif operation == "**":
            result = power(a, b)
        print(f"Результат: {result}\n")


if __name__ == "__main__":
    calculator()