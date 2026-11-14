import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with

# Для работы относительных локаторов необходимо импортировать класс with_tag_name (или with_name / with_id) из модуля selenium.webdriver.support.relative_locator.

# Инициализация драйвера (например, для Chrome)
driver = webdriver.Chrome()
driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
driver.maximize_window()

time.sleep(3)
# Находим label, затем поле ввода под ним
full_name_label = driver.find_element(By.XPATH, "//label[text()='Full Name']")
email_input = driver.find_element(locate_with(By.TAG_NAME, "input").below(full_name_label))
email_input.send_keys("ivan@example.com")

time.sleep(3)
# Находим поле Full Name и вводим в поле НАД элементом
submit_btn = driver.find_element(By.ID, "submit")
full_name_input = driver.find_element(locate_with(By.TAG_NAME, "input").above(email_input))
full_name_input.send_keys("Ivan Ivanov")

time.sleep(3)
# Поиск элемента, расположенного около определенного текста
label_element = driver.find_element(By.XPATH, "//label[text()='Current Address']")
address_textarea = driver.find_element(locate_with(By.TAG_NAME, "textarea").near(label_element))
address_textarea.send_keys("г. Минск, ул. Академическая")

time.sleep(3)

driver.get("https://qa-guru.github.io/one-page-form/automation-practice-form.html")

# Ищем элемент справа от первого найденного радиобатона
first_radio = driver.find_element(By.NAME, "gender")
second_radio = driver.find_element(locate_with(By.TAG_NAME, "input").to_right_of(first_radio))
second_radio.click()

time.sleep(3)
# Если радиокнопки или чекбоксы стоят в ряд, можно искать левый элемент
first_radio = driver.find_element(locate_with(By.TAG_NAME, "input").to_left_of(second_radio))
first_radio.click()



