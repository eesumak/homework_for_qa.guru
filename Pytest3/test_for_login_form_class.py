import sys
import allure
import pytest
import logging
from page_login import LoginFormPage

@allure.feature('Успешный вход')
@allure.story('Вывод приветствия')
@allure.title('Тест логина с валидными данными')
@pytest.mark.pozitiv
@pytest.mark.parametrize(
    "login, password, expected", [("user1", "password1", "Welcome, user1!")]
)
def test_valid_data_login(driver, login, password, expected):
    login_form = LoginFormPage(driver)
    login_form.open()
    login_form.field_login(login)
    login_form.field_password(password)
    login_form.login_button()
    assert login_form.welcome_message_text() == expected

@allure.feature('Неуспешный вход')
@allure.story('Неверные данные')
@allure.description('Проврка текста ошибки для разных комбинаций невалидных данных')
@pytest.mark.negativ
@pytest.mark.parametrize(
    "login, password, expected",
    [
        ("user2", "password1", "Wrong login or password"),
        ("user1", "password2", "Wrong login or password"),
        ("login1", "", "Password is required (minimum 6 characters)"),
        ("", "password1", "Login is required (minimum 3 characters)"),
    ],
)
def test_invalid_login(driver, login, password, expected):
    login_form = LoginFormPage(driver)
    login_form.open()
    login_form.field_login(login)
    login_form.field_password(password)
    login_form.login_button()
    assert login_form.error_message_text() == expected

@allure.feature('Неуспешный вход')
@allure.story('Пустой ввод')
@pytest.mark.negativ
def test_empty_fields(driver):
    login_form = LoginFormPage(driver)
    login_form.open()
    login_form.login_button()
    assert login_form.error_message_text() == (
        "Login and password are required" " (minimum 3 and 6 characters)"
    )

@allure.feature('Успешный выход')
@pytest.mark.parametrize(
    "login, password, expected", [("user1", "password1", "Welcome, user1!")]
)
def test_logout(driver, login, password, expected):
    login_form = LoginFormPage(driver)
    login_form.open()
    login_form.field_login(login)
    login_form.field_password(password)
    login_form.login_button()
    login_form.logout_button()
    with allure.step('Проверка заголовка текущей формы'):
        assert login_form.driver.find_element(*login_form.LOGIN_FORM_TITLE).text == "Login Form"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def test_allure_logs_example():
    # 1. Запись в стандартный лог (логгирование)
    logger.info("Это сообщение уровня INFO через стандартный модуль logging")
    logger.warning("Это предупреждение (WARNING) для отчета")

    # 2. Вывод в stdout (функция print)
    print("Текст, выведенный в стандартный поток вывода stdout")

    # 3. Вывод в stderr (ошибки в консоль)
    print("Текст, отправленный в поток ошибок stderr", file=sys.stderr)

    # 4. Ручное добавление вложений через Allure (опционально)
    allure.attach("Дополнительные данные", name="Custom Text Attachment", attachment_type=allure.attachment_type.TEXT)