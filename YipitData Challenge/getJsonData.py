#!/usr/local/bin/python
# -- coding: utf-8 --
import json, urllib
import re

def collect_data(url):

    response = urllib.urlopen(url)
    data = json.loads(response.read())
    return data

def parse_data(data_collected):
    
    tableData = []
    movieBudget = []
    lengthOfResults =len(data_collected['results'])
    dataList = ['Year','Title','Budget']
    tableData.append(dataList)
    
    for i in range(0,lengthOfResults):
        dataList = []
        detailedUrl = data_collected['results'][i]['films'][0]['Detail URL']
        year = data_collected['results'][i]['year']
        title = collect_data(detailedUrl)
        title = title['Title']

        try:
            budget = collect_data(detailedUrl)
            budget = budget['Budget']
            budget = convert_budget(budget)
            movieBudget.append(budget)
        except KeyError:
            budget = "US$0 million"
            budget = convert_budget(budget)
            movieBudget.append(budget)

        dataList.append(year.strip()[:4])
        dataList.append(title.strip())
        if budget == 0:
            dataList.append("Not Available")
        dataList.append('$ ' + str(budget).strip())
        tableData.append(dataList)

    for row in tableData:
        print("{: >48} {: >48} {: >48}".format(*row))

    find_average(movieBudget)
    

def convert_budget(budget):
    budget = budget.strip()
    
    if '$' in budget:
        winMovieBudget = re.findall(r"\$?([0-9]?[0-9,|.]+)",budget)
        return process_budget(winMovieBudget[0], True)
    else:
        winMovieBudget = re.findall(r"\$?([0-9]?[0-9,|.]+)",budget)
        return process_budget(winMovieBudget[0],False)
    

def find_average(movieBudgets):
    for num in range(0,len(movieBudgets)):
        if movieBudgets[num] == 0:
            try:
                movieBudgets[num] = (movieBudgets[num-1] + movieBudgets [num + 1]) / 2
            except:
                pass
    
    avg = sum(movieBudgets)/float(len(movieBudgets))
    print 'The average budget of these movies is $%.2f'%(avg)
    

def process_budget(winMovieBudget , flag):
    if flag == True:
    
        if ',' in winMovieBudget:
            winMovieBudget = winMovieBudget.replace(',','')
            return float(winMovieBudget)
        if '.' in winMovieBudget:
            winMovieBudget = float(winMovieBudget) * 1000000
            return winMovieBudget
        else:
            return float(winMovieBudget) * 1000000
    
    else:
        
        if ',' in winMovieBudget:
            winMovieBudget = winMovieBudget.replace(',','')
            return float(winMovieBudget) * 1.27
        if '.' in winMovieBudget:
            winMovieBudget = float(winMovieBudget) * 1000000 *1.27
            return winMovieBudget
        else:
            return float(winMovieBudget) * 1000000 * 1.27


url = "http://oscars.yipitdata.com/"
collected_data = collect_data(url)
parse_data(collected_data)


