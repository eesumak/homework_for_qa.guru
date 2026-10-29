import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class TestLoginForm:
    URL = "https://qa-guru.github.io/one-page-form/login.html"
    LOGIN_FIELD = (By.ID, "login-input")
    PASSWORD_FIELD = (By.ID, "password-input")
    LOGIN_BUTTON = (By.ID, "submit-button")
    LOGOUT_BUTTON = (By.ID, "logout-button")
    WELCOME_MESSAGE = (By.ID, "welcome-message")
    ERROR_MESSAGE = (By.ID, "error-message")
    LOGIN_FORM_TITLE = (By.CSS_SELECTOR, "body > main > section > h1.login-form-title")

    @pytest.fixture(scope="function", autouse=True)
    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.URL)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 5)
        yield
        self.driver.quit()

    def field_login(self, login):
        self.driver.find_element(*self.LOGIN_FIELD).send_keys(login)

    def field_password(self, password):
        self.driver.find_element(*self.PASSWORD_FIELD).send_keys(password)

    def login_button(self):
        self.driver.find_element(*self.LOGIN_BUTTON).click()

    def logout_button(self):
        self.driver.find_element(*self.LOGOUT_BUTTON).click()

    def welcome_message_text(self):
        self.wait.until(ec.visibility_of_element_located(self.WELCOME_MESSAGE))
        return self.driver.find_element(*self.WELCOME_MESSAGE).text

    def error_message_text(self):
        self.wait.until(ec.visibility_of_element_located(self.ERROR_MESSAGE))
        return self.driver.find_element(*self.ERROR_MESSAGE).text

    @pytest.mark.parametrize(
        "login, password, expected", [("user1", "password1", "Welcome, user1!")]
    )
    def test_valid_data_login(self, login, password, expected):
        self.field_login(login)
        self.field_password(password)
        self.login_button()
        assert self.welcome_message_text() == expected

    @pytest.mark.parametrize(
        "login, password, expected",
        [
            ("user2", "password1", "Wrong login or password"),
            ("user1", "password2", "Wrong login or password"),
            ("login1", "", "Password is required (minimum 6 characters)"),
            ("", "password1", "Login is required (minimum 3 characters)"),
        ],
    )
    def test_invalid_login(self, login, password, expected):
        self.field_login(login)
        self.field_password(password)
        self.login_button()
        assert self.error_message_text() == expected

    def test_empty_fields(self):
        self.login_button()
        assert self.error_message_text() == (
            "Login and password are required" " (minimum 3 and 6 characters)"
        )

    @pytest.mark.parametrize(
        "login, password, expected", [("user1", "password1", "Welcome, user1!")]
    )
    def test_logout(self, login, password, expected):
        self.test_valid_data_login(login, password, expected)
        self.logout_button()
        assert self.driver.find_element(*self.LOGIN_FORM_TITLE).text == "Login Form"
