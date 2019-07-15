'''
Author: Esther Edith Spurlock

Scrapes data about all schools from the CPS website 

This web scraper was created in the summer of 2019 and may need to be updated if CPS changes their website
'''
#Downloads needed for this section of the code
import pandas as pd
import gc
import scraping_helper_functions as shf
from cps_individual_school_data_2019 import scrape_page

#Initializes the dictionary we will use to store data
data = {'School ID': [],
        'OfficialSchoolName': [],
        'School Prefix': [],
        'Address': [],
        'lPhone': [], 
        'lFax': [],
        'Website': [],
        'OverallRating': [],
        'RatingStatus': [],
        'SchoolGradeText': [],
        'NumberOfStudents': [],
        'SchoolType': [],
        'SchoolAdministrator': [],
        'SchoolAdministratorTitle': [],
        'SecondaryContact': [],
        'SecondaryContactTitle': [],
        'Hours': [],
        'EarliestDropOffTime': [],
        'AfterSchoolHours': [],
        'Transit': [],
        'Kindergarten': [],
        'BilingualServices': [],
        'ClassroomLanguages': [],
        'Uniform': [],
        'AttendanceBoundaries': [],
        'RefugeeServices': [],
        'Title1Eligible': [],
        'Asian': [],
        'Black': [],
        'Hispanic': [],
        'White': [],
        'Other': [],
        'Low Income': [], 
        'Diverse Learners': [], 
        'Limited English': [], 
        'Mobility Rate': [], 
        'Chronic Truancy': [],
        'lStudentGrowth': [],
        'lStudentAttainment': [],
        'lCultureClimate': [],
        'NWEA Reading Growth': [],
        'NWEA Math Growth': [],
        'Reading Growth 3rd' : [],
        'Reading Growth 4th' : [],
        'Reading Growth 5th' : [],
        'Reading Growth 6th' : [],
        'Reading Growth 7th' : [],
        'Reading Growth 8th' : [],
        'Reading Growth All' : [],
        'Math Growth 3rd' : [],
        'Math Growth 4th': [],
        'Math Growth 5th' : [],
        'Math Growth 6th' : [],
        'Math Growth 7th' : [],
        'Math Growth 8th' : [],
        'Math Growth All' : [],
        'Reading Attainment 2nd' : [],
        'Reading Attainment 3rd' : [],
        'Reading Attainment 4th' : [],
        'Reading Attainment 5th' : [],
        'Reading Attainment 6th' : [],
        'Reading Attainment 7th' : [],
        'Reading Attainment 8th' : [],
        'Reading Attainment All' : [],
        'Math Attainment 2nd' : [],
        'Math Attainment 3rd' : [],
        'Math Attainment 4th' : [],
        'Math Attainment 5th' : [],
        'Math Attainment 6th' : [],
        'Math Attainment 7th' : [],
        'Math Attainment 8th' : [],
        'Math Attainment All' : [],
        'lInvolvedFamilies': [],
        'lAmbitiousInstruction': [],
        'lSupportiveEnvironment': [],
        'lEffectiveLeaders': [],
        'lCollaborativeTeachers': [],
        'lSchoolCommunity': [],
        'lParentTeacherPartnership': [],
        'lQualityofFacilities': [],
        'lSafety': [],
        'lSuspensionsYR1': [],
        'lSuspensionsYR2': [],
        'lSuspensionsAverage': [],
        'lMisconductsYR1': [],
        'lMisconductsYR2': [],
        'lMisconductsAverage': [],
        'lSuspensionLengthYR1': [],
        'lSuspensionLengthYR2': [],
        'lSuspensionLengthAverage': [],
        'lStudentAttendanceYR1': [],
        'lStudentAttendanceYR2': [],
        'lStudentAttendanceAverage': [],
        'lTeacherAttendanceYR1': [],
        'lTeacherAttendanceYR2': [],
        'lTeacherAttendanceAverage': []}

#This creates the dictionary to change column titles after we have created a pandas dataframe with all of our data
rename_dict = {'OfficialSchoolName': 'School Name',
        'lPhone': 'School Phone Number', 
        'lFax': 'School Fax Number',
        'OverallRating': 'Overall Rating',
        'RatingStatus': 'Rating Status',
        'SchoolGradeText': 'Grade Levels Served',
        'NumberOfStudents': 'Number of Students',
        'SchoolType': 'School Type',
        'SchoolAdministrator': 'Administrator',
        'SchoolAdministratorTitle': 'Administrator Title',
        'SecondaryContact': 'Secondary Contact',
        'SecondaryContactTitle': 'Secondary Contact Title',
        'EarliestDropOffTime': 'Earliest Dropoff Time',
        'AfterSchoolHours': 'After School Hours',
        'BilingualServices': 'Bilingual Services',
        'ClassroomLanguages': 'Classroom Languages',
        'Uniform': 'Dress Code',
        'AttendanceBoundaries': 'Attendance Boundaries',
        'RefugeeServices': 'Refugee Services',
        'Title1Eligible': 'Title 1 Eligible',
        'Asian': '% Asian',
        'Black': '% Black',
        'Hispanic': '% Hispanic',
        'White': '% White',
        'Other': '% Other',
        'Low Income': '% Low Income', 
        'Diverse Learners': '% Diverse Learners', 
        'Limited English': '% Limited English', 
        'Mobility Rate': '% Mobility Rate', 
        'Chronic Truancy': '% Chronic Truancy',
        'lStudentGrowth': 'Student Growth Percentile',
        'lStudentAttainment': 'Student Attainment Percentile',
        'lCultureClimate': 'Culture Climate',
        'lInvolvedFamilies': 'Involved Families',
        'lAmbitiousInstruction': 'Ambitious Instruction',
        'lSupportiveEnvironment': 'Supportive Environment',
        'lEffectiveLeaders': 'Effective Leaders',
        'lCollaborativeTeachers': 'Collaborative Teachers',
        'lSchoolCommunity': 'School Community',
        'lParentTeacherPartnership': 'Parent Teacher Partnership',
        'lQualityofFacilities': 'Quality of Facilities',
        'lSafety': 'Safety',
        'lSuspensionsAverage': '# Suspensions on Average',
        'lMisconductsAverage': '# Misconducts on Average',
        'lSuspensionLengthAverage': 'Length Suspensions on Average',
        'lStudentAttendanceAverage': 'Student Attendance on Average',
        'lTeacherAttendanceAverage': 'Teacher Attendance on Average'}

def go(year):
    '''
    Crawls through the initial CPS webpage to gather the URLs to scrape and then calls functions to scrape CPS data
    
    Inputs: year: the current year as a string
    '''
    url_lst = shf.loop_through_pages()
    for index, url in enumerate(url_lst):
        print(index)
        data['School ID'].append(url[-6:])  #we get the school ID from the url
        cur_len = len(data['School ID'])
        scrape_page(url, data) #scrapes the individual school's page
        for key, lst in data.items(): #makes sure that all data is filled in
            if len(lst) < cur_len:
                data[key].append('Not Listed')

    df = pd.DataFrame(data=data) #Creates a dataframe with our object
    change_rename_dict(year) #updates the rename dictionary to incorporate the appropriate years
    df.rename(columns=rename_dict, inplace=True)
    df.to_csv('cps_data_' + year +'.csv')
    
    shf.delete_lst([df, url_lst, year, url]) #Deleting references to objects we do not need

def change_rename_dict(year):
    '''
    Makes adjustments to the rename_dict so it uses the appropriate years
    
    Inputs: year: the surrent year as a string
    '''
    clean_year = {'YR1': str(int(year) - 2), 'YR2': str(int(year) - 1)}
    clean_label = {'Suspensions': '# Suspensions ', 'Misconducts': '# Misconducts ',
        'SuspensionLength': 'Length Suspensions ', 'StudentAttendance': 'Student Attendance ',
        'TeacherAttendance': 'Teacher Attendance '}
    
    for y in ['YR1', 'YR2']:
        for label in ['Suspensions', 'Misconducts', 'SuspensionLength', 'StudentAttendance', 'TeacherAttendance']:
            rename_dict['l'+label+y] = clean_label[label] + clean_year[y]
    
    shf.delete_lst([y, label, clean_year, clean_label])

go(year='2019')
gc.collect() #Collects the garbage
print('Complete')
