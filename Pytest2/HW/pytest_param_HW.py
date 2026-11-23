import json
import pytest


# Написать тест для "API", который через indirect фикстуру меняет заголовки авторизации (User, Admin, Guest).
@pytest.mark.parametrize("auth", ["User", "Admin", "Guest"], indirect=True)
def test_auth(auth):
    print(auth)
    assert "User" or "Admin" or "Guest" in auth["Authorization"] and "Bearer" in auth["Authorization"]


# Написать динамическую параметризацию, которая сканирует указанную папку и генерирует тесты под каждый найденный там .txt или .json файл.
def test_scan_dir(file_path):
    print(f"Обработка {file_path}")

    # Проверяем, что файл ненужного формата не попал в выборку
    assert file_path.suffix is not "csv"

    if file_path.suffix == ".txt":
        assert len(file_path.read_text()) > 0
    else:
        assert isinstance(json.loads(file_path.read_text()),dict)



# Сделать комбинаторный тест формы регистрации (Имя * Фамилия * Возраст) с красивыми кастомными ids.
names = ["Ваня", "Петя", "Маша"]
surnames = ["Петров", "Иванов", "Медведева"]
ages = [20, 7, 65, 33, 14, 100]


@pytest.mark.parametrize("name", names, ids= [f"Имя = {name}" for name in names])
@pytest.mark.parametrize("surname", surnames, ids= [f"Фамилия = {surname}" for surname in surnames])
@pytest.mark.parametrize("age", ages, ids= [f"Возраст = {ages}" for ages in ages])
def test_registration(name, surname, age):
    print(f"Регистрация: {name} {surname} {age} лет")
    assert name in names and surname in surnames and age in ages
