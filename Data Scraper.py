import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from selenium import webdriver
import time
import random
import sys






# url = 'https://theaudl.com/stats/player-stats'

# html = requests.get(url)

# s = BeautifulSoup(html.content, 'html.parser')

# pattern = s.find('div', id='web-panel-player-stats-table')

# nested = pattern.find('div', class_='svelte-player-stats-container svelte-16n93gz')
# last = nested.find('div', class_='svelte-player-stats-table svelte-16n93gz')
# table = last.find('table', class_='svelte-16n93gz')
# contents = table.find_all('tr') 

# table = s.find('div', id = 'web-panel-player-stats-table')

# progress = table.find('div', id = 'svelte-player-stats-table svelte-16n93gz')

# print(s.prettify())


# base_url = 'https://www.backend.audlstats.com/web-api/player-stats?limit=20&page={}'


'''
csv_filename = 'player_stats.csv'

with open(csv_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    page = 1
    while page < 2:
        url = base_url.format(page)
        response = requests.get(url)
        data = response.json()

        if page == 1:
            # Write header row on the first page
            header = list(data[0].keys())
            writer.writerow(header)

        for row in data['data']:
            writer.writerow(row.values())

        page += 1

    # Print the 
    csvfile.seek(0)  # Move the file pointer to the beginning of the file
    reader = csv.reader(csvfile)

    for row_num, row in enumerate(reader):
        if row_num >= 5:
            break

        print(row)


# Send a GET request to the website
url = "https://theaudl.com/stats/player-stats"
response = requests.get(url)

# Create a BeautifulSoup object
soup = BeautifulSoup(response.content, 'html.parser')

div_stats_table = soup.find('div', id='web-panel-player-stats-table')
# Find the table containing player stats
table = div_stats_table.find('table')

print(soup.prettify())

# Extract the headers from the table
headers = [header.text.strip() for header in table.find_all('th')]

# Extract the data rows from the table
data_rows = []
for row in table.find_all('tr'):
    data_rows.append([data.text.strip() for data in row.find_all('td')])

# Specify the filename for the CSV file
filename = "player_stats.csv"

# Write the data to the CSV file
with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)  # Write the headers
    writer.writerows(data_rows)  # Write the data rows

print(f"Player stats have been saved to '{filename}'.")



base_url = "https://theaudl.com/stats/player-stats?page="

def scrape_page(page_num):
    url = base_url + str(page_num)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Use BeautifulSoup or pandas to find the table and convert it into a DataFrame
    df = pd.read_html(str(soup.find_all('table')))[0]

    return df

all_data = pd.DataFrame()

for i in range(50):  # loop over the number of pages
    df = scrape_page(i)
    all_data = pd.concat([all_data, df])
    
# save the DataFrame to a csv file
all_data.to_csv('player_stats.csv', index=False)



# Initialize the driver
driver = webdriver.Chrome()  # You can also use Chrome or other browsers
base_url = "https://theaudl.com/stats/player-stats?page="

all_data = pd.DataFrame()

# Loop through all the pages
for i in range(1, 51):
    url = base_url + str(i)
    driver.get(url)
    
    # Wait for JavaScript to load the page
    driver.implicitly_wait(5)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Parse the table
    df = pd.read_html(str(soup.find_all('table')))[0]
    all_data = pd.concat([all_data, df])

    time.sleep(random.randint(1,5))

# Save to csv
all_data.to_csv('player_stats.csv', index=False)

# Close the driver
driver.quit()


data = pd.read_csv('player_stats.csv')

print(data.head())
'''

class PlayerStats():


    def __init__(self, year, per, team):
        self.base_url = 'https://www.backend.audlstats.com/web-api/player-stats?limit=20'
        self.year = year
        self.per = per
        self.team = team

    def get_url(self, page: int) -> str:
        if self.year == 'career' and self.team == 'all':
            return f"{self.base_url}&page={page}&per={self.per}"
        elif self.year == 'career':
            return f"{self.base_url}&page={page}&per={self.per}&team={self.team}"
        elif self.team == 'all':
            return f"{self.base_url}&page={page}&year={self.year}&per={self.per}"
        
        return f"{self.base_url}&page={page}&year={self.year}&per={self.per}&team={self.team}"
    
    def get_table(self):
        hasPlayerLeft = True
        playerStats = []
        page = 1
        while(hasPlayerLeft):
            try:
                url = self.get_url(page)
                data = requests.get(url)
                usable_data = data.json()
                players = usable_data['stats']
            except:
                print(f'An error occurred when attempting to scrape data from {url}')
                sys.exit(1)
            if not players:
                hasPlayerLeft = False
            else:
                playerStats = playerStats + players
                page = page + 1
        dataFrame = pd.DataFrame(playerStats)
        
        return dataFrame


    def stats_to_csv(self, file_path):
        try:
            df = self.get_table()
            df.to_csv(file_path, sep=',', index=False)
            print(f'Succesfully saved data as a csv file at {file_path}')
        except Exception as e:
            print(f'An error occurred when trying to save data as a csv file: {e}')

def main():
    stats = PlayerStats('career', 'total', 'spiders')
    # print(stats.get_table())
    path = '/Users/ridgehuang/Desktop/audldata/audldatavisualization/spiders_lifetime_stats.csv'

    stats.stats_to_csv(path)

if __name__ == '__main__':
    main()

