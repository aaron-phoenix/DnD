import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

TEST_USERS_FILE = "test_users.json"

@pytest.fixture(scope="session", autouse=True)
def cleanup_test_users():
    """Очищает файл с тестовыми пользователями после всех тестов"""
    yield
    if os.path.exists(TEST_USERS_FILE):
        os.remove(TEST_USERS_FILE)


@pytest.fixture(scope="session")
def base_url():
    try:
        with open("url.txt", "r") as file:
            base_url = file.read().strip()
            
            if not base_url:
                pytest.fail("Файл url.txt пуст!")
            
            return base_url
    except FileNotFoundError:
        pytest.fail("Файл url.txt не найден!")

@pytest.fixture
def driver():
    """Фикстура для инициализации и закрытия браузера"""
    options = Options()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # Для безголового режима
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()