'''
Author: Esther Edith Spurlock

Purpose: download data from the census using an API

Not all of the data fit into one csv, so this will split to data into 11 csvs

I downloaded 385 variables, these include:

Total_Population
Number male and female
Age breakdown by sex
Number white, black, indegenous, asian, Pacific islander, other race, and multiracial
Number Hispanic/Latinx and not Hispanic/Latinx
Citizenship status
Transportation to work
Time someone leaves home to go to work
Time it takes someone to get to work
Number of babies born in last 12 months
Number enrolled in school and which year
Highest level of education reached for those not in school
Number above/below poverty level
Total household income
Receiving Food Stams/SNAP, social security, supplimental social security, or public assistance
Number of veterans and non-veterans
Number with a service disability
Employment status
Type of employment by sex
Number of housing units in tract, if those units are occupied/who occupies them or vacant/why they are vacant
Number of residents who rent or own
Median number of rooms in housing unit for tract and median rent by number of rooms and median rent
Number of housing units with a mortgage
Median cost to an owner with a mortgage and the median cost to an owner without a mortgage
Median housing costs
Family type and family type by household size
Marrital status
Disability status by sex and age
Health insurance status by sex and age and number on public vs private insurance

I received help on this code from documentation from the CensusData pacage documentation
https://jtleider.github.io/censusdata/example1.html

This data comes from the ACS 5-year estimate

The variables come from here:
https://api.census.gov/data/2017/acs/acs1/variables.html
'''
#importing packages
import pandas as pd
import censusdata
import gc
import re
from unittest.mock import inplace

#I took this directly from the CensusData pacage documentation. It makes sure you can see all data in a dataframe if you print out the dataframe
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.precision', 2)

#This dictionary is used so we have descriptive names for our columns
rename_dict = {'B01001_001E': 'Total_Population', 'B01001_002E': 'Male', 'B01001_026E': 'Female', 'B02001_002E': 'White',
    'B02001_003E': 'Black', 'B02001_004E': 'Indigenous', 'B02001_005E': 'Asian', 'B02001_006E': 'Pacific_Islander',
    'B02001_007E': 'Other_Race', 'B02001_008E': 'Multiracial', 'B03001_002E': 'Not_Hispanic_Latino', 'B03001_003E': 'Hispanic_latino',
    'B05001_002E': 'Citizen_Born_in_US', 'B05001_003E': 'Citizen_Born_in_Territory', 'B05001_004E': 'Citizen_Born_Abroad_US_Parets',
    'B05001_005E': 'Citizen_Naturalized', 'B05001_006E': 'Not_Citizen', 'B08006_003E': 'Drive_to_Work_Alone', 'B08006_004E': 'Carpool_to_Work',
    'B08006_008E': 'Public_Transport_to_Work', 'B08006_014E': 'Bicycle_to_Work', 'B08006_015E': 'Walk_to_Work',
    'B08006_016E': 'Other_Transport_to_Work', 'B08006_017E': 'Work_From_Home', 'B08302_002E': 'Leave_Home12-5am', 'B08302_003E': 'Leave_Home5-5:30am',
    'B08302_004E': 'Leave_Home5:30-6am', 'B08302_005E': 'Leave_Home6-6:30am', 'B08302_006E': 'Leave_Home6:30-7am', 'B08302_007E': 'Leave_Home7-7:30_am',
    'B08302_008E': 'Leave_Home7:30-8am', 'B08302_009E': 'Leave_Home8-8:30am', 'B08302_010E': 'Leave_Home8:30-9am', 'B08302_011E': 'Leave_Home9-10am',
    'B08302_012E': 'Leave_Home10-11am', 'B08302_013E': 'Leave_Home11am-12pm', 'B08302_014E': 'Leave_Home12-4pm', 'B08302_015E': 'Leave_Home4pm-12am',
    'B08303_002E': '<5min_to_Work', 'B08303_003E': '5-9min_to_Work', 'B08303_004E': '10-14min_to_Work', 'B08303_005E': '15-19min_to_Work',
    'B08303_006E': '20-24min_to_Work', 'B08303_007E': '25-29min_to_Work', 'B08303_008E': '30-34min_to_Work', 'B08303_009E': '35-39min_to_Work',
    'B08303_010E': '40-44min_to_Work', 'B08303_011E': '45-59min_to_Work', 'B08303_012E': '60-89min_to_Work', 'B08303_013E': '>=90min_to_Work',
    'B13016_002E': 'Had_Baby_Last_Year', 'B14001_002E': 'Enrolled_School', 'B14001_003E': 'Nursery_Preschool', 'B14001_004E': 'Kindergarten', 'B14001_005E': 'Grade_1-4',
    'B14001_006E': 'Grade_5-8', 'B14001_007E': 'Grade_9-12', 'B14001_008E': 'Undergraduate', 'B14001_009E': 'Graduate_Professional_School', 'B14001_010E': 'Not_in_School',
    'B15003_002E': 'No_Schooling_Complete', 'B15003_003E': 'Nursery_School_Only', 'B15003_004E': 'Kindergarted_Only', 'B15003_005E': '1st_Grade_Only',
    'B15003_006E': '2nd_Grade_Only', 'B15003_007E': '3rd_Grade_Only', 'B15003_008E': '4th_Grade_Only', 'B15003_009E': '5th_Grade_Only',
    'B15003_010E': '6th_Grade_Only', 'B15003_011E': '7th_Grade_Only', 'B15003_012E': '8th_Grade_Only', 'B15003_013E': '9th_Grade_Only',
    'B15003_014E': '10th_Grade_Only', 'B15003_015E': '11th_Grade_Only', 'B15003_016E': '12th_Grade_No_Diploma', 'B15003_017E': 'HS_Diploma',
    'B15003_018E': 'GED_or_Alternative_Credential', 'B15003_019E': '<1yr_College', 'B15003_020E': '1+yr_College_No_Degree', 'B15003_021E': 'Associate_Degree',
    'B15003_022E': 'Bachelor_Degree', 'B15003_023E': 'Master_Degree', 'B15003_024E': 'Professional_Degree', 'B15003_025E': 'Doctorate',
    'B17001_002E': 'Below_Poverty_Level', 'B17001_031E': 'Above_Poverty_Level', 'B19001_002E': '<$10k_Household_Income', 'B19001_003E': '$10-15k_Household_Income',
    'B19001_004E': '$15-20k_Household_Income', 'B19001_005E': '$20-25k_Household_Income', 'B19001_006E': '$25-30k_Household_Income', 'B19001_007E': '$30-35k_Household_Income',
    'B19001_008E': '$35-40k_Household_Income', 'B19001_009E': '$40-45k_Household_Income', 'B19001_010E': '$45-50k_Household_Income', 'B19001_011E': '$50-60k_Household_Income',
    'B19001_012E': '$60-75k_Household_Income', 'B19001_013E': '$75-100k_Household_Income', 'B19001_014E': '$100-125k_Household_Income',
    'B19001_015E': '$125-150k_Household_Income', 'B19001_016E': '$150-200k_Household_Income', 'B19001_017E': '>=$200k_Household_Income',
    'B19058_002E': 'Food_Stamps_SNAP', 'B19058_003E': 'No_Food_Stamps_SNAP', 'B19059_002E': 'Retirement_Income', 'B19059_003E': 'No_Retirement_Income',
    'B21001_002E': 'Veteran', 'B21001_003E': 'Non-Veteran', 'B21100_003E': 'Service_Disability', 'B23025_004E': 'Employed_Civilian',
    'B23025_005E': 'Unemployed_Civilian', 'B23025_006E': 'Armed_Forces', 'B23025_007E': 'Not_in_labor_Force', 'B25001_001E': 'Total_Housing_Units',
    'B25002_002E': 'Occupied_Units', 'B25002_003E': 'Vacant_Units', 'B25003_002E': 'Owner_Occupied', 'B25003_003E': 'Renter_Occupied', 'B25004_002E': 'Units_For_Rent',
    'B25004_003E': 'Units_Rented_Unoccupied', 'B25004_004E': 'Units_For_Sale', 'B25004_005E': 'Units_Sold_Unoccupied', 'B25004_006E': 'Occasional_Use_Units',
    'B25004_007E': 'Units_For_Migrant_Workers', 'B25004_008E': 'Vacant_Unit_Other_Reason', 'B25018_001E': 'Median_Num_Rooms', 'B25027_002E': 'Housing_Units_With_Mortgage',
    'B25031_001E': 'Median_Rent_by_Bedrooms', 'B25035_001E': 'Median_Year_Housing_Built', 'B25037_002E': 'Median_Year_Owner_Occupied_Built',
    'B25037_003E': 'Median_Year_Renter_Occupied_Built', 'B25064_001E': 'Median_Rent', 'B25088_002E': 'Median_Owner_Cost_Mortgage', 'B25088_003E': 'Median_Owner_Cost_No_Mortgage',
    'B25105_001E': 'Median_Housing_Costs', 'B19055_002E': 'Social_Security_Income', 'B19055_003E': 'No_Social_Security_Income', 'B19056_002E': 'Supplimental_Social_Security',
    'B19056_003E': 'No_Supplimental_Social_Security', 'B19057_002E': 'Public_Assistance_Income', 'B19057_003E': 'No_Public_Assistance_Income', 'B01001_003E': 'Male_<5',
    'B01001_004E': 'Male_5-9', 'B01001_005E': 'Male_10-14', 'B01001_006E': 'Male_15-17', 'B01001_007E': 'Male_18-19', 'B01001_008E': 'Male_20', 'B01001_009E': 'Male_21',
    'B01001_010E': 'Male_22-24', 'B01001_011E': 'Male_25-29', 'B01001_012E': 'Male_30-34', 'B01001_013E': 'Male_35-39', 'B01001_014E': 'Male_40-44', 'B01001_015E': 'Male_45-49',
    'B01001_016E': 'Male_50-54', 'B01001_017E': 'Male_55-59', 'B01001_018E': 'Male_60-61', 'B01001_019E': 'Male_62-64', 'B01001_020E': 'Male_65-66', 'B01001_021E': 'Male_67-69',
    'B01001_022E': 'Male_70-74', 'B01001_023E': 'Male_75-79', 'B01001_024E': 'Male_80-84', 'B01001_025E': 'Male_>=85', 'B01001_027E': 'Female_<5', 'B01001_028E': 'Female_5-9',
    'B01001_029E': 'Female_10-14', 'B01001_030E': 'Female_15-17', 'B01001_031E': 'Female_18-19', 'B01001_032E': 'Female_20', 'B01001_033E': 'Female_21', 'B01001_034E': 'Female_22-24',
    'B01001_035E': 'Female_25-29', 'B01001_036E': 'Female_30-34', 'B01001_037E': 'Female_35-39', 'B01001_038E': 'Female_40-44', 'B01001_039E': 'Female_45-49', 'B01001_040E': 'Female_50-54',
    'B01001_041E': 'Female_55-59', 'B01001_042E': 'Female_60-61', 'B01001_043E': 'Female_62-64', 'B01001_044E': 'Female_65-66', 'B01001_045E': 'Female_67-69', 'B01001_046E': 'Female_70-74',
    'B01001_047E': 'Female_75-79', 'B01001_048E': 'Female_80-84', 'B01001_049E': 'Female_>=85', 'B11001_003E': 'Married-couple_family', 'B11001_005E': 'Male_Householder_No_Spouse',
    'B11001_006E': 'Female_Householder_No_Spouse', 'B11001_008E': 'Householder_Living_Alone', 'B11001_009E': 'Householder_Not_Alone_No_Family', 'B12001_003E': 'Male_Never_Married',
    'B12001_004E': 'Male_Now_Married', 'B12001_005E': 'Male_Now_Married_Spouse_Present', 'B12001_006E': 'Male_Now_Married_Spouse_Absent', 'B12001_007E': 'Male_Now_Married_Spouse_Absent_Separated',
    'B12001_008E': 'Male_Now_Married_Spouse_Absent_Other', 'B12001_009E': 'Male_Widowed', 'B12001_010E': 'Male_Divorced', 'B12001_012E': 'Female_Never_Married', 'B12001_013E': 'Female_Now_Married',
    'B12001_014E': 'Female_Now_Married_Spouse_Present', 'B12001_015E': 'Female_Now_Married_Spouse_Absent', 'B12001_016E': 'Female_Now_Married_Spouse_Absent_Separated',
    'B12001_017E': 'Female_Now_Married_Spouse_Absent_Other', 'B12001_018E': 'Female_Widowed', 'B12001_019E': 'Female_Divorced', 'B11016_003E': 'Family_Household_2_Person_Household',
    'B11016_004E': 'Family_Household_3_Person_Household', 'B11016_005E': 'Family_Household_4_Person_Household', 'B11016_006E': 'Family_Household_5_Person_Household',
    'B11016_007E': 'Family_Household_6_Person_Household', 'B11016_008E': 'Family_Household_>=7_Person_Household', 'B11016_010E': 'NonFamily_Household_1_Person_Household',
    'B11016_011E': 'NonFamily_Household_2_Person_Household', 'B11016_012E': 'NonFamily_Household_3_Person_Household', 'B11016_013E': 'NonFamily_Household_4_Person_Household',
    'B11016_014E': 'NonFamily_Household_5_Person_Household', 'B11016_015E': 'NonFamily_Household_6_Person_Household', 'B11016_016E': 'NonFamily_Household_>=7_Person_Household',
    'B24080_003E': 'Male_Private_For_Profit', 'B24080_004E': 'Male_Private_For_Profit_Private_Company', 'B24080_005E': 'Male_Private_For_Profit_Self_Employed_Incorporated',
    'B24080_006E': 'Male_Private_Not_For_Profit', 'B24080_007E': 'Male_Local_Gov', 'B24080_008E': 'Male_State_Gov', 'B24080_009E': 'Male_Federal_Gov',
    'B24080_010E': 'Male_Self_Employed_Not_Incorporated', 'B24080_011E': 'Male_Unpaid_Family_Work', 'B24080_013E': 'Female_Private_For_Profit', 'B24080_014E': 'Female_Private_For_Profit_Private_Company',
    'B24080_015E': 'Female_Private_For_Profit_Self_Employed_Incorporated', 'B24080_016E': 'Female_Private_Not_For_Profit', 'B24080_017E': 'Female_Local_Gov', 'B24080_018E': 'Female_State_Gov',
    'B24080_019E': 'Female_Federal_Gov', 'B24080_020E': 'Female_Self_Employed_Not_Incorporated', 'B24080_021E': 'Female_Unpaid_Family_Work', 'B18101_004E': 'Male_<5_With_Disability',
    'B18101_007E': 'Male_5_17_With_Disability', 'B18101_010E': 'Male_18_34_With_Disability', 'B18101_013E': 'Male_35_64_With_Disability', 'B18101_016E': 'Male_65_74_With_Disability',
    'B18101_019E': 'Male_>=75_With_Disability', 'B18101_023E': 'Female_<5_With_Disability', 'B18101_026E': 'Female_5_17_With_Disability', 'B18101_029E': 'Female_18_34_With_Disability',
    'B18101_032E': 'Female_35_64_With_Disability', 'B18101_035E': 'Female_65_74_With_Disability', 'B18101_038E': 'Female_>=75_With_Disability', 'B18102_004E': 'Male_<5_Hearing_Difficulty',
    'B18102_007E': 'Male_5_17_Hearing_Difficulty', 'B18102_010E': 'Male_18_34_Hearing_Difficulty', 'B18102_013E': 'Male_35_64_Hearing_Difficulty', 'B18102_016E': 'Male_65_74_Hearing_Difficulty',
    'B18102_019E': 'Male_>=75_Hearing_Difficulty', 'B18102_023E': 'Female_<5_Hearing_Difficulty', 'B18102_026E': 'Female_5_17_Hearing_Difficulty', 'B18102_029E': 'Female_18_34_Hearing_Difficulty',
    'B18102_032E': 'Female_35_64_Hearing_Difficulty', 'B18102_035E': 'Female_65_74_Hearing_Difficulty', 'B18102_038E': 'Female_>=75_Hearing_Difficulty', 'B18103_004E': 'Male_<5_Vision_Difficulty',
    'B18103_007E': 'Male_5_17_Vision_Difficulty', 'B18103_010E': 'Male_18_34_Vision_Difficulty', 'B18103_013E': 'Male_35_64_Vision_Difficulty', 'B18103_016E': 'Male_65_74_Vision_Difficulty',
    'B18103_019E': 'Male_>=75_Vision_Difficulty', 'B18103_023E': 'Female_<5_Vision_Difficulty', 'B18103_026E': 'Female_5_17_Vision_Difficulty', 'B18103_029E': 'Female_18_34_Vision_Difficulty',
    'B18103_032E': 'Female_35_64_Vision_Difficulty', 'B18103_035E': 'Female_65_74_Vision_Difficulty', 'B18103_038E': 'Female_>=75_Vision_Difficulty', 'B18104_004E': 'Male_5_17_Cognitive_Difficulty',
    'B18104_007E': 'Male_18_34_Cognitive_Difficulty', 'B18104_010E': 'Male_35_64_Cognitive_Difficulty', 'B18104_013E': 'Male_65_74_Cognitive_Difficulty', 'B18104_016E': 'Male_>=75_Cognitive_Difficulty',
    'B18104_020E': 'Female_5_17_Cognitive_Difficulty', 'B18104_023E': 'Female_18_34_Cognitive_Difficulty', 'B18104_026E': 'Female_35_64_Cognitive_Difficulty', 'B18104_029E': 'Female_65_74_Cognitive_Difficulty',
    'B18104_032E': 'Female_>=75_Cognitive_Difficulty', 'B18105_004E': 'Male_5_17_Ambulatory_Difficulty', 'B18105_007E': 'Male_18_34_Ambulatory_Difficulty', 'B18105_010E': 'Male_35_64_Ambulatory_Difficulty',
    'B18105_013E': 'Male_65_74_Ambulatory_Difficulty', 'B18105_016E': 'Male_>=75_Ambulatory_Difficulty', 'B18105_020E': 'Female_5_17_Ambulatory_Difficulty',
    'B18105_023E': 'Female_18_34_Ambulatory_Difficulty', 'B18105_026E': 'Female_35_64_Ambulatory_Difficulty', 'B18105_029E': 'Female_65_74_Ambulatory_Difficulty',
    'B18105_032E': 'Female_>=75_Ambulatory_Difficulty', 'B18106_004E': 'Male_5_17_Self_Care_Difficulty', 'B18106_007E': 'Male_18_34_Self_Care_Difficulty', 'B18106_010E': 'Male_35_64_Self_Care_Difficulty',
    'B18106_013E': 'Male_65_74_Self_Care_Difficulty', 'B18106_016E': 'Male_>=75_Self_Care_Difficulty', 'B18106_020E': 'Female_5_17_Self_Care_Difficulty', 'B18106_023E': 'Female_18_34_Self_Care_Difficulty',
    'B18106_026E': 'Female_35_64_Self_Care_Difficulty', 'B18106_029E': 'Female_65_74_Self_Care_Difficulty', 'B18106_032E': 'Female_>=75_Self_Care_Difficulty',
    'B18107_004E': 'Male_18_34_Independent_Living_Difficulty', 'B18107_007E': 'Male_35_64_Independent_Living_Difficulty', 'B18107_010E': 'Male_65_74_Independent_Living_Difficulty',
    'B18107_013E': 'Male_>=75_Independent_Living_Difficulty', 'B18107_017E': 'Female_18_34_Independent_Living_Difficulty', 'B18107_020E': 'Female_35_64_Independent_Living_Difficulty',
    'B18107_023E': 'Female_65_74_Independent_Living_Difficulty', 'B18107_026E': 'Female_>=75_Independent_Living_Difficulty',
    'B27001_004E': 'Male_<6_Health_Ins', 'B27001_005E': 'Male_<6_No_Health_Ins', 'B27001_007E': 'Male_6_18_Health_Ins', 'B27001_008E': 'Male_6_18_No_Health_Ins',
    'B27001_010E': 'Male_19_25_Health_Ins', 'B27001_011E': 'Male_19_25_No_Health_Ins', 'B27001_013E': 'Male_26_34_Health_Ins', 'B27001_014E': 'Male_26_34_No_Health_Ins',
    'B27001_016E': 'Male_35_44_Health_Ins', 'B27001_017E': 'Male_35_44_No_Health_Ins', 'B27001_019E': 'Male_45_54_Health_Ins', 'B27001_020E': 'Male_45_54_No_Health_Ins',
    'B27001_022E': 'Male_55_64_Health_Ins', 'B27001_023E': 'Male_55_64_No_Health_Ins', 'B27001_025E': 'Male_65_74_Health_Ins', 'B27001_026E': 'Male_65_74_No_Health_Ins',
    'B27001_028E': 'Male_>=75_Health_Ins', 'B27001_029E': 'Male_>=75_No_Health_Ins', 'B27001_032E': 'Female_<6_Health_Ins', 'B27001_033E': 'Female_<6_No_Health_Ins',
    'B27001_035E': 'Female_6_18_Health_Ins', 'B27001_036E': 'Female_6_18_No_Health_Ins', 'B27001_038E': 'Female_19_25_Health_Ins', 'B27001_039E': 'Female_19_25_No_Health_Ins',
    'B27001_041E': 'Female_26_34_Health_Ins', 'B27001_042E': 'Female_26_34_No_Health_Ins', 'B27001_044E': 'Female_35_44_Health_Ins', 'B27001_045E': 'Female_35_44_No_Health_Ins',
    'B27001_047E': 'Female_45_54_Health_Ins', 'B27001_048E': 'Female_45_54_No_Health_Ins', 'B27001_050E': 'Female_55_64_Health_Ins', 'B27001_051E': 'Female_55_64_No_Health_Ins',
    'B27001_053E': 'Female_65_74_Health_Ins', 'B27001_054E': 'Female_65_74_No_Health_Ins', 'B27001_056E': 'Female_>=75_Health_Ins', 'B27001_057E': 'Female_>=75_No_Health_Ins',
    'B27002_004E': 'Male_<6_Private_Ins', 'B27002_007E': 'Male_6_18_Private_Ins', 'B27002_010E': 'Male_19_25_Private_Ins', 'B27002_013E': 'Male_26_34_Private_Ins',
    'B27002_016E': 'Male_35_44_Private_Ins', 'B27002_019E': 'Male_45_54_Private_Ins', 'B27002_022E': 'Male_55_64_Private_Ins', 'B27002_025E': 'Male_65_74_Private_Ins',
    'B27002_028E': 'Male_>=75_Private_Ins', 'B27002_032E': 'Female_<6_Private_Ins', 'B27002_035E': 'Female_6_18_Private_Ins', 'B27002_038E': 'Female_19_25_Private_Ins',
    'B27002_041E': 'Female_26_34_Private_Ins', 'B27002_044E': 'Female_35_44_Private_Ins', 'B27002_047E': 'Female_45_54_Private_Ins', 'B27002_050E': 'Female_55_64_Private_Ins',
    'B27002_053E': 'Female_65_74_Private_Ins', 'B27002_056E': 'Female_>=75_Private_Ins', 'B27003_004E': 'Male_<6_Public_Ins', 'B27003_007E': 'Male_6_18_Public_Ins',
    'B27003_010E': 'Male_19_25_Public_Ins', 'B27003_013E': 'Male_26_34_Public_Ins', 'B27003_016E': 'Male_35_44_Public_Ins', 'B27003_019E': 'Male_45_54_Public_Ins',
    'B27003_022E': 'Male_55_64_Public_Ins', 'B27003_025E': 'Male_65_74_Public_Ins', 'B27003_028E': 'Male_>=75_Public_Ins', 'B27003_032E': 'Female_<6_Public_Ins', 'B27003_035E': 'Female_6_18_Public_Ins',
    'B27003_038E': 'Female_19_25_Public_Ins', 'B27003_041E': 'Female_26_34_Public_Ins', 'B27003_044E': 'Female_35_44_Public_Ins', 'B27003_047E': 'Female_45_54_Public_Ins',
    'B27003_050E': 'Female_55_64_Public_Ins', 'B27003_053E': 'Female_65_74_Public_Ins', 'B27003_056E': 'Female_>=75_Public_Ins', 'B11003_011E': 'Male_Single_Parent',
    'B11003_016E': 'Female_Single_Parent'}

#Since the CansusData package can't search for all our 385 variables at once, I broke them into 11 lists
demographic_vars_1 = ['B01001_001E', 'B01001_002E', 'B01001_026E', 'B01001_003E', 'B01001_004E', 'B01001_005E', 'B01001_006E', 'B01001_007E', 'B01001_008E', 'B01001_009E',
    'B01001_010E', 'B01001_011E', 'B01001_012E', 'B01001_013E', 'B01001_014E', 'B01001_015E', 'B01001_016E', 'B01001_017E', 'B01001_018E', 'B01001_019E', 'B01001_020E',
    'B01001_021E', 'B01001_022E', 'B01001_023E', 'B01001_024E', 'B01001_025E', 'B01001_027E', 'B01001_028E', 'B01001_029E', 'B01001_030E', 'B01001_031E', 'B01001_032E',
    'B01001_033E', 'B01001_034E', 'B01001_035E', 'B01001_036E']

demographic_vars_2 = ['B01001_037E', 'B01001_038E', 'B01001_039E', 'B01001_040E', 'B01001_041E', 'B01001_042E', 'B01001_043E', 'B01001_044E', 'B01001_045E', 'B01001_046E',
    'B01001_047E', 'B01001_048E', 'B01001_049E', 'B02001_002E', 'B02001_003E', 'B02001_004E', 'B02001_005E', 'B02001_006E',
    'B02001_007E', 'B02001_008E', 'B03001_002E', 'B03001_003E', 'B05001_002E', 'B05001_003E', 'B05001_004E', 'B05001_005E', 'B05001_006E']

commute_vars = ['B08006_003E', 'B08006_004E', 'B08006_008E', 'B08006_014E', 'B08006_015E', 'B08006_016E', 'B08006_017E', 'B08302_002E', 'B08302_003E', 'B08302_004E',
    'B08302_005E', 'B08302_006E', 'B08302_007E', 'B08302_008E', 'B08302_009E', 'B08302_010E', 'B08302_011E', 'B08302_012E', 'B08302_013E', 'B08302_014E', 'B08302_015E',
    'B08303_002E', 'B08303_003E', 'B08303_004E', 'B08303_005E', 'B08303_006E', 'B08303_007E', 'B08303_008E', 'B08303_009E', 'B08303_010E', 'B08303_011E',
    'B08303_012E', 'B08303_013E']

marriage_birth_vars = ['B13016_002E', 'B11001_003E', 'B11001_005E', 'B11001_006E', 'B11001_008E', 'B11001_009E', 'B12001_003E', 'B12001_004E', 'B12001_005E', 'B12001_006E',
    'B12001_007E', 'B12001_008E', 'B12001_009E', 'B12001_010E', 'B12001_012E', 'B12001_013E', 'B12001_014E', 'B12001_015E', 'B12001_016E', 'B12001_017E', 'B12001_018E',
    'B12001_019E', 'B11016_003E', 'B11016_004E', 'B11016_005E', 'B11016_006E', 'B11016_007E', 'B11016_008E', 'B11016_010E', 'B11016_011E', 'B11016_012E', 'B11016_013E',
    'B11016_014E', 'B11016_015E', 'B11016_016E']

education_vars = ['B14001_002E', 'B14001_003E', 'B14001_004E', 'B14001_005E', 'B14001_006E', 'B14001_007E', 'B14001_008E', 'B14001_009E', 'B14001_010E', 'B15003_002E',
    'B15003_003E', 'B15003_004E', 'B15003_005E', 'B15003_006E', 'B15003_007E', 'B15003_008E', 'B15003_009E', 'B15003_010E', 'B15003_011E', 'B15003_012E', 'B15003_013E',
    'B15003_014E', 'B15003_015E', 'B15003_016E', 'B15003_017E', 'B15003_018E', 'B15003_019E', 'B15003_020E', 'B15003_021E', 'B15003_022E', 'B15003_023E', 'B15003_024E',
    'B15003_025E']

income_vars = ['B17001_002E', 'B17001_031E', 'B19001_002E', 'B19001_003E', 'B19001_004E', 'B19001_005E', 'B19001_006E', 'B19001_007E', 'B19001_008E', 'B19001_009E',
    'B19001_010E', 'B19001_011E', 'B19001_012E', 'B19001_013E', 'B19001_014E', 'B19001_015E', 'B19001_016E', 'B19001_017E', 'B21001_002E', 'B21001_003E', 'B23025_004E',
    'B23025_005E', 'B23025_006E', 'B23025_007E', 'B24080_003E', 'B24080_004E', 'B24080_005E', 'B24080_006E', 'B24080_007E', 'B24080_008E', 'B24080_009E', 'B24080_010E',
    'B24080_011E', 'B24080_013E', 'B24080_014E', 'B24080_015E', 'B24080_016E', 'B24080_017E', 'B24080_018E', 'B24080_019E', 'B24080_020E', 'B24080_021E']

assist_housing_vars = ['B19057_002E', 'B19057_003E', 'B19058_002E', 'B19058_003E', 'B19055_002E', 'B19055_003E', 'B19056_002E', 'B19056_003E', 'B19059_002E',
    'B19059_003E', 'B25001_001E', 'B25002_002E', 'B25002_003E', 'B25003_002E', 'B25003_003E', 'B25004_002E', 'B25004_003E', 'B25004_004E',
    'B25004_005E', 'B25004_006E', 'B25004_007E', 'B25004_008E', 'B25018_001E', 'B25027_002E', 'B25031_001E', 'B25035_001E', 'B25037_002E', 'B25037_003E', 'B25064_001E',
    'B25088_002E', 'B25088_003E', 'B25105_001E']

disability_vars_1 = ['B18101_004E', 'B18101_007E', 'B18101_010E', 'B18101_013E', 'B18101_016E', 'B18101_019E', 'B18101_023E', 'B18101_026E', 'B18101_029E', 'B18101_032E',
    'B18101_035E', 'B18101_038E', 'B18102_004E', 'B18102_007E', 'B18102_010E', 'B18102_013E', 'B18102_016E', 'B18102_019E', 'B18102_023E', 'B18102_026E', 'B18102_029E',
    'B18102_032E', 'B18102_035E', 'B18102_038E', 'B18103_004E', 'B18103_007E', 'B18103_010E', 'B18103_013E', 'B18103_016E', 'B18103_019E', 'B18103_023E', 'B18103_026E',
    'B18103_029E', 'B18103_032E', 'B18103_035E', 'B18103_038E', 'B18104_004E', 'B18104_007E', 'B18104_010E']

disability_vars_2 = ['B18104_013E', 'B18104_016E', 'B18104_020E', 'B18104_023E', 'B18104_026E', 'B18104_029E', 'B18104_032E', 'B18105_004E', 'B18105_007E', 'B18105_010E',
    'B18105_013E', 'B18105_016E', 'B18105_020E', 'B18105_023E', 'B18105_026E', 'B18105_029E', 'B18105_032E', 'B18106_004E', 'B18106_007E', 'B18106_010E', 'B18106_013E',
    'B18106_016E', 'B18106_020E', 'B18106_023E', 'B18106_026E', 'B18106_029E', 'B18106_032E', 'B18107_004E', 'B18107_007E', 'B18107_010E', 'B18107_013E', 'B18107_017E',
    'B18107_020E', 'B18107_023E', 'B18107_026E', 'B21100_003E']

health_ins_vars_1 = ['B27001_004E', 'B27001_005E', 'B27001_007E', 'B27001_008E', 'B27001_010E', 'B27001_011E', 'B27001_013E', 'B27001_014E', 'B27001_016E', 'B27001_017E',
    'B27001_019E', 'B27001_020E', 'B27001_022E', 'B27001_023E', 'B27001_025E', 'B27001_026E', 'B27001_028E', 'B27001_029E', 'B27001_032E', 'B27001_033E', 'B27001_035E',
    'B27001_036E', 'B27001_038E', 'B27001_039E', 'B27001_041E', 'B27001_042E', 'B27001_044E', 'B27001_045E', 'B27001_047E', 'B27001_048E', 'B27001_050E', 'B27001_051E',
    'B27001_053E', 'B27001_054E', 'B27001_056E', 'B27001_057E']

health_ins_vars_2 = ['B27002_004E', 'B27002_007E', 'B27002_010E', 'B27002_013E', 'B27002_016E', 'B27002_019E', 'B27002_022E', 'B27002_025E', 'B27002_028E', 'B27002_032E',
    'B27002_035E', 'B27002_038E', 'B27002_041E', 'B27002_044E', 'B27002_047E', 'B27002_050E', 'B27002_053E', 'B27002_056E', 'B27003_004E', 'B27003_007E', 'B27003_010E',
    'B27003_013E', 'B27003_016E', 'B27003_019E', 'B27003_022E', 'B27003_025E', 'B27003_028E', 'B27003_032E', 'B27003_035E', 'B27003_038E', 'B27003_041E', 'B27003_044E',
    'B27003_047E', 'B27003_050E', 'B27003_053E', 'B27003_056E']

single_parent_vars = ['B11003_011E', 'B11003_016E']

#This gets a list of the tracts that are in the city of Chicago
tracts_df = pd.read_csv('CensusTractsTIGER2010.csv')
tract_lst = tracts_df['TRACTCE10'].tolist()

#These are the numbers we will need to get the correct geospatial data
IL_num = '17'
Cook_County_num = '031'

vars_lst = [demographic_vars_1, demographic_vars_2, commute_vars, marriage_birth_vars, education_vars, income_vars, assist_housing_vars,
    disability_vars_1, disability_vars_2, health_ins_vars_1, health_ins_vars_2, single_parent_vars]

i = 0
#Goes through all of the lists we have created
#Sometimes, the government API doesn't work well and you need to call something multiple times
#If it breaks down partway through the list, I tend to just run it again with a smaller vars_lst of the variables we haven't gotten to yet
for vars in vars_lst:
    #Get the census data from the API
    census_data_df = censusdata.download('acs5', 2017,
        censusdata.censusgeo([('state', IL_num), ('county', Cook_County_num), ('tract', '*')]),
        vars).rename(columns=rename_dict)
    #Pulling out the tract number from the index
    census_data_df['Tract'] = census_data_df.index
    census_data_df['Tract'] = census_data_df['Tract'].apply(lambda x: int(re.findall(r"\d\d\d\d\d\d", str(x))[0]))
    #Getting rid of all the tracts we don't want
    census_data_df = census_data_df[census_data_df['Tract'].isin(tract_lst)]
    #Saving our data to a CSV
    csv_name = 'acs5_data_' + str(i) + '.csv'
    census_data_df.to_csv(csv_name)
    i += 1
    print(i)

del census_data_df
del tracts_df
del tract_lst
del vars
del i

gc.collect()
