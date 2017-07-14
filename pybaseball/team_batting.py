import pandas as pd
from bs4 import BeautifulSoup
import requests

def get_soup(start_season, end_season, league, ind):
	url = "http://www.fangraphs.com/leaders.aspx?pos=all&stats=bat&lg={}&qual=0&type=8&season={}&month=0&season1={}&ind={}&team=0,ts&rost=0&age=0&filter=&players=0&page=1_100000"
	url = url.format(league, end_season, start_season, ind)
	s=requests.get(url).content
	#print(s)
	return BeautifulSoup(s, "html.parser")

def get_table(soup, ind):
	#doesn't work yet
	tables = soup.find_all('table')
	table = tables[10]
	data = []
	# couldn't find these in the table, hardcoding for now
	if ind == 0:
		headings = ["Team", "G","PA","HR","R","RBI","SB","BB%","K%","ISO","BABIP","AVG","OBP","SLG","wOBA","wRC+","BsR","Off","Def","WAR"]
	else:
		headings = ["Season","Team","G","PA","HR","R","RBI","SB","BB%","K%","ISO","BABIP","AVG","OBP","SLG","wOBA","wRC+","BsR","Off","Def","WAR"]

	data.append(headings)
	table_body = table.find('tbody')
	rows = table_body.find_all('tr')
	for row in rows:
	    cols = row.find_all('td')
	    cols = [ele.text.strip() for ele in cols]
	    data.append([ele for ele in cols[1:]])
	data = pd.DataFrame(data)
	data = data.rename(columns=data.iloc[0])
	data = data.reindex(data.index.drop(0))
	return data

def team_batting(start_season, end_season=None, league='all', ind=1):
	"""
	Get season-level batting data aggregated by team. 

	ARGUMENTS:
	start_season : int : first season you want data for (or the only season if you do not specify an end_season)
	end_season : int : final season you want data for 
	league : "all", "nl", or "al"
	ind : int : =1 if you want individual season level data, =0 if you want a team's aggreagate data over all seasons in the query
	"""
	if start_season is None:
		raise ValueError("You need to provide at least one season to collect data for. Try team_batting(season) or team_batting(start_season, end_season).")
	if end_season is None:
		end_season = start_season
	soup = get_soup(start_season=start_season, end_season=end_season, league=league, ind=ind)
	table = get_table(soup, ind)
	return table
