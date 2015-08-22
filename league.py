__author__ = 'josealvarado'

from leagueoflegends import LeagueOfLegends, RiotError


import urllib2
import json

import pycurl
from StringIO import StringIO

import requests
import time
import sys


# def main():

# lol = LeagueOfLegends('ENTER YOUR API KEY HERE')

    # Call the API with explicit summoner ID
    # id = lol.get_summoner_by_name('Brute_Ogre')
#lol.get_games(id)

    # # Or set the ID globally for all future calls
    # lol.set_summoner('your-summoner-name')
    # lol.get_summoner_stats()
    # lol.get_summoner_ranked_stats()

    # Access data through dictionaries
    # try:
    #     teams = lol.get_summoner_teams()
    #     for t in teams:
    #         print t["name"]
    #         for m in t["roster"]["memberList"]:
    #             id = m["playerId"]
    #             print id
    #             print lol.get_summoner_by_id(id)["name"]
    # except RiotError, e:
    #     print e.error_msg

# Returns a list of all champions. Optionally only return free to play champions.

    # try:
    #     champs = lol.get_champions(free_to_play=False)
    #     for champ in champs:
    #         print champ
    #         # print champ["name"]
    # except RiotError, e:
    #     print e.error_msg

# Returns a list of recent games played by a specific summoner, up to 10.
# Takes a specific `summoner_id` (long) argument. If you want to query by summoner name, add a second lookup (see below).

    # try:
    #     games = lol.get_summoner_games(2000)
    #     for game in games:
    #         print game["championId"]
    # except RiotError, e:
    #     print e.error_msg

if __name__ == '__main__':
    # main()

    # url = "https://na.api.pvp.net/api/lol/na/v2.2/match/1597716990?api_key=d17bf0eb-0ded-4c06-b41b-d9b03fbf6bd1"

    # opener = urllib2.build_opener(NotModifiedHandler())
    # req = urllib2.Request(url)
    # url_handle = opener.open(req)

    # buffer = StringIO()
    # c = pycurl.Curl()
    # c.setopt(c.URL, url)
    # c.setopt(c.WRITEDATA, buffer)
    # c.perform()
    # c.close()
    #
    # body = buffer.getvalue()
    # # Body is a string in some encoding.
    # # In Python 2, we can print it without knowing what the encoding is.
    # print(body)

    game_id = sys.argv[1]

    value = int(game_id)

    for i in range(0, 100000):
        time.sleep(1)
        # print value - i
        try:
            url = "https://na.api.pvp.net/api/lol/na/v2.2/match/" + str(value - i) + "?api_key=ENTER YOUR API KEY HERE"

            # print url
            r = requests.get(url)
            # print r.status_code
            print r.json()
        except :
            time.sleep(1)

    # url = "https://na.api.pvp.net/api/lol/na/v2.2/match/" + game_id + "?api_key=ENTER YOUR API KEY HERE"
    # r = requests.get(url)
    # print r.json()
