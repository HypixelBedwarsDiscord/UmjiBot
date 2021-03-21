from tinydb import TinyDB, Query
from tinydb.operations import delete


class Data:
    def __init__(self):
        self.data = TinyDB("data.json")
        self.query = Query()

    def set(self, id_: int, key: str, value):
        self.data.upsert({"id": id_, key: value}, self.query.id == id_)

    def get(self, id_: int):
        data = self.data.get(self.query.id == id_)
        if not data: return
        return Player(data)

    def delete(self, id_: int, key):
        if value := self.data.get(self.query.id == id_).get(key):
            self.data.update(delete(key), self.query.id == id_)
            return value


class Player:
    def __init__(self, data):
        self.uuid = data.get("uuid")
        self.blacklisted = data.get("blacklisted", False)

    @staticmethod
    def default():
        return Player({})
