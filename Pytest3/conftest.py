import os
import shutil
import subprocess
import pytest
from selenium import webdriver


@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

# Автоматический запуск генерации отчета с сохранением истории
def pytest_sessionfinish(session, exitstatus):
    results_dir = "Pytest3/allure-results"
    report_dir = "Pytest3/allure-report"
    old_history = os.path.join(report_dir, "history")
    new_history = os.path.join(results_dir, "history")

    # 1. Копируем историю из предыдущего отчёта (если он уже существует)
    if os.path.exists(old_history):
        shutil.copytree(old_history, new_history, dirs_exist_ok=True)

    # 2. Генерируем новый HTML-отчёт с учётом истории
    subprocess.run(
        ["allure", "generate", results_dir, "-o", report_dir, "--clean"],
        shell=True,
        check=False
    )

    # 3. Автоматически открываем отчёт в браузере (в фоновом режиме)
    subprocess.Popen(
        ["allure", "open", report_dir],
        shell=True
    )