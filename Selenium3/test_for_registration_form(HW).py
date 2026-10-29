import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TableElement:
    def __init__(self, driver, locator):
        self.driver = driver
        self.locator = locator

    @property
    def element(self):
        return self.driver.find_element(*self.locator)

    def get_row_data_by_name(self, row_name: str) -> list[str]:
        """Возвращает данные конкретной строки по её названию."""
        rows = self.element.find_elements(By.CSS_SELECTOR, "tbody tr")
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            # Если в строке есть ячейки, и значение первой равно нашему названию,
            # то возвращаем значения строки
            if cells and cells[0].text.strip() == row_name:
                return [cell.text for cell in cells]

    def get_cell_value_by_name(self, row_name: str, column_index: int) -> str:
        """Возвращает значение конкретной ячейки."""
        cell = self.get_row_data_by_name(row_name)[column_index]
        return cell


class TestStudentRegistrationForm:
    URL = "https://qa-guru.github.io/one-page-form/automation-practice-form.html"
    FIRST_NAME_INPUT = (By.ID, "firstName")
    LAST_NAME_INPUT  = (By.ID, "lastName")
    EMAIL_INPUT = (By.ID, "userEmail")
    GENDER_MALE = (By.ID,"gender-radio-1")
    GENDER_FEMALE = (By.ID, "gender-radio-2")
    GENDER_OTHER = (By.ID, "gender-radio-3")
    MOBILE_INPUT = (By.ID, "userNumber")
    DATE_OF_BIRTH = (By.ID, "dateOfBirthInput")
    SUBJECTS_INPUT = (By.ID, "subjectsInput")
    HOBBIES_SPORTS = (By.ID, "hobbies-checkbox-1")
    HOBBIES_READING = (By.ID, "hobbies-checkbox-2")
    HOBBIES_MUSIC = (By.ID, "hobbies-checkbox-3")
    PICTURE_LOAD_BUTTON = (By.ID, "uploadPicture")
    CURRENT_ADDRESS = (By.ID, "currentAddress")
    STATE_SELECT = (By.ID, "state")
    CITY_SELECT = (By.ID, "city")
    SUBMIT_BUTTON   = (By.ID, "submit")
    MESSAGE  = (By.ID, "formError")
    RESULT_FORM = (By.ID, "resultModal")
    RESULT_TABLE = (By.ID, "resultBody")

    @pytest.fixture(scope="function", autouse=True)
    def setup(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.URL)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 5)
        # Ожидание загрузки страницы (заголовок)
        self.wait.until(EC.title_contains("Practice Form"))
       # Ожидание появления и кликаем по кнопке закрытия (крестику) модального окна
        self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#fixedban > div > div > button"))).click()
        # Ожидаем, пока баннер полностью исчезнет, чтобы он не перекрывал элементы формы
        self.wait.until(EC.invisibility_of_element(
            (By.XPATH, "//*[contains(text(), 'Level up your automation')]")))
        yield
        self.driver.quit()

    def fill_name(self, first_name, last_name):
        self.driver.find_element(*self.FIRST_NAME_INPUT).send_keys(first_name)
        self.driver.find_element(*self.LAST_NAME_INPUT).send_keys(last_name)

    def fill_email(self, email):
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)

    def fill_gender(self, gender):
        self.driver.find_element(*gender).click()

    def fill_mobile(self, mobile):
        self.driver.find_element(*self.MOBILE_INPUT).send_keys(mobile)

    def select_subject(self, subject):
        self.driver.find_element(*self.SUBJECTS_INPUT).click()
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//div[contains(@class, 'subjects-auto-complete__option') and text()='{subject}']"))).click()

    def click_submit_button(self):
        self.driver.find_element(*self.SUBMIT_BUTTON).click()

    def check_message(self):
        return self.driver.find_element(*self.MESSAGE).text

    def check_result_form(self):
        self.wait.until(EC.visibility_of_element_located(self.RESULT_FORM))
        return self.driver.find_element(By.ID, "example-modal-sizes-title-lg").text


    @pytest.mark.parametrize("first_name, last_name, email, gender, mobile, subject, expected_result",
                             [("Иван",
                               "Иванов",
                               "ivan.ivanov@example.com",
                               GENDER_MALE,
                               "9051452345",
                               "History",
                               "Thanks for submitting the form")])
    def test_valid_registration_form(self, first_name, last_name,
                                     email, gender, mobile,
                                     subject, expected_result):
        self.fill_name(first_name, last_name)
        self.fill_email(email)
        self.fill_gender(gender)
        self.fill_mobile(mobile)
        self.select_subject(subject)
        self.click_submit_button()

        #Проверяем, что появилась форма с заполненными данными
        assert self.check_result_form() == expected_result
        # Проверяем, что значения в нужных строках
        result_table = TableElement(self.driver, self.RESULT_TABLE)
        assert (result_table.get_cell_value_by_name("Student Name", 1)
                == first_name + " " + last_name)
        assert (result_table.get_cell_value_by_name("Student Email", 1)
                == email)
        assert (result_table.get_cell_value_by_name("Gender", 1)
                == self.driver.find_element(*gender).get_attribute("value"))
        assert (result_table.get_cell_value_by_name("Mobile", 1)
                == mobile)
        assert (result_table.get_cell_value_by_name("Subjects", 1)
                == subject)
