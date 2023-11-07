import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import time
import subprocess


# Read categoriesss and cities from text files with 'utf-8' encoding
with open('categoriesss', 'r', encoding='utf-8') as category_file:
    categories = category_file.read().splitlines()

with open('cities.txt', 'r', encoding='utf-8') as city_file:
    cities = city_file.read().splitlines()

# Define the elements you want to scrape and their corresponding column names
elements_to_scrape = [
    'Category','City','Title', 'Rating', 'TimesRated', 'Address', 'Phone', 'Instagram'
]


# Create an empty dictionary to store the data
data = {col: [] for col in elements_to_scrape}

#setting up the driver source(it will always in sync with and current chrome version) + removing image loading
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--blink-settings=imagesEnabled=false')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')



## Add Options to Webdriver
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
captchadriver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://easy.co.il/list/Hair-Design")


# scripts to play music and pause music from spotify, its for a notification about a captcha.
playscript_path = 'subscripts/playscript.scpt'
pausescript_path = 'subscripts/pausescript.scpt'



def captchaon(url):
    print("captcha***********")
    captchadriver.get(url)
    captchadriverurl = captchadriver.current_url
    subprocess.call(['osascript', playscript_path])
    while "captcha" in captchadriverurl:
        time.sleep(5)
        captchadriverurl = captchadriver.current_url
    subprocess.call(['osascript', pausescript_path])
    time.sleep(5)
    driver.get(captchadriverurl)
    return


# Iterate through each category and city combination
for category in categories:
    for city in cities:
        # Define the search query
        query = f"{category} {city}"
        print(query)
        # Send the search terms
        driver.get("https://easy.co.il/list/Hair-Design")
        search_input = driver.find_element(By.ID, "SearchInputBiz")
        search_input.send_keys(query)
        search_input.send_keys(Keys.RETURN)
        current_url = driver.current_url
        if 'captcha' in current_url:
            captchaon(current_url)
        # Wait for the search results to load (you can use WebDriverWait for this)
        while True:
            # Click the "Load More" button if it exists
            try :
                load_more_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "next-page-button")))
                load_more_button.click()
                print("pressed next page")
                current_url = driver.current_url
                if 'captcha' in current_url:
                    captchaon(current_url)
            except Exception as e:
                # Handle other exceptions
                print(f"no more load more buttons")
                current_url = driver.current_url
                if 'captcha' in current_url:
                    captchaon(current_url)
                break


        # Collect href links from the <li> element
        current_url = driver.current_url
        if 'captcha' in current_url:
            captchaon(current_url)
        print(current_url)
        print(driver.find_element(By.CLASS_NAME,"list-results"))
        #print(driver.find_element(By.XPATH, "//*[@id='listContent']/div/div/ul"))
        #print(driver.find_element(By.XPATH, "/ html / body / div / div / div / div[1] / div[2] / div[3] / div / main / div"))
        perentofli = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, "list-results")))  # Modify the XPath as needed
        li_elements = perentofli.find_elements(By.TAG_NAME, "li")
        print(li_elements)
        href_links = []
        for li in li_elements:
            try:
                link_element = li.find_element(By.TAG_NAME, "a")
                href = link_element.get_attribute("href")
                if href not in href_links:
                    href_links.append(href)
                    print(href)

            except Exception:
                # Handle the case where the <li> element doesn't contain a link
                continue


        # Gather data from each opened link
        for href in href_links:
            # Navigate to the link
            driver.get(href)
            current_url = driver.current_url
            if 'captcha' in current_url:
                captchaon(current_url)
            for col in elements_to_scrape:
                    # Extract and store each element
                    #we have 6 dynamic info sources. if none of them exists, its not a page of a business, its a captcha.
                if col == 'Title':
                    try:
                        title_element = WebDriverWait(driver, 0.2).until(EC.presence_of_element_located((By.CLASS_NAME, "biz-title")))
                        title = title_element.text
                        print(title)
                    except Exception as e:
                        title = None
                    data['Title'].append(title)
                elif col == 'Rating':
                    try:
                        rating_element = WebDriverWait(driver, 0.2).until(EC.presence_of_element_located((By.XPATH,"//*[@id='app']/div[2]/main/div/div/div[1]/div[1]/div[1]/div[2]/div/span")))
                        rating = rating_element.text
                        print(rating)
                    except Exception as e:
                        # Handle other exceptions
                        rating = None
                    data['Rating'].append(rating)

                elif col == 'TimesRated':
                    try:
                        times_rated_element = WebDriverWait(driver, 0.2).until(EC.presence_of_element_located((By.ID, "headerItemReviewBox")))
                        times_rated = times_rated_element.text
                        print(times_rated)
                    except Exception as e:
                        # Handle other exceptions
                        times_rated = None
                    data['TimesRated'].append(times_rated)

                elif col == 'Address':
                    try:
                        address_element = WebDriverWait(driver, 0.2).until(EC.presence_of_element_located((By.CLASS_NAME, "biz-address-text")))
                        address = address_element.text
                        print(address)
                    except Exception as e:
                        address = None
                    data['Address'].append(address)

                elif col == 'Phone':
                    try:
                        phone_element = WebDriverWait(driver, 0.2).until(EC.presence_of_element_located((By.ID, "action-phone-label")))
                        phone = phone_element.text
                        print(phone)

                    except Exception as e:
                        phone = None
                    data['Phone'].append(phone)


                elif col == 'Instagram':
                    try:
                        instagram_element = WebDriverWait(driver, 0.2).until(EC.presence_of_element_located((By.CLASS_NAME, "biz-action-button.instagram")))
                        a_element = instagram_element.find_element(By.TAG_NAME, "a")
                        instagram = a_element.get_attribute("href")
                        print(instagram)
                    except Exception as e:
                        # Handle other exceptions
                        instagram = None
                    data['Instagram'].append(instagram)

                elif col == 'City':
                    data['City'].append(city)
                    print(city)
                elif col == 'Category':
                    data['Category'].append(category)
                    print(category)

        data_df = pd.DataFrame(data)
        # Save the data to a CSV file with 'utf-8' encoding
        data_df.to_csv('search_results.csv', mode='a', header=False, index=False, encoding='utf-8')

