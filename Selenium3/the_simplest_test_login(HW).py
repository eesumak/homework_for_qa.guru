import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestLogin:
    URL = "https://qa-guru.github.io/one-page-form/login.html"
    LOGIN_INPUT     = (By.ID, "login-input")
    PASSWORD_INPUT  = (By.ID, "password-input")
    SUBMIT_BUTTON   = (By.ID, "submit-button")
    STATUS_MESSAGE  = (By.ID, "error-message")

    @pytest.fixture(scope="function", autouse=True)
    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.URL)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 5)
        yield
        self.driver.quit()

    def input_login(self, login):
        self.driver.find_element(*self.LOGIN_INPUT).send_keys(login)

    def input_password(self, password):
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)

    def submit_login(self):
        self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON)).click()

    def error_message_text(self):
        self.wait.until(EC.visibility_of_element_located(self.STATUS_MESSAGE))
        return self.driver.find_element(*self.STATUS_MESSAGE).text

    @pytest.mark.parametrize("login, password, expected",[
        ("qaguru@gmail.com", "qagurupassword", "Wrong login or password")])
    def test_invalid_login(self, login, password, expected):
        self.input_login(login)
        self.input_password(password)
        self.submit_login()
        assert expected in self.error_message_text()
        print("Тест пройден успешно! Ввели неверные данные и не смогли войти в систему.")
