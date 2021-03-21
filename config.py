import json

with open("config.json") as file:
    config = json.load(file)


class Config:
    def __init__(self):
        self.keys = Keys()
        self.owner = config["owner"]


class Keys:
    def __init__(self):
        self.token = config["keys"]["token"]
        self.hypixel = config["keys"]["hypixel"]
        self.postgres = config["keys"]["postgres"]
