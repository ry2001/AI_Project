from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import praw
import pandas as pd
import pickle

posts = []
PATH = "Reddit/chromedriver.exe"
search_term = "Apple Watch"                                             # enter the search term

num_of_pages = 3                                                       # what page to scrap until

def Reddit_Scraper():                                                   # uses praw library to scrape reddit
    reddit = praw.Reddit(client_id = "CLIENT_ID",                       # users need to enter their own client id
    client_secret = "CLIENT_SECRET",                                    # users need to enter their own client secret
    user_agent = "USER_AGENT")                                          # users need to enter their own user agent

    submission_list = []

    for url in link: 
        comment_string = "/comments"
        if comment_string in url: 
            submission= reddit.submission(url = url)
            submission_list.append(submission)

    for submissions in submission_list:
        submissions.comments.replace_more(limit = None)

    for submissions in submission_list:
        for comments in submissions.comments.list():
            posts.append(comments.body)

driver = webdriver.Chrome(PATH)
driver.get("https://www.google.com/")

search = driver.find_element_by_name("q")
search.send_keys(f"site:reddit.com {search_term} Reviews")
search.send_keys(Keys.RETURN)

try:
    for x in range(2, num_of_pages + 1): 
        main = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "search")))
        links = main.find_elements(By.CSS_SELECTOR, "div.yuRUbf > a")
        link = [i.get_attribute('href') for i in links]

        Reddit_Scraper()

        main2 = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.LINK_TEXT, str(x))))
        main2.click()

    df = pd.DataFrame(posts)
    df.columns = ['comments']
    df.to_csv(f'Reddit/{search_term}_all_comments.csv')

finally:
    time.sleep(5)
    driver.quit()

pickle.dump(search_term, open("Reddit/search_term.pkl", "wb"))











