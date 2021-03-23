import asyncpg


async def DataConnect(password):
    data = Data()
    await data._initialize(password)
    return data


class Data:
    async def _initialize(self, password):
        self.pool = await asyncpg.create_pool(host="localhost", user="postgres", database="umjibot", password=password)

    async def set(self, id_: int, key, value):
        async with self.pool.acquire() as connection:
            await connection.execute(f"INSERT INTO users(id, {key}) VALUES($1, $2) ON CONFLICT (id) DO UPDATE SET {key} = $2", id_, value)
            await self.pool.release(connection)

    async def get(self, id_: int):
        async with self.pool.acquire() as connection:
            data = await connection.fetchrow("SELECT * FROM users WHERE id = $1", id_)
            await self.pool.release(connection)
            if not data: return
            return Player(data)

    async def delete(self, id_: int):
        async with self.pool.acquire() as connection:
            await connection.execute("DELETE FROM users WHERE id = $1", id_)
            await self.pool.release(connection)


class Player:
    def __init__(self, data):
        self.uuid = data.get("uuid")
        self.blacklisted = data.get("blacklisted", False)

    @staticmethod
    def default():
        return Player({})
