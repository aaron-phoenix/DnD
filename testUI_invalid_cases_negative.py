import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from Auth import Auth


# Массив невалидных данных
invalid_credentials_front = [
    ("123", "Vanushka08", "User with this username does not exist"),  # несуществующий пользователь
    ("aaron", "Wrong1234", "Invalid password"),  # неверный пароль
    ("aaron", "wrong", "Password must be at least 8 characters, include uppercase, lowercase and a number"), #неверный пароль менее 8 символов
    ("admin", "12345678", "Password must be at least 8 characters, include uppercase, lowercase and a number"),  # пароль из одних цифр валидной длины
    ("user", "pass", "Password must be at least 8 characters, include uppercase, lowercase and a number")  # общие неверные данные
]

invalid_credentials_back = [
    ("", "Vanushka08", "Login is required"),  # пустой логин
    ("test@user", "Pass1234", "Invalid email format"),  # invalid email как логин
    ("verylongusernamethatshouldnotexist", "Password1", "Login must be no more than 30 characters"),  # длинный логин
    ("пролтримпрольтимсвак", "Password1", "Login can contain only Latin letters, numbers, dots, hyphens and underscores"),   #логин на кириллице
    ("///dfghjkjhgfdfghjkj", "Password1", "Login can contain only Latin letters, numbers, dots, hyphens and underscores"),   #запрещенные символы
    ("'\\\'dfghjkjhgfdfghjkj", "Password1", "Login can contain only Latin letters, numbers, dots, hyphens and underscores"),   #запрещенные символы
    ("fghh()jdghfdg()", "Password1", "Login can contain only Latin letters, numbers, dots, hyphens and underscores"),
    ("<><><><><><>ghjnghjn", "Password1", "Login can contain only Latin letters, numbers, dots, hyphens and underscores"),
    (".....fghhdfgh.......", "Password1", "Login format is invalid"),
    ("df--ghjkjhgf--ghjkj", "Password1", "Login format is invalid"),
    ("dfgh___jkjhgfdfghjkj", "Password1", "Login format is invalid"),
    ("...fgfghhnbvc", "Password1", "Login format is invalid"),
    ("---fgfghhnbvc", "Password1", "Login format is invalid"),
    ("___fghfghnbvc", "Password1", "Login format is invalid"),
    ("fghnb...", "Password1", "Login format is invalid"),
    ("fghnb---", "Password1", "Login format is invalid"),
    ("fghnb___", "Password1", "Login format is invalid"),
    ("dfghj😀😀😀dfghjdcvbn", "Password1", "Login can contain only Latin letters, numbers, dots, hyphens and underscores"),   #смайлы
    ("dfghj男男男dfghjdcvbn", "Password1", "Login can contain only Latin letters, numbers, dots, hyphens and underscores")      #иероглифы
]

invalid_credentials_empty = [
    ("aaron", "", "Password is required")
]
def check_error_message(driver, login, password, expected_error):
    """Общая функция проверки сообщения об ошибке"""
    try:
        error_message = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, f'//*[contains(text(), "{expected_error}")]'))
        )
        assert error_message.is_displayed()
        print(f"✅ Найдено сообщение об ошибке: {error_message.text} для логина '{login}'")
    except TimeoutException:
        driver.save_screenshot(f"login_error_not_found_{login}_{password[:3]}.png")
        pytest.fail(f"Error message '{expected_error}' not found for login: '{login}', password: '{password}'")

@pytest.mark.parametrize("login,password,expected_error", invalid_credentials_front)
def test_login_frontend_negative(driver, base_url, login, password, expected_error):
    auth = Auth(driver, base_url)
    auth.open_page()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    
    auth.login(login, password)
    auth.submit_click()
    check_error_message(driver, login, password, expected_error)

@pytest.mark.parametrize("login,password,expected_error", invalid_credentials_back)
def test_login_backend_negative(driver, base_url, login, password, expected_error):
    auth = Auth(driver, base_url)
    auth.open_page()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    
    auth.login(login, password)
    # Проверяем, что кнопка неактивна или форма не отправляется
    assert not auth.is_submit_enabled(), "Submit button should be disabled for invalid input"
    check_error_message(driver, login, password, expected_error)

@pytest.mark.parametrize("login,password,expected_error", invalid_credentials_empty)
def test_empty_password(driver, base_url, login, password, expected_error):
    auth = Auth(driver, base_url)
    auth.open_page()
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )
    auth.login(login, password)
    # Кликаем в любое другое место на странице
    click_empty = driver.find_element(By.CSS_SELECTOR, ".LoginPageForm-module-scss-module__-A6TXq__header")
    click_empty.click()
    
    check_error_message(driver, login, password, expected_error)
