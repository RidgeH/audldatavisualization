import requests
import csv
import pandas as pd
import sys


class PlayerStats():


    def __init__(self, year, per, team):
        self.base_url = 'https://www.backend.ufastats.com/web-api/player-stats?limit=20'
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

class TeamStats():

    # &opponent and &perGame
    
    def __init__(self, year, per, team):
        self.base_url = 'https://www.backend.ufastats.com/web-api/team-stats?limit=50'
        self.year = year
        self.per = per
        self.team = team
    
    def get_url(self):
        route = self.base_url
        if self.year != 'Career':
            route += f'&year={self.year}'
        if self.per == 'game':
            route += '&perGame'
        if self.team == 'opponent':
            route += '&opponent'
        
        return route
    
    def get_table(self):
        # only one page, total teams = 38, max = 50, don't see the UFA adding > 12 teams anytime soon, no loops.
        url = self.get_url()
        stats = requests.get(url).json()
        team_stats = stats['stats']
        dataFrame = pd.DataFrame(team_stats)
        return dataFrame
    
    def stats_to_csv(self, file_path):
        try:
            df = self.get_table()
            df.to_csv(file_path, sep=',', index=False)
            print(f'Successfully saved team stats at {file_path}')
        except Exception as e:
            print(f'An error occurred when trying to save team stats as a csv file: {e}')

def main():
    spiders_2024 = PlayerStats('2024', 'total', 'spiders')
    path = '/Users/ridgehuang/Desktop/audldata/audldatavisualization/team_stats_2024.csv'
    team_stats_2024 = TeamStats(2024, 'total', 'team')
    print(team_stats_2024.get_table())
    team_stats_2024.stats_to_csv(path)

if __name__ == '__main__':
    main()