import requests
import csv
import pandas as pd
import sys



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

