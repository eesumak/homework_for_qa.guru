import pytest
from dataclasses import dataclass

# Тестируем функцию валидации email
def is_valid_email(email: str) -> bool:
    return "@" in email and "." in email.split("@")[-1]

# 1. Базовое использование @pytest.mark.parametrize
# Параметризация на уровне теста позволяет запустить одну и ту же тестовую функцию множество раз с разными входными данными.
# Это избавляет от антипаттерна «тесты в цикле for» (когда при первом падении внутри цикла весь остальной цикл прерывается).

@pytest.mark.parametrize(
    "email, expected_result",
    [
        ("user@test.com", True),
        ("invalid-email", False),
        ("user@com", False),
        ("admin@company.ru", True),
    ]
)
def test_email_validation(email, expected_result):
    assert is_valid_email(email) == expected_result

# Множественное использование (Комбинаторная параметризация / Декартово произведение)
# Если повесить на один тест несколько декораторов @pytest.mark.parametrize, pytest автоматически перемножит их между собой.
# Это незаменимо для тестирования матриц доступов, комбинаций браузеров, операционных систем или языков.
@pytest.mark.parametrize("browser", ["Chrome", "Firefox", "Safari"])
@pytest.mark.parametrize("role", ["admin", "user"])
def test_matrix_access(browser, role):
    # Этот тест запустится 6 раз (3 браузера * 2 роли)
    print(f"\n[Тест] Проверка интерфейса: {browser} для роли {role}")
    assert True

# 3. Идентификаторы (IDs) и метки в параметризации для читаемости отчетов
# Когда тестов становится много, в отчетах (особенно в CI/CD пайплайнах) сложно понять, какой именно набор данных упал,
# если они отображаются как test_user[user0] или test_user[alex-active]. pytest позволяет кастомизировать эти отчеты.
# 3.1 example:
@pytest.mark.parametrize(
    "status_code, expected",
    [(200, "OK"), (404, "Not Found"), (500, "Internal Error")],
    ids=["success_case", "not_found_case", "server_error_case"] # Четкие имена для отчета
)
def test_api_status(status_code, expected):
    assert True

# 3.2 example:
@dataclass
class User:
    name: str
    age: int

# Передача функции генератора айдишников (Идеально для сложных объектов)
# Если у вас десятки параметров, писать вручную список ids неудобно. Передайте функцию в ids, и она автоматически сгенерирует красивые строки.
def generate_id(val):
    # Эта функция вызывается для каждого элемента в параметрах
    if isinstance(val, User):
        # Добавлена глобальная настройка для отключения экранирования не-ASCII символов
        return f"User({val.name}_age={val.age})"
    return str(val)

@pytest.mark.parametrize(
    "user",
    [User("Иван", 20), User("Ольга", 35)],
    ids=generate_id # Применяем генератор имен
)
def test_user_age_limits(user):
    assert user.age >= 18

# 3.3 example:
# Использование встроенных меток внутри параметров (pytest.param) - критически важно для отчетов.
# С помощью pytest.param можно не только вешать skip или xfail, но и задавать локальный id для конкретной строчки данных.
@pytest.mark.parametrize(
    "x, y",
    [
        (1, 2),
        (5, 5),
        # Задаем кастомный ID и одновременно вешаем маркер xfail на одну строку
        pytest.param(0, 0, marks=pytest.mark.xfail(reason="Деление на ноль"), id="zero_division_case")
    ]
)
def test_math_logic(x, y):
    if x == 0 and y == 0:
        assert False
    assert x + y >= 2


# pytest -v -s --log-cli-level=DEBUG --tb=short