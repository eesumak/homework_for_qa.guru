from pathlib import Path

import json
import pytest


@pytest.fixture
def auth(request):
    # Переменная request.param получает значение из декоратора теста
    user_role = request.param
    headers = {"Authorization": f"Bearer token {user_role}"}
    yield headers


directory = Path("my_dir")
directory.mkdir(exist_ok=True)
(directory / "1.txt").write_text("Hello World")
(directory / "2.json").write_text(json.dumps({"Hello": "World"}))
(directory / "3.csv").write_text("123")

def pytest_generate_tests(metafunc):
    if "file_path" in metafunc.fixturenames:
        if directory.exists():
            # Составляем список только нужных файлов
            files = files = sorted([*directory.glob("*.txt"), *directory.glob("*.json")])
        else:
            files =[]

        # Генерируем понятные идентификаторы для отчетов
        ids = [f"Файл {f.name}" for f in files]
        metafunc.parametrize("file_path", files, ids=ids)

