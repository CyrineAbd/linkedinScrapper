from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from pymongo import MongoClient
import sys

# MongoDB connection setup
def connect_to_mongodb():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["linkedin_profiles"]
    collection = db["profiles"]
    return collection

# Save extracted profile data to MongoDB
def save_to_mongodb(data, collection):
    try:
        if data:
            # Check if the profile is already in the database using the profile URL
            if not collection.find_one({"url": data["url"]}):
                collection.insert_one(data)
                print("Data saved to MongoDB:", data)
            else:
                print("Profile already exists in MongoDB:", data["url"])
    except Exception as e:
        print(f"Error saving data to MongoDB: {e}")

# Initialize WebDriver
def init_driver():
    driver = webdriver.Chrome()  # Make sure to specify the correct path if needed
    return driver

# Log in to LinkedIn
def login_linkedin(driver, username, password):
    url = 'https://www.linkedin.com/login'
    driver.get(url)
    sleep(2)

    driver.find_element(By.ID, 'username').send_keys(username)
    driver.find_element(By.NAME, 'session_password').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button').click()
    sleep(2)

# Search profiles dynamically
def search_profiles(driver, query):
    search_url = f"https://www.linkedin.com/search/results/people/?keywords={query}"
    driver.get(search_url)
    sleep(5)

# Extract profile URLs on the current page
def get_profile_urls(driver):
    profiles = driver.find_elements(By.CSS_SELECTOR, 'a.app-aware-link')
    profile_urls = set()
    for profile in profiles:
        profile_id = profile.get_attribute('href')
        if profile_id and 'linkedin.com/in/' in profile_id:
            profile_urls.add(profile_id)
    return profile_urls

# Get profile URLs from multiple pages and stop after the specified number of pages
def get_urls_from_multiple_pages(driver, num_pages):
    all_profile_urls = set()

    for page in range(num_pages):
        current_page_urls = get_profile_urls(driver)
        all_profile_urls.update(current_page_urls)

        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(2)

        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.artdeco-pagination__button--next'))
            )
            next_button.click()
            sleep(3)
        except TimeoutException:
            print(f"Next button not found on page {page + 1}. Stopping.")
            break

    return all_profile_urls

# Extract data from individual profiles
def extract_profile_data(driver, url):
    try:
        driver.get(url)
        sleep(3)

        page_source = BeautifulSoup(driver.page_source, "html.parser")
        name = page_source.find('h1', class_='text-heading-xlarge').get_text(strip=True) if page_source.find('h1', class_='text-heading-xlarge') else "N/A"
        headline = page_source.find('div', class_='text-body-medium').get_text(strip=True) if page_source.find('div', class_='text-body-medium') else "N/A"
        address = page_source.find('span', class_='text-body-small inline t-black--light break-words').get_text(strip=True) if page_source.find('span', class_='text-body-small inline t-black--light break-words') else "N/A"

        return {"url": url, "name": name, "headline": headline, "address": address}

    except Exception as e:
        print(f"Error occurred while extracting data from {url}: {e}")
        return None

# Main execution
def main(query, num_pages):
    driver = init_driver()

    # Load LinkedIn credentials
    credential = open('login_credential.txt')
    line = credential.readlines()
    username = line[0].strip()
    password = line[1].strip()

    # Log in to LinkedIn
    login_linkedin(driver, username, password)

    # Search profiles
    search_profiles(driver, query)

    # Get profile URLs
    all_profiles = get_urls_from_multiple_pages(driver, num_pages)

    # Connect to MongoDB
    collection = connect_to_mongodb()

    # Extract and save profile data
    for profile_url in all_profiles:
        
        profile_data = extract_profile_data(driver, profile_url)
        save_to_mongodb(profile_data, collection)

    driver.quit()

if __name__ == "__main__":
    # Get query and number of pages from command line arguments
    query = sys.argv[1]
    num_pages = int(sys.argv[2])

    main(query, num_pages)
