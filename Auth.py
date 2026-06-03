from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class Auth:
    def __init__(self, driver, url) -> None:
        self.driver = driver
        self.url = url
        
    def open_page(self) -> None:
        self.driver.get(self.url)
        self.driver.maximize_window()

    def login(self, login, password):
        # Клик по ссылке логина с ожиданием
        waiter = WebDriverWait(self.driver, 10)
        login_link = waiter.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="/login"]'))
        )
        login_link.click()
        
        # Поле login с ожиданием
        login_field = waiter.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="login"]'))
        )
        login_field.send_keys(login)
        
        # Поле password
        password_field = self.driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
        password_field.send_keys(password)

    def submit_click(self):
        waiter = WebDriverWait(self.driver, 10)
        # Кнопка Confirm
        submit_button = waiter.until(
            EC.element_to_be_clickable((By.XPATH, '//button[.//span[text()="Confirm"]]'))
        )
        submit_button.click()

    def is_submit_enabled(self):
        """Проверяет, активна ли кнопка Confirm"""
        waiter = WebDriverWait(self.driver, 10)
        submit_button = waiter.until(
            EC.presence_of_element_located((By.XPATH, '//button[.//span[text()="Confirm"]]'))
        )
        return submit_button.is_enabled()

    def get_submit_button(self):
        """Возвращает элемент кнопки Confirm"""
        waiter = WebDriverWait(self.driver, 10)
        return waiter.until(
            EC.element_to_be_clickable((By.XPATH, '//button[.//span[text()="Confirm"]]'))
        )
        
    def get_error_message(self, expected_text=None):
        """Получает сообщение об ошибке"""
        waiter = WebDriverWait(self.driver, 10)
        if expected_text:
            return waiter.until(
                EC.visibility_of_element_located((By.XPATH, f'//*[contains(text(), "{expected_text}")]'))
            )
        else:
            # Ищем любое сообщение об ошибке
            return waiter.until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.error-message, .alert-danger, [role="alert"]'))
            )
    def is_error_displayed(self, expected_text=None):
        """Проверяет, отображается ли сообщение об ошибке"""
        try:
            self.get_error_message(expected_text)
            return True
        except TimeoutException:
            return False
    
    def get_field_validation_message(self, field_name):
        """Получает сообщение валидации для конкретного поля"""
        waiter = WebDriverWait(self.driver, 10)
        return waiter.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, f'input[name="{field_name}"] ~ .error-message, .invalid-feedback'))
        )