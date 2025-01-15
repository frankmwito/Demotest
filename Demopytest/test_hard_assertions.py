from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import unittest

class TestLambda(unittest.TestCase):  # Using unittest for hard assertions
    def test_hard(self):
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        
        try:
            # Navigate to the webpage
            driver.get("https://ecommerce-playground.lambdatest.io/")
            driver.maximize_window()
            
            # Verify Header
            header = driver.find_element(By.ID, "entry_217820")
            self.assertTrue(header.is_displayed(), "Assertion Error: Header is not displayed on the page.")
            
            # Verify Footer
            footer = driver.find_element(By.ID, "entry_217558")
            self.assertTrue(footer.is_displayed(), "Assertion Error: Footer is not displayed on the page.")
            
            # Verify Search Bar
            search_bar = driver.find_element(By.XPATH, "(//input[@placeholder='Search For Products'])[1]")
            self.assertTrue(search_bar.is_displayed(), "Assertion Error: Search bar is not displayed on the page.")
            
            print("All elements verified successfully!")
        
        finally:
            driver.quit()
