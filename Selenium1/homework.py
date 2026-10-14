import time
from selenium import webdriver
from selenium.webdriver.common.by import By

# 1. Запуск браузера Chrome
driver = webdriver.Chrome()

try:
    # 2. Открытие страницы
    driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
    driver.maximize_window()
    time.sleep(5)  # Пауза, чтобы визуально заметить открытие

    # 3. Поиск элементов и заполнение полей
    # Находим поле Full Name по его ID и вводим текст
    full_name_field = driver.find_element(By.ID, "userName")
    # web_elements = driver.find_elements(By.XPATH, "someXPath")

    full_name_field.send_keys("Василий Васильев")

    # Находим поле Email по его ID и вводим текст
    email_field = driver.find_element(By.ID, "userEmail")
    email_field.send_keys("ivan@example.com")

    # Находим кнопку Submit по ее ID и кликаем
    submit_button = driver.find_element(By.ID, "submit")
    submit_button.click()

    # 4. Проверка результата
    time.sleep(5)  # Пауза, чтобы увидеть результат отправки

    # Находим блок с отправленными данными
    result_box = driver.find_element(By.ID, "name")

    # Проверяем, что в блоке результата появился введенный текст в нужном поле
    assert "Василий Васильев" in result_box.text
    print("Тест на проверку Full Name успешно пройден!")

finally:
    # 5. Закрытие браузера в любом случае
    driver.quit()

# 1.Запуск браузера Chrome
driver = webdriver.Chrome()

try:
    # 2. Открытие страницы
    driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
    driver.maximize_window()
    time.sleep(5)  # Пауза, чтобы визуально заметить открытие

    # 3. Поиск элементов и заполнение полей
    full_name_field = driver.find_element(By.ID, "userName")
    full_name_field.send_keys("Василий Васильев")
    email_field = driver.find_element(By.ID, "userEmail")
    email_field.send_keys("ivanexample.com")
    submit_button = driver.find_element(By.ID, "submit")
    submit_button.click()

    # 4. Проверка результата
    time.sleep(5)  # Пауза, чтобы увидеть результат отправки

    # Находим блок с отправленными данными
    result_box = driver.find_element(By.ID, "output")

    # Проверяем, что в блоке результата нет некорректного ввода
    assert "ivanexample.com" not in result_box.text
    print("Тест на проверку контроля Email успешно пройден!")

finally:
    # 5. Закрытие браузера в любом случае
    driver.quit()

# 1. Запуск браузера Chrome
driver = webdriver.Chrome()

try:
    # 2. Открытие страницы
    driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
    driver.maximize_window()
    time.sleep(5)  # Пауза, чтобы визуально заметить открытие

    # 3. Поиск элементов и заполнение полей
    full_name_field = driver.find_element(By.ID, "userName")
    full_name_field.send_keys("Василий Васильев")
    email_field = driver.find_element(By.ID, "userEmail")
    email_field.send_keys("ivan@example.com")

    # Находим поле Current Address по его ID и вводим текст
    currentAddress_field = driver.find_element(By.ID, "currentAddress")
    currentAddress_field.send_keys("г. СПб Невский проспект")

    # Находим кнопку Submit по ее ID и кликаем
    submit_button = driver.find_element(By.ID, "submit")
    submit_button.click()

    # 4. Проверка результата
    time.sleep(5)  # Пауза, чтобы увидеть результат отправки

    # Находим в блок с отправленными данными
    result_box = driver.find_element(By.ID, "output")
    result_box_current = result_box.find_element(By.ID, "currentAddress")

    # Проверяем, что в блоке результата появился введенный текст в нужном поле
    assert "Current Address :г. СПб Невский проспект" == result_box_current.text
    print("Тест успешно пройден!")

finally:
    # 5. Закрытие браузера в любом случае
    driver.quit()

# 1. Запуск браузера Chrome
driver = webdriver.Chrome()

try:
    # 2. Открытие страницы
    driver.get("https://qa-guru.github.io/one-page-form/text-box.html")
    driver.maximize_window()
    time.sleep(5)  # Пауза, чтобы визуально заметить открытие

    # 3. Поиск элементов и заполнение полей
    full_name_field = driver.find_element(By.ID, "userName")
    full_name_field.send_keys("Василий Васильев")
    email_field = driver.find_element(By.ID, "userEmail")
    email_field.send_keys("ivan@example.com")
    currentAddress_field = driver.find_element(By.ID, "currentAddress")
    currentAddress_field.send_keys("г. СПб Невский проспект")

    # Находим поле Permanent Address по его ID и вводим текст
    permanentAddress_field = driver.find_element(By.ID, "permanentAddress")
    permanentAddress_field.send_keys("СПб")

    # Находим кнопку Submit по ее ID и кликаем
    submit_button = driver.find_element(By.ID, "submit")
    submit_button.click()

    # 4. Проверка результата
    time.sleep(5)  # Пауза, чтобы увидеть результат отправки

    # Находим в блок с отправленными данными
    result_box = driver.find_element(By.ID, "output")

    # Проверяем, что в блоке результата появился введенный текст и что его нет в ненужном поле
    assert "СПб" in result_box.text
    assert "Permananet Address :СПб" != result_box.find_element(By.ID, "currentAddress").text
    assert "СПб" not in result_box.find_element(By.ID, "email").text
    assert "СПб" not in result_box.find_element(By.ID, "name").text


    print("Тест успешно пройден!")

finally:
    # 5. Закрытие браузера в любом случае
    driver.quit()
