import json
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Registration:
    TEST_USERS_FILE = "test_users.json"
    
    def __init__(self, driver, url) -> None:
        self.driver = driver
        self.url = url
        
    def open_page(self) -> None:
        self.driver.get(self.url)
        self.driver.maximize_window()

    def load_test_users(self):
        """Загружает список зарегистрированных тестовых пользователей"""
        if os.path.exists(self.TEST_USERS_FILE):
            with open(self.TEST_USERS_FILE, 'r') as f:
                return json.load(f)
        return []

    def save_test_user(self, username, email):
        """Сохраняет данные зарегистрированного пользователя"""
        users = self.load_test_users()
        users.append({
            "username": username,
            "email": email,
            "timestamp": time.time()
        })
        with open(self.TEST_USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)

    def clear_test_users(self):
        """Очищает файл с тестовыми пользователями (для setup/teardown)"""
        if os.path.exists(self.TEST_USERS_FILE):
            os.remove(self.TEST_USERS_FILE)

    def register(self, login, email, password, confirm_password):
        
        try:
            self.driver.find_element(By.CSS_SELECTOR, 'a[href="/registration"]').click()
        except:
            pass
        
        login_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="login"]'))
        )
        login_field.send_keys(login)
        
        email_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[autocomplete="email"]'))
        )
        email_field.send_keys(email)
        
        password_field = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[placeholder="password"]'))
        )
        password_field.send_keys(password)
        
        confirm_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="repeatPassword"][type="password"]'))
        )
        confirm_field.send_keys(confirm_password)
        
        waiter = WebDriverWait(self.driver, 10)
        submit_button = waiter.until(
            EC.element_to_be_clickable((By.XPATH, '//button[.//span[text()="Confirm"]]'))
        )
        submit_button.click()