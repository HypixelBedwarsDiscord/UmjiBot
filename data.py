import asyncpg


async def DataConnect(password):
    data = Data()
    await data._initialize(password)
    return data


class Data:
    async def _initialize(self, password):
        self.data = await asyncpg.connect(host="localhost", user="postgres", database="umjibot", password=password)

    async def set(self, id_: int, key, value):
        await self.data.execute(f"INSERT INTO users(id, {key}) VALUES($1, $2) ON CONFLICT (id) DO UPDATE SET {key} = $2", id_, value)

    async def get(self, id_: int):
        data = await self.data.fetchrow("SELECT * FROM users WHERE id = $1", id_)
        if not data: return
        return Player(data)

    async def delete(self, id_: int):
        await self.data.execute("DELETE FROM users WHERE id = $1", id_)


class Player:
    def __init__(self, data):
        self.uuid = data.get("uuid")
        self.blacklisted = data.get("blacklisted", False)

    @staticmethod
    def default():
        return Player({})
