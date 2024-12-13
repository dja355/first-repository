#importing libraries - have to first install beautiful soup and pandas
import requests
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup

#initialize a few known variables that you will use
url = 'https://web.archive.org/web/20230902185655/https://en.everybodywiki.com/100_Most_Highly-Ranked_Films'
db_name = 'Movies1.db'
table_name = 'Top_50'
# csv_path = 'c:\users\dj_ap\Desktop\PY4E\code3\movies_ibm\top_50_films1.csv'
csv_path = 'top_50_films1.csv'
df = pd.DataFrame(columns=["Film","Year","IMDb's Top 250"])
count = 0

#load the webpage
html_page = requests.get(url).text
data = BeautifulSoup(html_page, 'html.parser')


tables = data.find_all('tbody')
rows = tables[0].find_all('tr')

for row in rows:
    # if count<40:
    col = row.find_all('td')
    if len(col)!=0:
        data_dict = {"Film": col[1].contents[0],
                    "Year": col[2].contents[0],
                    "IMDb's Top 250": col[4].contents[0]}
        df1 = pd.DataFrame(data_dict, index=[0])
        df = pd.concat([df,df1], ignore_index=True)
            # count+=1
    # else:
        # break

df1 = df[df['Year'] >= "1965"]



def convert_to_int(value):
    try:
        return int(value)
    except ValueError:
        return 1000  # or any default value you prefer

# Apply the function to the column
df1["IMDb's Top 250"] = df1["IMDb's Top 250"].apply(convert_to_int)

print(df1)



df1["IMDb's Top 250"] = df1["IMDb's Top 250"].astype(int, errors="ignore")

df2 = df1.sort_values(by="IMDb's Top 250", ascending=True)

print(df2)

df2.set_index("IMDb's Top 250", inplace=True)

print(df2)

df2.to_csv(csv_path)

conn = sqlite3.connect(db_name)
df2.to_sql(table_name, conn, if_exists='replace', index=False)
conn.close()