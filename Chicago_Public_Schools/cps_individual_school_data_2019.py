'''
Author: Esther Edith Spurlock

Scrapes data about individual school from the CPS website 

This web scraper was created in the summer of 2019 and may need to be updated if CPS changes their website

Downloaded data:
    School name
    School address
    School phone number
    Grade range
    Number of students
    School rating
    School Prefix
    School website
    School type
    Faculty
    Hours
    Public transit
    Kindergarten status
    Bilingual Services
    Classroom Languages
    Dress Code status
    Attendance Boundaries
    Refugee Services
    Title I Eligibility
    % Asian/Black/Hispanic/White/Other
    % Low Income/Diverse Learners/Limited English/Mobility Rate/Chronic Truancy
    Student Growth Description
    Student Attainment Description
    Culture and Climate Description
    NWEA Reading/Math Growth
    Reading/Math Growth/Attainmnet by grade
    Involved Families Level
    Ambitious Instruction Level
    Supportive Environment Level
    Effective Leaders Level
    Collaborative Teachers Level
    School Community Level
    Parent Teacher Partnership Level
    Quality of Facilities
    Safety
    Number/length of suspensions across 2 years and average
    Miscounduct across 2 years and average
    Student/teacher attendance across 2 years and average

Data I have chosen to exclude:
    Grade category
    Which L train the children use (if they use one)
    If the school is a Go CPS participant
    If the school has more than 2 faculty listed
    If the schools use public transportation methods other than Bus, Train, and Metra
    If the school is part of Healthy CPS
    If the school has its Creative Schools Certification
    If the school is part of Supportive Schools
    Survey Response rates
    Data from the following tabs:
        Admissions
        Programs
        Downloads
'''
#Downloads needed for this section of the code
import scraping_helper_functions as shf

def scrape_page(url, data):
    '''
    Scrapes a single page for data about a school
    
    Inputs: 
        url: url of the page we want to scrape
        data: a dictionary with the information we want to add to
    '''
    soup = shf.create_soup(url) #creates BeautifulSoup object from url
    get_bar_chart_data(soup, data) #gets data stored in a bar chart on the school's page
    get_span_data(soup, data) #gets data stored in span tags
    data['Website'].append(get_a_data(soup)) #gets data stored in a tags (just the website)

    shf.delete_lst([soup])

def get_bar_chart_data(soup, data):
    '''
    Gets data stored in bar charts, this includes:
        % Asian
        % Black
        % Hispanic
        % White
        % Other
        % Low Income
        % Diverse Learners
        % Limited English
        % Mobility Rate
        % Chronic Truancy
        NWEA Reading/Math Growth
        Reading/Math Growth/Attainmnet by grade
    
    Inputs:
        soup: a BeautifulSoup object
        data: a dictionary we will add to
    '''
    #Initializes the dictionary which stores which prefixes we will use
    prefix_dict = {"ctl00_ContentPlaceHolder1_pnlDemographicsChart": [''],\
        "ctl00_ContentPlaceHolder1_pnlStatisticsChart": [''],\
        "ctl00_ContentPlaceHolder1_liElementarySchoolCharts": [''],\
        "ctl00_ContentPlaceHolder1_pnlGrowthES": ['Reading Growth ', 'Math Growth '], \
        "ctl00_ContentPlaceHolder1_pnlAttainES": ['Reading Attainment ', 'Math Attainment ']}
    
    #Searches for div tags who have the listed ids
    for instance in soup.find_all(['div'], id=["ctl00_ContentPlaceHolder1_pnlDemographicsChart",\
        "ctl00_ContentPlaceHolder1_pnlStatisticsChart","ctl00_ContentPlaceHolder1_liElementarySchoolCharts",\
        "ctl00_ContentPlaceHolder1_pnlGrowthES", "ctl00_ContentPlaceHolder1_pnlAttainES"]):
        
        i = 0 #an index which will only be used to ensure we are using the appropriate prefix
        prefix_lst = prefix_dict[instance['id']]

        pct_lst = [] #holds the numbers we scrape
        key_lst = [] #holds the names of the columns we want the numbers to map to in the data dictionary
        
        #Searches for span tags who have the listed ids, this will give us the percents/percentiles
        for percent in instance.find_all(['span'], class_=["value" ,"value bold", "value bold value-behind"]):
            per = percent.get_text().strip()
            pct_lst.append(per)
        
        #Searches for div tags who have the listed ids, this will give us the columns names
        for demographic in instance.find_all(['div'], class_=["bar-lefttext","panel-body text-bold grey-darkest"]):
            key = demographic.get_text().strip('\n?').strip()
            if key.endswith('percentile'): #formats the name in a way we like
                key = key[:21].strip()
            key_lst.append(prefix_lst[i] + key)
            if key == 'All': #'All' comes at the end of a bar chart and we then need to use a different prefix
                i += 1

        for index, per in enumerate(pct_lst): #loops through the percent list with its index
            key = key_lst[index] #the appropriate key will have the same index as the percent
            data[key].append(per) #add the data to the dictionary

    #shf.delete_lst([instance, percent, demographic, per, pct_lst, key_lst, key, prefix_dict, prefix_lst])

def get_a_data(soup):
    '''
    Gets the data that is held in a tags, this includes the school website
    
    Inputs: 
        soup: a BeautifulSoup object

    Returns:
       the school's website or 'Not Listed' if there is no data
    '''
    for instance in soup.find_all(['a'], id=['ctl00_ContentPlaceHolder1_lnkSchoolWebsite']):
                return instance.get_text()
    return 'Not Listed'

def get_span_data(soup, data):
    '''
    Gets the data that is held in span tags, this includes:
        School Name
        School Prefix
        School Address
        School Phone Number
        School Fax Number
        School Rating
        Rating Status
        Grade Range
        Number Of Students
        School Type
        School Administrator
        School Administrator Title
        Secondary Contact
        Secondary Contact Title
        Hours
        Earliest Dropoff Time
        Transit Empty
        Kindergarten Status
        Bilingual Services
        Classroom Languages
        Dress Code Status
        Attendance Boundaries
        Refugee Services
        Title 1 Eligible
        Student Growth Description
        Student Attainment Description
        Culture and Climate Description
        Involved Families Level
        Ambitious Instruction Level
        Supportive Environment Level
        Effective Leaders Level
        Collaborative Teachers Level
        School Community Level
        Parent Teacher Partnership Level
        Quality of Facilities
        Safety
        Number/length of suspensions across 2 years and average
        Miscounduct across 2 years and average
        Student/teacher attendance across 2 years and average
    
    Inputs: 
        soup: a BeautifulSoup object
        data: a dictionary we will add to
    '''
    transit_options = ''
    for instance in soup.find_all(['span']): #searches for all span tags
        if instance.has_attr('id'): #we only want elements with ids
            inst_id = instance['id']
            #We only want instances where the id begins with the listed string
            if inst_id.startswith('ctl00_ContentPlaceHolder1_lb'):
                end_id = inst_id[28:] #the identifying part of the id comes after the beginning of the string listed above
                if end_id == 'OfficialSchoolName': #We need to pull two things out of the text under this id
                    prefix = 'None'
                    name = instance.get_text()
                    if ' - ' in name:
                        prefix, name = name.split(' - ',  1) #splits the name into two parts
                    data['School Prefix'].append(prefix)
                    data[end_id].append(name)
                elif end_id in data: #puts the data in the dictionary if the key is in the dictionary
                    data[end_id].append(instance.get_text())
                elif end_id in ['lTransitEmpty', 'Train', 'Bus', 'Metra']: #puts all transit options in a string
                    transit_options += instance.get_text() + ', '

    data['Transit'].append(transit_options[:-2]) #puts all transit options into the data dictionary without the extra comma at the end
    #shf.delete_lst([inst_id, end_id, instance, prefix, name])
