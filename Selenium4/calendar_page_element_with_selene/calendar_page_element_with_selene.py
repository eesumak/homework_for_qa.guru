from selene import browser, by, be, have


# https://github.com/yashaka/selene

# переписать используя "голый" Selenium
# 1. Выполнено в файле "calendar_page_element_with_selenium"
class Calendar:
    def __init__(self, base_element):
        self.input_field = base_element

    def select_date(self, day: str, month: str, year: str):
        # 2. Выполнено: Как исправить - убрать всплывающее окно что мешает, используя Selene?

        # Переписать например такое Selenium решение на Selene - посмотреть насколько проще итоговый код
        # wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Level up your automation')]")))
        ## Находим и кликаем по кнопке закрытия (крестику) модального окна
        browser.element('//*[@id="fixedban"]/div/div/button').should(be.clickable).click()
        ## Ожидаем, пока баннер полностью исчезнет, чтобы он не перекрывал элементы формы
        browser.element('//*[@id="fixedban"]').should(be.hidden)

        self.input_field.click()
        browser.element(".react-datepicker__year-select").click().element(by.text(year)).click()
        browser.element(".react-datepicker__month-select").click().element(by.text(month)).click()

        day_padded = f"00{day}" if len(day) == 1 else f"0{day}"
        browser.element(f".react-datepicker__day--{day_padded}:not(.react-datepicker__day--outside-month)").click()


class AutomationPracticeFormPage:
    def __init__(self):
        browser.open("https://qa-guru.github.io/one-page-form/automation-practice-form.html")
        self.birthday_calendar = Calendar(browser.element("#dateOfBirthInput"))


class TestSuite:
    def test_select_birthday_date(self):
        page = AutomationPracticeFormPage()
        page.birthday_calendar.select_date(day="15", month="July", year="2000")
        page.birthday_calendar.input_field.should(have.value("15 Jul 2000"))


ts = TestSuite()
ts.test_select_birthday_date()
