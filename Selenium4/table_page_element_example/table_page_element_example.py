import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumpagefactory.Pagefactory import PageFactory

# Использовано PageFactory
# Добавлена работа с таблицей 2
# Добавлен TC, в котором идет работа сразу с 2-я таблицами


# 1. Реализация Page Element для таблицы
class TableElement:
    def __init__(self, table):
        self.element = table

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


class TablePage(PageFactory):
    URL = "https://the-internet.herokuapp.com/tables"

    locators = {"table1": ("ID", "table1"), "table2": ("ID", "table2")}

    def __init__(self, driver):
        self.driver = driver

    def get_table(self, table):
        # Возвращаем веб-элемент - таблицу
        return TableElement(getattr(self, table))


class TestTable:
    @pytest.fixture(scope="function", autouse=True)
    def driver(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.get(TablePage.URL)
        self.wait = WebDriverWait(self.driver, 5)
        self.wait.until(EC.title_contains("The Internet"))
        yield
        self.driver.quit()

    @pytest.mark.parametrize("table", ["table1", "table2"])
    @pytest.mark.parametrize(
        "row_index, column_index, expected_value",
        [(1, 3, "$51.00"), (2, 2, "jdoe@hotmail.com")],
    )
    def test_table(self, table, row_index, column_index, expected_value):

        # Получаем Web element (таблицу)
        table_page = TablePage(self.driver)
        table = table_page.get_table(table)

        # Сбор данных для демонстрации
        headers = table.get_headers()
        first_row = table.get_row_data(0)
        specific_cell = table.get_cell_value(row_index, column_index)

        # Вывод результатов в консоль
        print("Заголовки таблицы:", headers)
        print("Первая строка данных:", first_row)
        print(
            f"Значение в строке {row_index}, колонке {headers[column_index]}:"
            f" {specific_cell}"
        )

        # Простые проверки (Assertions)
        assert "Last Name" in headers
        assert "Smith" in first_row
        assert specific_cell == expected_value

        print("\n✅ Тест успешно пройден!")

    @pytest.mark.parametrize(
        "table1, table2, row_index, column_index, expected_value",
        [
            ("table1", "table2", 1, 3, "$51.00"),
            ("table1", "table2", 2, 2, "jdoe@hotmail.com"),
        ],
    )
    def test_two_tables(self, table1, table2, row_index, column_index, expected_value):
        table_page = TablePage(self.driver)
        table1 = table_page.get_table(table1)
        table2 = table_page.get_table(table2)
        specific_cell_1 = table1.get_cell_value(row_index, column_index)
        specific_cell_2 = table2.get_cell_value(row_index, column_index)

        assert specific_cell_1 == specific_cell_2 == expected_value
