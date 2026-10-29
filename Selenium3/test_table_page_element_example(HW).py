import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# TODO: 4) Переписать используя PageFactory (Lesson 5)

# Добавлена работа с таблицей 2
# Добавлен TC, в котором идет работа сразу с 2-я таблицами

# 1. Реализация Page Element для таблицы
class TableElement:
    def __init__(self, driver, locator):
        self.driver = driver
        self.locator = locator

    @property
    def element(self):
        return self.driver.find_element(*self.locator)

    def get_headers(self) -> list[str]:
        """Возвращает список заголовков таблицы."""
        header_elements = self.element.find_elements(By.CSS_SELECTOR, "thead th")
        return [header.text for header in header_elements]

    def get_row_data(self, row_index: int) -> list[str]:
        """Возвращает данные конкретной строки по её индексу (начиная с 0)."""
        rows = self.element.find_elements(By.CSS_SELECTOR, "tbody tr")
        cells = rows[row_index].find_elements(By.TAG_NAME, "td")
        return [cell.text for cell in cells]

    def get_cell_value(self, row_index: int, column_index: int) -> str:
        """Возвращает значение конкретной ячейки."""
        # реализовано через вызов get_row_data
        cell = self.get_row_data(row_index)[column_index]
        return cell


class TestTablePage:
    URL = "https://the-internet.herokuapp.com/tables"
    table1_locator = (By.ID, "table1")
    table2_locator = (By.ID, "table2")

    @pytest.fixture(scope="function", autouse=True)
    def driver(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(self.URL)
        self.wait = WebDriverWait(self.driver, 5)
        self.wait.until(EC.title_contains("The Internet"))
        yield
        self.driver.quit()

    @pytest.mark.parametrize("table_locator", [table1_locator, table2_locator])
    @pytest.mark.parametrize(" row_index, column_index, expected_value", [
        (1, 3, "$51.00"),
        (2,2, "jdoe@hotmail.com")])
    def test_table(self, table_locator, row_index, column_index, expected_value):
        # Инициализация таблицы как Page Element через её локатор
        table = TableElement(self.driver, table_locator)

        # Сбор данных для демонстрации
        headers = table.get_headers()
        first_row = table.get_row_data(0)
        specific_cell = table.get_cell_value(row_index, column_index)

        # Вывод результатов в консоль
        print("Заголовки таблицы:", headers)
        print("Первая строка данных:", first_row)
        print(f"Значение в строке {row_index}, колонке {headers[column_index]}: {specific_cell}")

        # Простые проверки (Assertions)
        assert "Last Name" in headers
        assert "Smith" in first_row
        assert specific_cell == expected_value

        print("\n✅ Тест успешно пройден!")

    @pytest.mark.parametrize("table1_locator, table2_locator, row_index, column_index, expected_value", [
        (table1_locator, table2_locator,1, 3, "$51.00"),
        (table1_locator, table2_locator, 2, 2, "jdoe@hotmail.com")])
    def test_two_tables(self, table1_locator, table2_locator, row_index, column_index, expected_value):
        table1 = TableElement(self.driver, table1_locator)
        table2 = TableElement(self.driver, table2_locator)
        specific_cell_1 = table1.get_cell_value(row_index, column_index)
        specific_cell_2 = table2.get_cell_value(row_index, column_index)

        assert specific_cell_1 == specific_cell_2 == expected_value
