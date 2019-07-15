'''
Author: Esther Edith Spurlock

Helper functions to help with scraping data from the web
'''
#Downloads needed for this section of the code
import bs4
from selenium import webdriver
import requests
import sys
import gc

#This is the pathway to ChromeDriver on my machine. You will need to update this path to match where ChromeDriver is on your machine
chrome_path = 'C:/Users/eespu/AppData/Local/Programs/Python/Python37/Lib/site-packages/selenium/webdriver/chrome/chromedriver'
#The URL that points to the first page with the list of schools
#This URL worked as of summer 2019. It may have to be changed
starting_url = 'https://schoolinfo.cps.edu/schoolprofile/SearchResults.aspx'
        
def create_soup(url):
    '''
    Creates a BeautifulSoup object of the CPS all schools list
    
    Inputs: the url you want to scrape
    
    Returns: a BeautifulSoup object
    '''
    req = requests.get(url) #Creating the request object
    if req:
        req_en = req.text.encode('iso-8859-1', 'ignore') #Encode the request object
    else:
        sys.exit("Not a valid request object")
    
    soup = bs4.BeautifulSoup(req_en, features="html.parser") #Turning the request object into a BeautifulSoup object

    if soup:
        delete_lst([req, req_en]) #Deleting references to objects we do not need
        return soup
    else:
        del soup
        sys.exit("Not a valid soup object")

def delete_lst(del_lst):
    '''
    deletes a list of objects
    
    inputs: a list of objects to be deleted
    '''
    for item in del_lst:
        del item

def loop_through_pages():
    '''
    loops through all the pages of the CPS website to collect all individual school's url
    
    Inputs: 
        chrome_path: the pathway to get to chrome on your machine
        url: the url to the CPS website
    
    Returns: url_lst: a list of individual school urls
    '''
    browser = webdriver.Chrome(chrome_path) #create a web driver
    browser.get(starting_url) #loads the CPS website onto the driver
    #the beginning string of the xpath for the different pages
    x_path_origin = '//*[@id="ctl00_ContentPlaceHolder1_gvSchoolSearchResults"]/tbody/tr[1]/td/table/tbody/tr/td'
    
    url_lst = []     
    #These dictionaries are specific to the way the CPS website was set up in 2019
    start_dict = {0:1, 1:4, 2:5}
    end_dict = {0:7, 1:9, 2:8}

    for i in range(3): #as of 2019, there are 3 sets of pages we need to loop through
        start = start_dict[i] #for each set of pages, we need to start and end at different xpaths to avoid errors and duplicates
        end = end_dict[i]
        for page in range(start,end):
            x_path = x_path_origin + ('[%s]'%str(page))#finishes creating the xpath to look for
            browser.find_element_by_xpath(x_path).click()#clicks on the xpath
            soup = bs4.BeautifulSoup(browser.page_source, features="html.parser")#create a beautiful soup object
            get_urls(soup, url_lst)#gets the urls from a specific page

    browser.close()#close browser
    delete_lst([browser, soup, x_path, x_path_origin, page, i, start, end, end_dict])
    return url_lst

def get_urls(soup, url_lst):
    '''
    Finds the urls to link to the different schools and updates url_lst
    
    Inputs: 
        soup: a BeautifulSoup object
        url_lst: a list of school urls we have already found
    '''
    #This is the beginning to every url with individual school information
    #This is the prefix as of summer 2019
    prefix = 'https://schoolinfo.cps.edu/schoolprofile/'
    
    for instance in soup.find_all(['a']): #Loop through all the instances of tag "a"
        if instance.has_attr('href'):
            end_url = instance['href']
            if end_url.startswith("SchoolDetails.aspx?SchoolId="): #Checks that this is a url to an individual school
                url_lst.append(prefix + end_url)

    delete_lst([instance, end_url])
