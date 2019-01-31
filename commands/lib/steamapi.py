import json
import re
import urllib.request
from commands.lib.other import safe_get_list
from operator import itemgetter


class SteamAPI(object):
    """Class for getting information from the steam api"""

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.steam_titles = None

    def set_api_key(self, api_key):
        self.api_key = str(api_key)

    def get_steam_id(self, user):
        match = re.match(
            r'((http|https):\/\/steamcommunity\.com\/(profiles|id)\/(?P<steamid>\w+))', user)

        if match:
            user = match.group("steamid")

        with urllib.request.urlopen("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=" + self.api_key + "&steamids=" + str(user)) as url:
            data = json.loads(url.read().decode())
        if safe_get_list(safe_get_list(data, "response"), "players", []) == []:
            with urllib.request.urlopen("https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key=" + self.api_key + "&vanityurl=" + str(user)) as url:
                data = json.loads(url.read().decode())
            if safe_get_list(safe_get_list(data, "response"), "success") == 1:
                user = safe_get_list(
                    safe_get_list(data, "response"), "steamid")
            else:
                user = None
        return user

    def get_game_titles(self):
        try:
            with urllib.request.urlopen("https://api.steampowered.com/ISteamApps/GetAppList/v2/") as url:
                self.steam_titles = safe_get_list(safe_get_list(
                    json.loads(url.read().decode()), "applist"), "apps")
        except:
            self.steam_titles = None
        return self.steam_titles

    def get_game_title(self, appid):
        for title in self.steam_titles:
            if str(safe_get_list(title, "appid")) == str(appid):
                return safe_get_list(title, "name")
        return "Unknown"

    def get_player_summary(self, steamid):
        with urllib.request.urlopen("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=" + self.api_key + "&steamids=" + str(steamid)) as url:
            data = json.loads(url.read().decode())

        return safe_get_list(safe_get_list(safe_get_list(data, "response"), "players"), 0, False)

    def get_steam_level(self, steamid):
        with urllib.request.urlopen("https://api.steampowered.com/IPlayerService/GetSteamLevel/v1/?key=" + self.api_key + "&steamid=" + str(steamid)) as url:
            return safe_get_list(safe_get_list(json.loads(url.read().decode()), "response"), "player_level", "Unknown")

    def get_owned_games(self, steamid):
        with urllib.request.urlopen("https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key=" + self.api_key + "&steamid=" + str(steamid)) as url:
            data = safe_get_list(json.loads(url.read().decode()), "response")

        if safe_get_list(data, "game_count", 0) == 0:
            return []

        return safe_get_list(data, "games", [])

    def get_most_played_games(self, steamid, amount=5):
        games = [[0, 0] for i in range(amount)]
        for game in self.get_owned_games(steamid):
            if safe_get_list(game, "playtime_forever", 0) > min([game[1] for game in games]):
                games[amount - 1][0] = safe_get_list(game, "appid")
                games[amount - 1][1] = safe_get_list(game, "playtime_forever")
                games = sorted(games, key=itemgetter(1), reverse=True)

        return games
