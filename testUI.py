import pytest
import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from Auth import Auth
from Register import Registration
from conftest import cleanup_test_users, base_url, driver

def test_login_positive(driver, base_url):
    login = "aaron2"
    password = "Vanushka2008"
    
    auth  = Auth(driver, base_url)
    auth.open_page()
    sleep(5)
    auth.login(login, password)
    icon = driver.find_element(By.CSS_SELECTOR, 'svg[viewBox="0 0 32 32"]')
    assert icon.is_displayed(), "Profile icon not displayed after login"

def test_registration_positive1(driver, base_url):
    timestamp = int(time.time())
    
    username = f"testuser_{timestamp}"
    email = f"testuser_{timestamp}@example.com"
    password = "TestPassword123!"
    confirm_password = "TestPassword123!"
    
    reg = Registration(driver, base_url)
    reg.open_page()
    time.sleep(3)
    
    reg.register(username, email, password, confirm_password)
    
    # Ожидание появления иконки профиля
    icon = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, 'svg[viewBox="0 0 32 32"]'))
    )
    assert icon.is_displayed(), "Profile icon not displayed after registration"
    
    print(f"\n✅ Успешная регистрация: {username} / {email}")
    reg.save_test_user(username, email)
    
    # Проверка, что мы НЕ на странице регистрации
    assert "register" not in driver.current_url.lower(), "Still on registration page"
    
    # URL может остаться прежним, это нормально
    print(f"📍 Текущий URL: {driver.current_url}")

def test_full_registration_and_login_flow(driver, base_url):
    """Полный сценарий: регистрация нового пользователя и авторизация с его данными"""

    # Шаг 1: Генерация уникальных данных
    timestamp = int(time.time())
    username = f"testuser_{timestamp}"
    email = f"testuser_{timestamp}@example.com"
    password = "TestPassword123!"
    
    print(f"\n📝 Сгенерированы данные:")
    print(f"   Username: {username}")
    print(f"   Email: {email}")
    print(f"   Password: {password}")

    # Шаг 2: Регистрация
    print("\n🔐 Шаг 1: Регистрация нового пользователя...")
    reg = Registration(driver, base_url)
    reg.open_page()
    time.sleep(3)
    
    reg.register(username, email, password, password)
    
    # Проверка успешной регистрации
    try:
        icon = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'svg[viewBox="0 0 32 32"]'))
        )
        assert icon.is_displayed(), "Profile icon not displayed after registration"
        print(f"✅ Регистрация успешна: {username}")
        
        # Проверка, что мы не на странице регистрации
        assert "register" not in driver.current_url.lower(), "Still on registration page"
        
    except TimeoutException:
        error_messages = driver.find_elements(By.XPATH, '//*[contains(@class, "error") or contains(text(), "already") or contains(text(), "exists")]')
        if error_messages:
            pytest.fail(f"Registration failed with error: {error_messages[0].text}")
        else:
            raise
    
    # Шаг 3: Выход из аккаунта
    try:
        # Ждём появления кнопки выхода
        logout_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "Logout") or contains(text(), "Sign out")]'))
        )
        logout_button.click()
        time.sleep(2)
        print("✅ Выполнен выход из аккаунта")
    except:
        print("⚠️ Кнопка выхода не найдена, продолжаем...")
    
    # Шаг 4: Переход на главную страницу для авторизации
    print("\n🔐 Шаг 2: Авторизация с зарегистрированными данными...")
    
    # Создаём новый экземпляр Auth
    auth = Auth(driver, base_url)
    
    # Открываем главную страницу
    auth.open_page()
    time.sleep(2)
    
    # Метод login теперь имеет ожидания
    auth.login(username, password)
    
    # Проверка успешной авторизации
    try:
        icon = WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'svg[viewBox="0 0 32 32"]'))
        )
        assert icon.is_displayed(), "Profile icon not displayed after login"
        print(f"✅ Авторизация успешна с логином: {username}")
        print("\n🎉 Полный цикл регистрация → авторизация успешно завершён!")
    except TimeoutException:
        pytest.fail("Login failed - profile icon not displayed")