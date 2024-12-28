# Import required libraries
from dotenv import load_dotenv  # For loading environment variables
import os
import time
from selenium import webdriver  # Main Selenium WebDriver
from selenium.webdriver.common.by import By  # For locating elements
from selenium.webdriver.support.ui import WebDriverWait  # For explicit waits
from selenium.webdriver.support import expected_conditions as EC  # Conditions for waits
from selenium.common.exceptions import TimeoutException  # Handle timeout errors
from selenium.webdriver.common.keys import Keys  # For keyboard interactions
from selenium.webdriver.chrome.options import Options  # Chrome-specific options
from selenium.webdriver.chrome.service import Service  # Chrome service management
from webdriver_manager.chrome import ChromeDriverManager  # Automatic chromedriver management

# Load environment variables from .env file
load_dotenv()

# Get LinkedIn credentials from environment variables
email = os.getenv("email")
password = os.getenv("password") 

# Configure Chrome options
options = Options()
options.add_argument("--start-maximized")  # Start browser maximized

# Initialize Chrome WebDriver with automatic driver management
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# Navigate to LinkedIn login page
driver.get("https://www.linkedin.com/login")

# Find and fill in email field
email_input = driver.find_element(By.ID, "username")
email_input.send_keys(email)

# Find and fill in password field
password_input = driver.find_element(By.ID, "password")
password_input.send_keys(password)

# Submit login form
password_input.send_keys(Keys.RETURN)

# Wait for page to load after login
time.sleep(5)  

def job_scrap(): 
    # Navigate to LinkedIn jobs page
    driver.get("https://www.linkedin.com/jobs/collections/") 
    
    try:
        # Wait up to 10 seconds for job listings to load
        # Look for elements with class containing 'job-card-container__link'
        job_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class, 'job-card-container__link')]"))
        )
        
        # Store job URLs for later processing
        job_urls = [job.get_attribute('href') for job in job_elements]
        
        # Visit each job posting page
        for index, url in enumerate(job_urls):
            driver.get(url)  # Navigate to job posting
            time.sleep(5)  # Wait for page to load   
              
            try:
                # Click "See more" button if available
                see_more_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'jobs-description__footer-button')]"))
                )
                see_more_button.click()
                time.sleep(5)  # Wait for content to load
            except TimeoutException:
                print(f"No 'See more' button found for job {index + 1}: {url}")


            page_html = driver.page_source
            filename = f"job_pages/job_{index + 1}.html"
            os.makedirs(os.path.dirname(filename), exist_ok=True) 

            with open(filename, "w", encoding="utf-8") as file:
                file.write(page_html)
                print(f"saved: {filename}")
    except TimeoutException:
        print("Failed to load job elements.")

try:
    # Main execution block
    print("Login Successful") 
    job_scrap()
except Exception as e:
    # Handle any unexpected errors
    print(f"Error occurred: {e}")    

# Clean up by closing the browser
driver.quit() 










