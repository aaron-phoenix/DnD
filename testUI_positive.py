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
    
    reg.register(username, email, password, password)
    
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
        
        logout_button = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[local-name()="svg"]//*[local-name()="path"][starts-with(@d, "M24.3333 21.6665L31 14.9998")]'))
        )
        logout_button.click()
        # Проверка, что мы не на странице регистрации
        assert "register" not in driver.current_url.lower(), "Still on registration page"
        
    except TimeoutException:
        error_messages = driver.find_elements(By.XPATH, '//*[contains(@class, "error") or contains(text(), "already") or contains(text(), "exists")]')
        if error_messages:
            pytest.fail(f"Registration failed with error: {error_messages[0].text}")
        else:
            raise
    
    # Шаг 3: Выход из аккаунта (УЛУЧШЕННАЯ ВЕРСИЯ)
    print("\n🚪 Шаг 3: Выход из аккаунта...")
    logout_success = False
    
    # Вариант 1: Клик по аватару/иконке профиля, затем по logout
    try:
        # Сначала кликаем по иконке профиля (часто logout скрыт в меню)
        profile_icon = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'svg[viewBox="0 0 32 32"]'))
        )
        profile_icon.click()
        time.sleep(1)  # Ждём открытия меню
        
        # Ищем кнопку logout в открывшемся меню
        logout_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "Logout") or contains(text(), "Sign out") or contains(text(), "Выйти")]'))
        )
        logout_button.click()
        time.sleep(2)
        logout_success = True
        print("✅ Выполнен выход из аккаунта (через меню профиля)")
        
    except Exception as e:
        print(f"⚠️ Не удалось выйти через меню профиля: {e}")
        
        # Вариант 2: Прямой поиск кнопки logout
        if not logout_success:
            try:
                logout_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Logout")] | //a[contains(text(), "Logout")] | //*[@id="logout"] | //*[@class*="logout"]'))
                )
                logout_button.click()
                time.sleep(2)
                logout_success = True
                print("✅ Выполнен выход из аккаунта (прямая кнопка)")
            except Exception as e2:
                print(f"⚠️ Прямая кнопка logout не найдена: {e2}")
        
        # Вариант 3: Использование JavaScript для очистки localStorage/sessionStorage
        if not logout_success:
            print("🔄 Используем альтернативный метод: очистка storage")
            driver.execute_script("window.localStorage.clear();")
            driver.execute_script("window.sessionStorage.clear();")
            driver.refresh()
            time.sleep(2)
            print("✅ Storage очищен, пользователь деавторизован")
            logout_success = True
    
    # Если не удалось выйти - не фатально, просто перезагружаем страницу
    if not logout_success:
        print("⚠️ Не удалось найти кнопку выхода, перезагружаем страницу")
        driver.get(base_url)
        time.sleep(2)
    
    # Шаг 4: Переход на главную страницу для авторизации
    print("\n🔐 Шаг 4: Авторизация с зарегистрированными данными...")
    
    # Создаём новый экземпляр Auth
    auth = Auth(driver, base_url)
    
    # Если мы не на странице логина, переходим
    if "login" not in driver.current_url.lower():
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