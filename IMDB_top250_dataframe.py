import requests

from bs4 import BeautifulSoup

import pandas as pd

from pandasgui import show

import numpy as np

import time

starter=time.time()

url="https://www.imdb.com/chart/top/"
response=requests.get(url)

html_codes=response.content

soup=BeautifulSoup(html_codes,"html.parser")

lst_of_points=[]
for each in soup.find_all("strong"):
    lst_of_points.append(each["title"])

lst_of_names=[]
for each in soup.find_all("a"):
    try:
        lst_of_names.append(each["title"])
    except KeyError:
        pass
lst_of_films=[]
for each in soup.find_all("a"):
    if each.string!=None:
        lst_of_films.append(each.string)
release_year=[]
for each in soup.find_all("span",{"class":"secondaryInfo"}):
    release_year.append(int(each.string[1:-1]))


lst_of_films=lst_of_films[44:-28]

lst_of_names=lst_of_names[:-5]
lst_of_dirs=[]
for each in lst_of_names:
    lst=each.split(",")
    lst_of_dirs.append(lst[0])
lst_of_points=lst_of_points
lst_of_stars=[]
lst_of_vote_number=[]

for each in lst_of_points:

    lst_of_stars.append(float(each[:3]))


    lst=each[13:-13].split(",")
    empty=""
    for i in lst:
        empty+=i
    lst_of_vote_number.append(int(empty))

dict_for_dataframe={
                    "Name of the Film":lst_of_films[:247],

                    "Release Year":release_year[:247],

                    "Team":lst_of_names[:247],

                    "Star":lst_of_stars[:247],

                    "Number of Votes":lst_of_vote_number[:247],

                    "Director of the Film":lst_of_dirs[:247]

                    }
print(len(dict_for_dataframe["Name of the Film"]),len(dict_for_dataframe["Release Year"]),len(dict_for_dataframe["Team"]),len(dict_for_dataframe["Star"]),len(dict_for_dataframe["Number of Votes"]),len(dict_for_dataframe["Director of the Film"]))
data=pd.DataFrame(dict_for_dataframe)
data.reset_index(drop=True,inplace=True)

data["Weighted Popularism Calculation"]=np.sqrt(data["Star"]*data["Number of Votes"])



def filter_for_star_number_and_year(filter_for_star_number,filter_for_year):
    if isinstance(filter_for_star_number, (int,float)) and isinstance(filter_for_year, int) :
        x=data["Star"]>=filter_for_star_number

        y=data["Release Year"]>=filter_for_year

        return data[x&y]



def filter_for_year(filter_for_year):
    if isinstance(filter_for_year, int):
        x=data["Release Year"]>=filter_for_year
        return data[x]



def filter_for_star_number(filter_for_star_number):
    if isinstance(filter_for_star_number, (int, float)):
        xx=data["Star"]>=filter_for_star_number
        return data[xx]



def choose_directory(number_of_director):

    print("You choose {}".format(pd.unique(data["Director of the Film"])[number_of_director - 1]))
    filter=data["Director of the Film"]==pd.unique(data["Director of the Film"])[number_of_director-1]
    return data[filter]




print("Welcome to IMDB Top 250 Interface")

while True:
    ask=int(input("1-Filter by number of stars\n2-Filter by release time\n3-Both\n4-Choose Director\n5-None\nChoose One:"))


    if ask==1:
        filter=float(input("Number of Stars: "))
        try:
            int(filter)
        except:
            pass
        print("Work in Progress...")
        show(filter_for_star_number(filter))
        break


    elif ask==2:
        filter=int(input("Release Year: "))
        print("Work in Progress...")
        show(filter_for_year(filter))
        break


    elif ask==3:
        filter1=float(input("Number of Stars: "))
        filter2=int(input("Release Year: "))
        print("Work in Progress...")
        try:
            int(filter1)
        except:
            pass

        show(filter_for_star_number_and_year(filter1,filter2))
        break


    elif ask==4:
        for index, each in enumerate(pd.unique(data["Director of the Film"])):
            print("{}. {}".format(index + 1, each))

        number_of_director = int(input("Which director you want to watch? "))

        print("Work in Progress...")

        show(choose_directory(number_of_director))
        break


    elif ask==5:
        print("Work in Progress...")

        show(data)

        break

    else:
        print("Incorrect choice")
        continue

