import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess


# Read categories and cities from text files with 'utf-8' encoding
with open('search_quaries/categories', 'r+', encoding='utf-8') as category_file:
    categories = category_file.read().splitlines()

with open('search_quaries/cities.txt', 'r+', encoding='utf-8') as city_file:
    cities = city_file.read().splitlines()

# Define the elements you want to scrape and their corresponding column names
elements_to_scrape = [
    'Category','City','Title', 'Rating', 'TimesRated', 'Address', 'Phone', 'Instagram'
]

data_df = pd.DataFrame(columns=elements_to_scrape)
data_df.to_csv('database_example.csv', mode='a', header=True, index=False, encoding='utf-8')

def scrape_driver_setup():
    #setting up the driver source(it will always in sync with and current chrome version) + removing image loading
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    ## Add Options to Webdriver
    driver = webdriver.Chrome(options=chrome_options)
    captchadriver = webdriver.Chrome()
    driver.get("https://easy.co.il/list/Hair-Design")
    return driver, captchadriver

# scripts to play music and pause music from spotify, its for a notification about a captcha.
#delete or change as needed.
playscript_path = 'subscripts/playscript.scpt'
pausescript_path = 'subscripts/pausescript.scpt'

driver, captchadriver = scrape_driver_setup()

def captchaon(url):
    print("captcha")
    captchadriver.get(url)
    subprocess.call(['osascript', playscript_path])
    while "captcha" in captchadriver.current_url:
        time.sleep(5)
    subprocess.call(['osascript', pausescript_path])
    time.sleep(4)
    driver.get(captchadriver.current_url)
    return

def savedata(col, data):
        if col == 'Title':
            try:
                title = WebDriverWait(driver, 0.2).until(EC.presence_of_element_located((By.CLASS_NAME, "biz-title"))).text
            except Exception as e:
                title = ("אין")
            data['Title'].append(title)
        elif col == 'Rating':
            try:
                rating = WebDriverWait(driver, 0.2).until(EC.presence_of_element_located(
                    (By.XPATH, "//*[@id='app']/div[2]/main/div/div/div[1]/div[1]/div[1]/div[2]/div/span"))).text
            except Exception as e:
                rating = '0.0'
            data['Rating'].append(rating)

        elif col == 'TimesRated':
            try:
                times_rated= WebDriverWait(driver, 0.2).until(
                    EC.presence_of_element_located((By.ID, "headerItemReviewBox"))).text
            except Exception as e:
                # Handle other exceptions
                times_rated = '0 ביקורות'
            data['TimesRated'].append(times_rated)

        elif col == 'Address':
            try:
                address = WebDriverWait(driver, 0.2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "biz-address-text"))).text
            except Exception as e:
                address = 'אין'
            data['Address'].append(address)

        elif col == 'Phone':
            try:
                phone = WebDriverWait(driver, 0.2).until(EC.presence_of_element_located((By.ID, "action-phone-label"))).text
            except Exception as e:
                phone = 'אין'
            data['Phone'].append(phone)

        elif col == 'Instagram':
            try:
                instagram = WebDriverWait(driver, 0.2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "biz-action-button.instagram"))).find_element(By.TAG_NAME,"a").get_attribute("href")
            except Exception as e:
                instagram = 'אין'
            data['Instagram'].append(instagram)

        elif col == 'City':
            data['City'].append(city)
        elif col == 'Category':
            data['Category'].append(category)

# Iterate through each category and city combination
for category in categories:
    for city in cities:
        query_sent,true1,done_load_more,li_elements_found = 0,0,0,0
        query = f"{category} {city}"

        # Create an empty dictionary to store the data
        data = {col: [] for col in elements_to_scrape}

        while True:
            # Define the search query
            while query_sent == 0:
                try:
                    # Send the search terms
                    driver.get("https://easy.co.il/list/Hair-Design")
                    print(f"now scraping {query}")
                    search_input = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "SearchInputBiz")))
                    search_input.send_keys(query)
                    search_input.send_keys(Keys.RETURN)
                    print(f"keys sent")
                    query_sent = 1
                except Exception:
                    if 'captcha' in driver.current_url:
                        captchaon(driver.current_url)

                    continue

            href_links = []
            while True:
                # Click the "Load More" button if it exists
                while done_load_more == 0:
                    try :
                        load_more_button = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "next-page-button")))
                        load_more_button.click()
                    except Exception as e:
                        if 'captcha' in driver.current_url:
                            captchaon(driver.current_url)
                        else:
                            done_load_more = 1
                            print("no more load more button")
            # Collect href links from the <li> element
                try:
                    li_elements = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "listContent"))).find_elements(By.TAG_NAME, "li")
                    li_elements_found = 1
                except Exception:
                    query_sent = 0
                    done_load_more = 0
                    li_elements = 0
                    print("li elements not found")
                    break

                for li in li_elements:
                    try:
                        link_element = li.find_element(By.TAG_NAME, "a")
                        href = link_element.get_attribute("href")
                        if href not in href_links:
                            href_links.append(href)
                            print(href)
                    except Exception as e:
                        if 'captcha' in driver.current_url:
                            captchaon(driver.current_url)
                print(f"done gathering business links for {query}")
                break
            if li_elements_found == 0:
                continue
            else:
                break

        # Gather data from each opened link
        if li_elements_found == 1:
            print("Gathering data")
            for link in href_links:
                while True:
                    try:
                        # Navigate to the link
                        driver.get(link)
                        for col in elements_to_scrape:
                            # Extract and store each element
                            savedata(col, data)
                        break

                    except Exception as e:
                        if 'captcha' in driver.current_url:
                            captchaon(driver.current_url)
                        print(f"exception {e}")
                        continue

            # Save the data to a CSV file with 'utf-8' encoding
            data_df = pd.DataFrame(data)
            data_df.to_csv('database.csv',mode = 'a', header=False, index=False, encoding='utf-8')
print("PROGRAM FINISHED")

