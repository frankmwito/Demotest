# Test assertion for page titles

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def test_lambdatest_title():
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service = service) 

    
        driver.get("https://ecommerce-playground.lambdatest.io/")
        driver.maximize_window()
    
        assert driver.title == "Your Store", "Assertion Error: That is not the expected title of the page"
        
        print(driver.title)
        
    finally:
        driver.quit()
    
    