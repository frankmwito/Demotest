from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from faker import Faker
import pytest
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def shared_credentials():
    first_name = "Frank"
    last_name = "Lambert"
    email = "flambert22@gmail.com"
    telephone = "1312345678"
    password = "1234567890"
    return first_name, last_name, email, telephone, password

@pytest.fixture(autouse=True)
def setup_automatic_fixture():
    print("\nStarting a Test")
    yield
    print("\nTest Completed")

@pytest.fixture(scope="function")
def setup_teardown1():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://ecommerce-playground.lambdatest.io/")
    driver.maximize_window()
    yield driver  # Return the driver to test functions
    print("\nThis is the Teardown")
    driver.quit()

@pytest.mark.usefixtures("setup_teardown1")
def test_signup(setup_teardown1):  
    driver = setup_teardown1
    faker = Faker()
    first_name = faker.first_name()  
    last_name = faker.last_name()
    email = faker.email()
    telephone = faker.phone_number()  
    password = faker.password()

    # Hover over My Account
    my_account = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="widget-navbar-217834"]/ul/li[6]/a'))
    )
    actions = ActionChains(driver)
    actions.move_to_element(my_account).perform()

    # Click Register
    register = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Register']"))
    )
    register.click()

    # Fill Registration Form
    driver.find_element(By.ID, "input-firstname").send_keys(first_name)
    driver.find_element(By.ID, "input-lastname").send_keys(last_name)
    driver.find_element(By.ID, "input-email").send_keys(email)
    driver.find_element(By.ID, "input-telephone").send_keys(telephone)
    driver.find_element(By.ID, "input-password").send_keys(password)
    driver.find_element(By.ID, "input-confirm").send_keys(password)

    # Click radio buttons
    driver.find_element(By.XPATH, "//label[normalize-space()='No']").click()
    driver.find_element(By.XPATH, "//label[normalize-space()='Yes']").click()

    # Click agree checkbox
    agree_checkbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//label[@for='input-agree']"))
    )
    agree_checkbox.click()

    # Click continue
    continue_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@value='Continue']"))
    )
    continue_button.click()

    # Wait for success page
    time.sleep(2)
    assert "success" in driver.current_url or "account/success" in driver.current_url, "Registration was not successful."

@pytest.mark.usefixtures("setup_teardown1")
def test_login(shared_credentials, setup_teardown1):
    driver = setup_teardown1
    first_name, last_name, email, telephone, password = shared_credentials
    wait = WebDriverWait(driver, timeout=10, poll_frequency= 2)

    myaccount = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="widget-navbar-217834"]/ul/li[6]/a'))) 
    actions = ActionChains(driver)
    actions.move_to_element(myaccount).perform()
    
    login = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Login']")))
    login.click()

    WebDriverWait(driver, timeout= 5, poll_frequency= 1)
    driver.find_element(By.ID, "input-email").send_keys(email)
    driver.find_element(By.ID, "input-password").send_keys(password)
    driver.find_element(By.XPATH, "//input[@value='Login']").click()

    welcome = driver.find_element(By.XPATH, "(//h2[normalize-space()='My Account'])[1]").text
    print(welcome)
    assert "my account" == welcome.lower(), "Login Failed"
