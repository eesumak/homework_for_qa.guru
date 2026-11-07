import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


class TestTextBox:
    URL = "https://qa-guru.github.io/one-page-form/text-box.html"
    FULL_NAME_FIELD = (By.ID, "userName")
    EMAIL_FIELD = (By.ID, "userEmail")
    CURRENT_ADDRESS_FIELD = (By.ID, "currentAddress")
    PERMANENT_ADDRESS_FIELD = (By.ID, "permanentAddress")
    SUBMIT_BUTTON = (By.ID, "submit")
    RESULT_BOX = (By.ID, "output")
    RESULT_NAME = (By.ID, "name")
    RESULT_EMAIL = (By.ID, "email")


    @pytest.fixture(scope="function", autouse=True)
    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.URL)
        self.driver.maximize_window()
        yield
        self.driver.quit()

    # Заполнение полей
    def full_name_field(self, full_name):
        self.driver.find_element(*self.FULL_NAME_FIELD).send_keys(full_name)

    def email_field(self, email):
        self.driver.find_element(*self.EMAIL_FIELD).send_keys(email)

    def current_address_field(self, current_address):
        (
            self.driver.find_element(*self.CURRENT_ADDRESS_FIELD).send_keys(
                current_address)
        )

    def permanent_address_field(self, permanent_address):
        (
            self.driver.find_element(*self.PERMANENT_ADDRESS_FIELD).send_keys(
                permanent_address)
        )

    # Клик кнопки
    def submit_button(self):
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    # Результирующий блок
    def result_box(self):
        return self.driver.find_element(*self.RESULT_BOX)

    def result_box_name(self):
        return self.driver.find_element(*self.RESULT_NAME).text

    def result_box_email(self):
        return self.driver.find_element(*self.RESULT_EMAIL).text


    # Проверки
    @pytest.mark.parametrize("full_name, email", [
        ("Василий Васильев", "ivan@example.com"),
        ("Petr Petrov", "petrov@gmail.com")
    ])
    def test_valid_data(self, full_name, email):
        self.full_name_field(full_name)
        self.email_field(email)
        self.submit_button()
        assert full_name in self.result_box_name()
        assert email in self.result_box_email()
        print("Тест на проверку Full Name and Email успешно пройден!")


    @pytest.mark.parametrize("email", [
        "ivanexample.com","p@.org"
    ])
    def test_invalid_email(self, email):
        self.email_field(email)
        self.submit_button()
        assert email not in self.result_box().text
        print("Тест на проверку контроля Email успешно пройден!")


    @pytest.mark.parametrize("current_address", [
        "г. Барнаул, ул. Индустриальная", "г. СПб, Невский проспект"
    ])
    def test_valid_current_address(self, current_address):
        self.current_address_field(current_address)
        self.submit_button()
        assert (
            current_address
            in self.result_box().find_element(*self.CURRENT_ADDRESS_FIELD).text
        )
        print("Тест на проверку Current Address успешно пройден!")


    @pytest.mark.parametrize("full_name, email, current_address, permanent_address", [
        ("Василий Васильев","ivan@example.com", "г. СПб Невский проспект", "СПб"),
        ("Ekaterina Sumak", "eesumak@gmail.com", "St. Petersburg", "Essentuki")
    ])
    def test_valid_full_data(
        self, full_name, email, current_address, permanent_address
    ):
        self.full_name_field(full_name)
        self.email_field(email)
        self.current_address_field(current_address)
        self.permanent_address_field(permanent_address)
        self.submit_button()
        assert full_name in self.result_box_name()
        assert email in self.result_box_email()
        assert (
            current_address
            in self.result_box().find_element(*self.CURRENT_ADDRESS_FIELD).text
        )
        assert (
            permanent_address
            in self.result_box().find_element(*self.PERMANENT_ADDRESS_FIELD).text
        )
        print("Тест успешно пройден!")
