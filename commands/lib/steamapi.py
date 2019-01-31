# TODO: Create steam class
# So we can do Steam.get_player_summaries(user)
# Steam.api_key = XXXXXXXXXXXXX
import json
import re
import urllib.request
from commands.lib.other import safe_get_list


class SteamAPI(object):
    """Class for getting information from the steam api"""

    def __init__(self, api_key=None):
        self.api_key = api_key
        self.steam_titles = None

    def set_api_key(self, api_key):
        self.api_key = api_key

    def get_steam_id(self, user):
        match = re.match(
            r'((http|https):\/\/steamcommunity.com\/(profiles|id)\/(?P<steamid>\w+))', user)

        if match:
            user = match.group("steamid")

        with urllib.request.urlopen("https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key=" + self.api_key + "&steamids=" + user) as url:
            data = json.loads(url.read().decode())
        if safe_get_list(safe_get_list(data, "response"), "players", []) == []:
            with urllib.request.urlopen("https://api.steampowered.com/ISteamUser/ResolveVanityURL/v1/?key=" + self.api_key + "&vanityurl=" + user) as url:
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
