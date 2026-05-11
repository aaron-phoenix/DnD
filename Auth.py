from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
        
        # Кнопка Confirm
        submit_button = waiter.until(
            EC.element_to_be_clickable((By.XPATH, '//button[.//span[text()="Confirm"]]'))
        )
        submit_button.click()
        