from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

class Calendar:
    def __init__(self, driver,  base_element):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.input_field = base_element

    def select_date(self, day: str, month: str, year: str):
        self.wait.until(EC.title_contains("Practice Form"))
        # Ожидание появления и кликаем по кнопке закрытия (крестику) модального окна
        self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#fixedban > div > div > button"))).click()
        # Ожидаем, пока баннер полностью исчезнет, чтобы он не перекрывал элементы формы
        self.wait.until(EC.invisibility_of_element(
            (By.XPATH, '//*[@id="fixedban"]')))
        self.driver.find_element(*self.input_field).click()
        Select(self.driver.find_element(By.CLASS_NAME, "react-datepicker__year-select")).select_by_visible_text(year)
        Select(self.driver.find_element(By.CLASS_NAME, "react-datepicker__month-select")).select_by_visible_text(month)
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'#datepickerDays > span[data-day="{day}"]'))).click()

    def chek_select_date(self, value):
        select_date = self.driver.find_element(*self.input_field).get_attribute("value")
        assert select_date == value

class AutomationPracticeFormPage:
    def __init__(self, driver):
        self.driver = driver
        self.driver.maximize_window()
        self.driver.get("https://qa-guru.github.io/one-page-form/automation-practice-form.html")
        self.birthday_calendar = Calendar(self.driver, (By.ID, "dateOfBirthInput"))

class TestSuite:
    def test_select_birthday_date(self):
        driver = webdriver.Chrome()
        page = AutomationPracticeFormPage(driver)
        page.birthday_calendar.select_date(day="15", month="July", year="2000")
        page.birthday_calendar.chek_select_date("15 Jul 2000")
        driver.quit()

ts = TestSuite()
ts.test_select_birthday_date()
