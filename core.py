########################################################
# Author:     Johnson Olusegun
# Course:     Advance CS topics (CSC 121, Spring 2021)
# Assignment: Italy & Covid reporting Assigment in 2020
# Python version: Python 3.8
########################################################

# perform all pandas operations
import pandas as pd
from regions import *


class Core:

    # constructor
    def __init__(self):
        self._data = self.read_files()

        # this function reads all the files

    def read_files(self):
        # read the growth rate csv
        try:
            # read growth rate
            # growth_rate = pd.read_csv('./Italy_Covid_2020/growth_rate.csv')
            # read case by infection
            # case_by_infection = pd.read_csv('./Italy_Covid_2020/cases_by_infection.csv')
            # italy reported case
            reported_case = pd.read_csv('./Italy_Covid_2021/reported_cases.csv')
            # italy region summary
            italy_summary_table = pd.read_csv('./Italy_Covid_2021/summary_table.csv')
            # country reported case
            covid_march = pd.read_csv('./Italy_Covid_2020/owid.csv')

        except FileNotFoundError as e:
            # set notification error
            print(e.filename)
            return []
        else:

            return [reported_case, covid_march, italy_summary_table]

        # get region function
        # this function gets and return all the regions

    def get_region(self):
        if len(self._data) > 0:
            return self._data[0]['region'].unique()
        return ["None"]

    # get European Countries
    # get all the european countries
    def get_european_countries(self):
        if len(self._data) > 0:
            df = self._data[1]
            df1 = df.loc[df['continent'] == 'Europe']

            return df1['location'].unique()

        return ["None"]

    # Summary table
    # get italy region summary
    def getRegionSummary(self, name):
        # empty dictionary
        s = {}
        # data frame
        df = self._data[2]

        # extract the data
        try:
            # get region summary
            row = df.loc[df['Region'] == name]
            # get index
            index = df.index[df['Region'] == name][0]
            s['newConfirmed'] = row['New confirmed cases by infection date'][index]
            s['expectedChanges'] = row['Expected change in daily cases'][index]
        except KeyError:
            s['newConfirmed'] = "Unknown"
            s['expectedChanges'] = "Unknown"

        return s

    # this function gets and display country statistic
    def getRegionStats(self, name):
        # get region population
        region_population = self.get_population(name)
        # get case number
        case_number = self.get_case_number(name)
        # calculate percentage
        cal_percentage = self.get_percentage(case_number, region_population)
        # get region summary
        summary_table = self.getRegionSummary(name)

        if region_population and case_number and cal_percentage is not None:
            return {
                "region": name,
                "population": regions['Italy'],
                "region_population": region_population,
                "case_number": case_number,
                "newConfirmed": summary_table['newConfirmed'],
                "expectedChanges": summary_table['expectedChanges'],
                "percentage": round(cal_percentage, 1)
            }
        else:
            return None

    # get population
    # this method gets region population by name
    def get_population(self, name):
        # set local variables
        found = False
        code = ''
        # loop through region object
        for k in regions:
            # strip and check if name entered match name in region object
            if name.strip() == k:
                code = regions[k]
                found = True
        # check if found else return None
        if found:
            return code
        else:
            return None

    # get case number method
    def get_case_number(self, name):

        # check the length
        if len(self._data) > 0:
            # total number of case
            case_sum = 0
            # list of case
            all_case = self._data[0]
            # get name and index from list
            for index, re in enumerate(all_case['region']):
                # check if name == name
                if re == name:
                    # get case by index
                    confirm = all_case['confirm'][index]
                    case_sum += confirm
            # return case
            return case_sum
        # else return None
        return None

    # get the sum of all italy reported case
    def all_italy_reported_case(self):
        total_case = 0
        # check for errors
        if len(self._data) > 0:
            # loop through all the region
            for region in self.get_region():
                total_case += self.get_case_number(region)
            return total_case
        else:
            return None

    # calculate percentage
    def get_percentage(self, reported_case, region_population):
        # check the length
        if len(self._data) > 0:
            # How many people belong to the particular demographic you're measuring, and how many people belong to the
            # entire population

            re_population = region_population.split(',')
            # total population
            total_population = ''
            for i in re_population:
                total_population += i

            # Divide the number of people in your demographic
            # affected divided by entire population
            step1 = int(reported_case) / int(total_population)
            # Multiply the result from Step 1 by 100 to convert it into a percentage:
            step2 = step1 * 100

            return step2
        else:
            return None

    # This function accept country name and return an array of population and max infection case
    def find_data_by_Country(self, country):
        if len(self._data) > 0:
            df = self._data[1]
            df1 = df.loc[df['location'] == country]

            try:
                population = max(df1['population'].dropna())
            except ValueError:
                population = 0

            try:
                infection_case = max(df1['total_cases'].dropna())
            except ValueError:
                infection_case = 0

            return [population, infection_case]

        return ["None"]

    #######################################################
    # get country stats
    def getEuropeanCountryStats(self, country):
        euroDataList = self.find_data_by_Country(country)
        rate = self.getInfectionRate(euroDataList, country)
        return rate

    ####################################################
    # get italy country stats
    def getItalyStats(self, country):
        italyDataList = self.find_data_by_Country(country)
        rate = self.getInfectionRate(italyDataList, country)
        return rate

    #####################################################
    # calculate infection rate
    def calculateInfectionRate(self, totalPopulation, numOfCase, K):
        # number of infections / population at risk * K
        return numOfCase / totalPopulation * K

    #####################################################
    # get infection rate
    def getInfectionRate(self, dataList, country):
        # constant K
        K = 100
        rateDic = {}
        if dataList[0] == 0:
            rateDic['country'] = country
            rateDic['population'] = "Not enough data"
            rateDic['case'] = "Not enough data"
            rateDic['rate'] = "Unknown"
            rateDic['constant'] = K

        elif dataList[1] == 0:
            rateDic['country'] = country
            rateDic['population'] = dataList[0]
            rateDic['case'] = "Not enough data"
            rateDic['rate'] = "Unknown"
            rateDic['constant'] = K
        else:
            rateDic['country'] = country
            rateDic['population'] = dataList[0]
            rateDic['case'] = dataList[1]
            rateDic['rate'] = "" + str(round(self.calculateInfectionRate(dataList[0], dataList[1], K), 1)) + "%"
            rateDic['constant'] = K

        return rateDic
