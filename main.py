from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import keyboard
import math
import time
import concurrent.futures


# Функция, выполняющая основную работу.
def up_salegroup(url, email, password):
    # options
    chrome_options = webdriver.ChromeOptions()
    # Юзер-Агент
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")
    # Запуск в фоновом режиме. Пока не включаем.
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    # Передаем параметры в driver
    driver = webdriver.Chrome(options=chrome_options)
    # Открываем на весь экран
    driver.maximize_window()
    # Переходим по ссылке
    driver.get(url)
    try:
        # Процесс авторизации.
        auth = driver.find_element(By.CSS_SELECTOR, "button[data-target='#loginModal']")
        auth.click()
        time.sleep(1)
        # Находим поля для ввода и кнопку.
        email_input = driver.find_element(By.CSS_SELECTOR, "input[name='_username']")
        password_input = driver.find_element(By.CSS_SELECTOR, "input[name='_password']")
        login_button = driver.find_element(By.CSS_SELECTOR, "button#submit_login")

        # Ввод данных для авторизации
        email_input.send_keys(f"{email}")
        password_input.send_keys(f"{password}")

        login_button.click()

        time.sleep(2)
    except Exception as ex:
        print('Ошибка в авторизации на salegroups')
        print(ex)

    # Заходим в список объявлений.
    driver.get('https://salegroups.ru/user/adverts/')
    time.sleep(1)

    # Узнаем кол-во объявлений.
    try:
        link_element = driver.find_element(By.CSS_SELECTOR, "a.post-row__group-name")
        link_element.click()
        time.sleep(1)
        # Ждем, пока элемент с классом "box__part-title" загрузится на странице
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'box__part-title')))

        # Находим все элементы с классом "box__part-title"
        elements = driver.find_elements(By.CLASS_NAME, 'box__part-title')

        # Получаем текст второго элемента, который содержит "Другие объявления продавца (1384)"
        element_text = elements[1].text if len(elements) > 1 else None

        if element_text:
            # Извлекаем число из строки "Другие объявления продавца (1384)"
            number = element_text.split('(')[-1].split(')')[0]
            # Определяем промежуток нажатия на кнопку по формуле: 5 дней (в секундах) делим на количество карточек (с округлением в > + 1 сек).
            wait_click = 432000 / int(number)
            rounded_value = math.ceil(wait_click)
            print(rounded_value)
        else:
            rounded_value = 480
    except Exception as ex:
        print('Не нашел количетсов объявлений.')
        print(ex)
    # Переходим обратно на страницу с объявлениями и жмем на кнопки.
    driver.get('https://salegroups.ru/user/adverts/')
    time.sleep(3)
    while True:
        try:
            time.sleep(3)
            # Находим все элементы с классом 'post-row'
            post_elements = driver.find_elements(By.CLASS_NAME, 'post-row')
        except Exception:
            print('Не найдены элементы post-row')


        # Обходим все элементы с классом 'post-row'
        for post_element in post_elements:
            # Проверяем наличие элемента с классом 'post-row__actions'
            try:
                actions_element = post_element.find_element(By.CLASS_NAME, 'post-row__actions')
            except NoSuchElementException:
                # Если элемента 'post-row__actions' нет, пропускаем этот пост
                print('Не найден, пропускаю.')
                time.sleep(rounded_value)
                continue
            try:
                # Проверяем наличие формы с классом 'post-row__action' (для кнопки синхронизации)
                sync_button_element = actions_element.find_element(By.CSS_SELECTOR, 'form[data-entity="sync-group"]')
                print('Кнопка присутствует, нажимаю')
                sync_button_element.submit()
            except Exception:
                print('Пропускаю')
                time.sleep(rounded_value)
        try:
            # Ждем, пока элемент станет кликабельным
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//li[@class="pagination__next"]/a')))
            # Кликаем на элемент
            next_button.click()
            time.sleep(10)
        except Exception:
            print('Кнопка не найдена. Завершаю работу и начинаю заного!')
            break
# Функция для парсинга данных из файла
def parse_config_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip().split('|') for line in lines]

def main():
    while True:
        config_data = parse_config_file('config.txt')
        up_salegroup(config_data[0][0], config_data[0][1], config_data[0][2])



# Точка входа.
if __name__ == '__main__':
    main()

