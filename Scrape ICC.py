from bs4 import BeautifulSoup
import csv
from urllib.request import urlopen
import pandas as pd

######
# Had to repeat this code twice. Error shown in first run "'utf-8' codec can't decode byte 0xd2 in position 444: invalid continuation byte"
# This was at row 17067 of the file
# Therefore rows from 17067 was moved to another file and run again.
# Csv Files Scraped Data from ICC nov 19 and Scraped Data from ICC nov 19 2 are the result of trial 1 and trial 2 respectively
# Number of unavailable xings in trial 1 = 495
# Number of unavailable xings in trial 2 = ?


#Pay attention to the encoding!
#All Scraped Crossings are available in "Scraped Data from ICC Nov 19.csv"
######
xingInIL = 0
with open('../Inventory Database Downloaded/Illinois Database (As of August 2018).csv', newline='', encoding='latin-1') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    #reader = csv.reader(csvfile, delimiter=',')
    #row_count = sum(1 for row in reader)
    df_cols = []
    unavailable_xing = []
    ####### This is to identify the number of variables that are present in the table #######
    url = "https://www.icc.illinois.gov/railroad/crossing.aspx?dotId=938792R"
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    table = soup.find("table", {"class": "table table-striped table-bordered table-responsive"})
    nrowinTable = len(table.findAll('tr'))
    df_vals = [[] for i in range(nrowinTable)]
    #print("Number of rows ="+row_count)
    for i, row in enumerate(spamreader):
        if (row==[] or row==None):
            continue
        if i == 0:
            print(row)
        print(i)
        #print(row)
        #print(row[0]+" "+row[12])
            #Ignore the first line of the Input FRA Inventory CSV File. The first line is headers.
        if row[12] == '17':  #Row[12] is StateCD and 17 = Illinois
            #print("here "+row[0])
            url = "https://www.icc.illinois.gov/railroad/crossing.aspx?dotId="+row[0]
            page = urlopen(url)
            soup = BeautifulSoup(page, 'html.parser')
            table = soup.find("table", {"class": "table table-striped table-bordered table-responsive"})
            if table == None:
                unavailable_xing.append(row[0])
                continue

            j = 0
            for r in table.findAll('tr'):
                colval = r.td.string
                df_vals[j].append(colval)
                j += 1
                if (xingInIL == 0):  # Just once parse thru the table to get all the column headers
                    colname = r.th.string
                    df_cols.append(colname)

            xingInIL += 1
#except:
#        print(i)


    print(xingInIL)
    df = pd.DataFrame(columns=df_cols)
    for k in range(len(df_cols)):
        df[df_cols[k]] = df_vals[k]
    print(df.shape)
    df.to_csv("Scraped Data from ICC Nov 19.csv")
csvfile.close()

