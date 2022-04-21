from msilib.schema import Error
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import os
import pickle
import pandas as pd

# enter path
PATH = 'Google/chromedriver.exe' 
driver = webdriver.Chrome(PATH)

google_search = 'apple sustainable' # search keywords
driver.get("https://www.google.com") # enter google website

# select search bar and search keywords
search = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='q']"))) 
time.sleep(1)
search.clear()
search.send_keys(google_search) #enter keywords
time.sleep(1)
search.send_keys(Keys.ENTER) # press enter

try:
    main = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "rso"))) #locate main page

    links = main.find_elements(By.CSS_SELECTOR, "div a") # find elements in website that has a link
    link = [i.get_attribute('href') for i in links] #collate url in a list
    print(link)
    content = [] 

    for i in range(len(link)):
        if link[i]!= None:
            try:
                driver.get(link[i]) # enter each link in list
                time.sleep(1)
                b = driver.find_elements(By.TAG_NAME, "p") #access each paragrahs of words
                for data in b:
                    content.append(data.text) #add data into content list
            except:
                driver.back()
                print(Error)
finally:
    driver.quit()

# Create directory named after search terms
try:
    os.makedirs(f"Google/{google_search}")
    print("Directory", google_search, "created")
except FileExistsError:
    print("Directory", google_search, "exists")

# save files into folders
pickle.dump(content, open("Google/%s/content.pkl" % google_search, "wb"))
pickle.dump(google_search, open("Google/search_word.pkl", "wb"))

df = pd.DataFrame(content, columns=['Data'])
df.to_csv(f"Google/{google_search}/data.csv", index=False)