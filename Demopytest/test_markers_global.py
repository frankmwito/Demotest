from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pytest
from faker import Faker

# Apply global markers
pytestmark = [pytest.mark.sanity, pytest.mark.smoke]

def test_lambda_form():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    try:
        driver.get("https://www.lambdatest.com/selenium-playground/input-form-demo")
        driver.maximize_window()
        
        # Initialize Faker
        faker = Faker()
        
        # Fill out the form with generated data
        name = faker.name()
        driver.find_element(By.XPATH, "//input[@id='name']").send_keys(name)
        
        email = faker.email()
        driver.find_element(By.XPATH, "//input[@id='inputEmail4']").send_keys(email)
        
        password = faker.password()
        driver.find_element(By.XPATH, "//input[@id='inputPassword4']").send_keys(password)
        
        company = faker.company()
        driver.find_element(By.XPATH, "//input[@id='company']").send_keys(company)
        
        website = faker.domain_name()
        driver.find_element(By.XPATH, "//input[@id='websitename']").send_keys(website)
        
        country = "India"  # Faker's generated countries may not match dropdown options
        dropdown = Select(driver.find_element(By.NAME, "country"))
        dropdown.select_by_visible_text(country)
        
        city = faker.city()
        driver.find_element(By.XPATH, "//input[@id='inputCity']").send_keys(city)
        
        address1 = faker.address()
        driver.find_element(By.ID, "inputAddress1").send_keys(address1)
        
        address2 = faker.address()
        driver.find_element(By.ID, "inputAddress2").send_keys(address2)
        
        state = faker.state()
        driver.find_element(By.ID, "inputState").send_keys(state)
        
        zipcode = faker.zipcode()
        driver.find_element(By.ID, "inputZip").send_keys(zipcode)
        
        # Submit the form
        driver.find_element(By.XPATH, "//button[normalize-space()='Submit']").click()
        
        print("Your form has been submitted successfully!")
    finally:
        driver.quit()
