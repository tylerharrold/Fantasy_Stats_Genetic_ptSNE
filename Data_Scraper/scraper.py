from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import pandas as pd
import os
from pathlib import Path

# Quick and dirty script using Beautiful Soup to scrape fantasy data from pro football
# 	reference for the past decade or so


# custom search function to get tabular data while ignoring the regular header rows
# that intersperse player data on pro football reference (for readability, i presume)
def is_tr_but_has_no_class(tag):
	return tag.name == 'tr' and not tag.has_attr("class")

# function that does the scraping for a given year
def scrape_year(year):
	url = 'https://www.pro-football-reference.com/years/' + str(year) + '/fantasy.htm'

	response = get(url).content

	html = BeautifulSoup(response , 'html.parser')

	fantasy_table = html.find('tbody')
	rows = fantasy_table.find_all(is_tr_but_has_no_class)

	players = []

	for row in rows:
		player = []
		tds = row.find_all('td')
		for col in tds:
			col_text = col.get_text()
			if col_text == '':
				col_text = 0
			player.append(col_text)
		players.append(player)


	dir_path = os.path.dirname(os.path.realpath(__file__))

	if dir_path[-1] is not '/' : dir_path = dir_path + '/'

	filename = str(year) + '_raw.csv'

	save_path = dir_path + '../RawFantasyData/' + filename

	df = pd.DataFrame(players)
	df.to_csv(save_path, index=None , header=None)


# run for a hair over a decade
year = 2019

for i in range(12):
	year = year - 1
	scrape_year(year)
