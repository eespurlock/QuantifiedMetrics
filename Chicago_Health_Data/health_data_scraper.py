'''
Author: Esther Edith Spurlock

Scrapes Chicago public health data

I got help on this using:
http://stanford.edu/~mgorkove/cgi-bin/rpython_tutorials/Scraping_a_Webpage_Rendered_by_Javascript_Using_Python.php
https://stackoverflow.com/questions/510348/how-can-i-make-a-time-delay-in-python
https://stackoverflow.com/questions/20244691/python-selenium-how-do-i-find-all-element-ids-on-a-page
https://stackoverflow.com/questions/7713797/how-to-get-css-class-name-using-selenium

Need to figure out:
Child Opportunity Index
Economic Hardship
'''
#imports
import pandas as pd
import bs4
import time
from selenium import webdriver
import gc

data_dict = {'community name': []} #dictionary we will fill in

#This is the pathway to ChromeDriver on my machine. You will need to update this path to match where ChromeDriver is on your machine
chrome_path = 'C:/Users/eespu/AppData/Local/Programs/Python/Python37/Lib/site-packages/selenium/webdriver/chrome/chromedriver'

starting_url = 'https://www.chicagohealthatlas.org/community-areas' #URL with links to community area pages

def go(url=starting_url):
    '''
    Goes from beginning to end of web scraper
    
    Inputs: the beginning website you want to use
    '''
    soup = create_soup(url, False)
    url_lst = find_links(soup) #gets the list of urls of the community pages
    default = []
    for index, url in enumerate(url_lst):
        scrape_page(url, default) #scrapes the community's page
        for key, lst in data_dict.items(): #makes sure that all data is filled in
            if len(lst) < index + 1:
                data_dict[key].append('Not Listed')
        default.append('Not Listed') #generates list to make sure all previous data is filled in if a new metric appears on a later page
    
    df = pd.DataFrame(data=data_dict) #creates a pandas dataframe from the dictionary
    df.to_csv('chicago_health_data.csv') #turns our pandas dataframe into a csv
    
    delete_lst([soup, df, url_lst, url, default, key, lst])
    gc.collect()
    
def scrape_page(url, default):
    '''
    Scrapes a single page for its health data
    
    Inputs: 
    url: the url for a community page
    default: the default list for a newly-created dictionary item
    '''
    soup = create_soup(url, True)

    community_name = soup.find('h1', class_="t-main-title") #finds the community name
    if community_name is None: #checks if there is data on the page
        return None
    community_name = community_name.get_text()
    data_dict['community name'].append(community_name)
    
    for table in soup.find_all('div', class_="c-panel__content"): #finds all the tables on the page
        col_names = []
        year = 1
        for column in table.find_all('th', class_="c-table__cell"): #finds all the column names
            col_n = column.get_text()
            if col_n == community_name:
                col_n = "Community" #puts all of the community information into one column instead of different columns for every community
            if col_n == "Year":
                col_n = col_n + str(year) #differentiates between the two different year columns
                year += 1
            col_names.append(col_n)
        col_names = col_names[1:] #takes out the first entry in col_names because the first column has no data in it

        for row in table.find_all('tr'): #the section with the information we want
            count = -1
            specific_names = []
            for cell in row.find_all('td', class_="c-table__cell"): #finds all the row names and the data
                text = cell.get_text()
                if count < 0:
                    for name in col_names: #creates the names for the dictionary fields
                        specific_names.append(name + " " + text)
                else:
                    col = specific_names[count] #the name of the column will have the same index as the count
                    col_lst = data_dict.get(col, default[:]) #gets the current dictionary list, if there is no list, gives us the default values
                    col_lst.append(text) #adds the data to the list
                    data_dict[col] = col_lst #sets the dictionary value
                count += 1

    delete_lst([soup, community_name, table, column, col_n, col_names, row, count, specific_names, cell, text, col, col_lst])


def find_links(soup):
    '''
    Finds the links to all urls
    
    Inputs: a BeautifulSoup object
    '''
    url_lst = []
    for instance in soup.find_all('a', class_='c-simple-list__link'):
        end_url = instance['href'] #gets the last part of the url
        url_lst.append('https://www.chicagohealthatlas.org/' + end_url) #creates the whole url
    delete_lst([instance, end_url])
    return url_lst

def create_soup(url, expand):
    '''
    Creates a BeautifulSoup object of the CPS all schools list
    
    Inputs: 
        url: the url you want to scrape
        expand: if there are sections in the web page that need expanding: True for community pages, false for the first page with links to community pages
    
    Returns: a BeautifulSoup object
    '''
    browser = webdriver.Chrome(chrome_path) #create a web driver
    browser.get(url) #loads the website onto the driver
    time.sleep(2) #waits 2 seconds for the page to load
    if expand:
        aria = browser.find_elements_by_xpath('//*[@aria-hidden]') #finds all the sections that need expanded
        for a in aria:
            if a.get_attribute('class') == 'fa fa-caret-down txt-color-charade':
                a.click() #clicks on the portion that needs expanded
                time.sleep(2) #waits 2 seconds for table to load
    htmlSource = browser.page_source #gets the page source from the web page
    del browser

    return bs4.BeautifulSoup(htmlSource, features="html.parser") #returns a BeautifulSoup object

def delete_lst(del_lst):
    '''
    deletes a list of objects
    
    inputs: a list of objects to be deleted
    '''
    for item in del_lst:
        del item

go()
print('Complete')
