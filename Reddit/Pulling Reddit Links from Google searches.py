import click
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from re import sub
import praw
from praw.models import MoreComments
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize


posts= []
PATH="C:/Users/stjia/Downloads/chromedriver_win32/chromedriver.exe"
search_term="Mood Lamp Review"

num_of_pages=10            #what page to scrap until



def Reddit_Scraper():                                                   #uses praw library to 
    reddit = praw.Reddit(client_id="Q98C0PiBG2Dx7L2JfzqpCQ",        
    client_secret= "QberX4-WWcAcsu8HVX8N6l9a_H1GDQ",
    user_agent = "Dyson Airwrap Scraper")

    submission_list=[]

    for url in link: 
        comment_string = "/comments"
        if comment_string in url: 
            submission= reddit.submission(url=url)
            submission_list.append(submission)


    for submissions in submission_list:
        submissions.comments.replace_more(limit=None)

    for submissions in submission_list:
        for comments in submissions.comments.list():
            posts.append(comments.body)







driver = webdriver.Chrome(PATH)

driver.get("https://www.google.com/")


search= driver.find_element_by_name("q")
search.send_keys("site:reddit.com " + search_term)
search.send_keys(Keys.RETURN)

try:
    
    for x in range(2, num_of_pages+1): 
        
        main = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, "search")))
        links = main.find_elements(By.CSS_SELECTOR, "div.yuRUbf > a")
        link = [i.get_attribute('href') for i in links]

        Reddit_Scraper()


        main2= WebDriverWait(driver,10).until(EC.presence_of_element_located((By.LINK_TEXT, str(x))))
        main2.click()
        

    df = pd.DataFrame(posts)

    df.to_csv('Mood_lamp_all_comments.csv')

finally:
    time.sleep(5)
    driver.quit()













