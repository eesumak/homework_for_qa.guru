import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class LoginFormPage:
    URL = "https://qa-guru.github.io/one-page-form/login.html"
    LOGIN_FIELD = (By.ID, "login-input")
    PASSWORD_FIELD = (By.ID, "password-input")
    LOGIN_BUTTON = (By.ID, "submit-button")
    LOGOUT_BUTTON = (By.ID, "logout-button")
    WELCOME_MESSAGE = (By.ID, "welcome-message")
    ERROR_MESSAGE = (By.ID, "error-message")
    LOGIN_FORM_TITLE = (By.CSS_SELECTOR, "body > main > section > h1.login-form-title")

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        with allure.step('Открытие формы логина'):
            self.driver.get(self.URL)
            self.wait = WebDriverWait(self.driver, 5)

    def field_login(self, login):
        with allure.step('Ввод логина'):
            self.driver.find_element(*self.LOGIN_FIELD).send_keys(login)

    def field_password(self, password):
        with allure.step('Ввод пароля'):
            self.driver.find_element(*self.PASSWORD_FIELD).send_keys(password)

    def login_button(self):
        with allure.step('Клик кнопки входа'):
            self.driver.find_element(*self.LOGIN_BUTTON).click()

    def logout_button(self):
        with allure.step('Клик кнопки выхода'):
            self.driver.find_element(*self.LOGOUT_BUTTON).click()

    def welcome_message_text(self):
        with allure.step('Отображение приветствия'):
            self.wait.until(ec.visibility_of_element_located(self.WELCOME_MESSAGE))
            return self.driver.find_element(*self.WELCOME_MESSAGE).text

    def error_message_text(self):
        with allure.step('Отображение ошибки'):
            self.wait.until(ec.visibility_of_element_located(self.ERROR_MESSAGE))
            return self.driver.find_element(*self.ERROR_MESSAGE).text