import json

with open("config.json") as file:
    config = json.load(file)


class Config:
    def __init__(self):
        self.keys = Keys()
        self.owner = config["owner"]
        self.channels = Channels()


class Keys:
    def __init__(self):
        self.token = config["keys"]["token"]
        self.hypixel = config["keys"]["hypixel"]
        self.postgres = config["keys"]["postgres"]


class Channels:
    def __init__(self):
        self.errors = config["channels"]["errors"]

    def get(self, bot):
        self.errors = bot.get_channel(self.errors)
