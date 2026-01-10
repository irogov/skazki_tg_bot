from database.connection import get_pg_connection, db_name, host, port, user, password
from psycopg import AsyncConnection
from services.fairytale import get_story

async def add_tale(tale_text, tale_group, rating):
    connection: AsyncConnection = await get_pg_connection(
            db_name=db_name,
            host=host,
            port=port,
            user=user,
            password=password,
        )
        
    async with connection.cursor() as cursor:
        await cursor.execute(
            '''
            INSERT INTO fairytales(tale_text, tale_group, rating)
            VALUES(%s, %s, %s)
            ''',
            (tale_text, tale_group, rating)
        )
        await connection.commit()

async def db_daily_population(db_pool, client):
    async with db_pool.connection() as conn:
        try:
            async with conn.cursor() as cur:
                for gr in range(1, 4):
                    for _ in range(30):
                        tale_text, group = await get_story(gr, client)
                        await cur.execute(
                            '''
                            INSERT INTO fairytales(tale_text, tale_group, rating)
                            VALUES(%s, %s, %s)
                            ''',
                            (tale_text, group, 5)
                        )
                        await conn.commit()
        except Exception as e:
            await conn.rollback()
            print("Ошибка при вставке:", e)
            raise

async def add_user(conn: AsyncConnection, user_tel_id):
    async with conn.cursor() as cursor:
        await cursor.execute(
            '''
            INSERT INTO Users(user_tel_id, is_alive, banned, role, paid)
            VALUES(%s, %s, %s, %s, %s)
            ''',
            (user_tel_id, True, False, 'user', False)
        )
        # await conn.commit()

# async def fetch_tale(user_tel_id, group):
    # connection: AsyncConnection = await get_pg_connection(
    #     db_name=db_name,
    #     host=host,
    #     port=port,
    #     user=user,
    #     password=password,
    # )
    # async with connection.cursor() as cursor:
    #     data = await cursor.execute(
    #         '''
    #         SELECT f.tale_id, f.tale_text
    #         FROM Fairytales f
    #         WHERE f.tale_group = %s
    #         AND NOT EXISTS (
    #             SELECT 1
    #             FROM tales_for_users tfu
    #             WHERE tfu.tale_id = f.tale_id
    #             AND tfu.user_tel_id = %s
    #         );
    #         ''',
    #         (group, user_tel_id)
    #     )
    #     return await data.fetchone()
    
async def add_tale_to_tales_for_users(conn: AsyncConnection, user_tel_id, tale_id):
    async with conn.cursor() as cursor:
        await cursor.execute(
            '''
            INSERT INTO tales_for_users(user_tel_id, tale_id)
            VALUES(%s, %s)
            ''',
            (user_tel_id, tale_id)
        )
        # await conn.commit()

async def fetch_tale(conn: AsyncConnection, user_tel_id, group):
    async with conn.cursor() as cursor:
        data = await cursor.execute(
            '''
            SELECT f.tale_id, f.tale_text
            FROM Fairytales f
            WHERE f.tale_group = %s
            AND NOT EXISTS (
                SELECT 1
                FROM tales_for_users tfu
                WHERE tfu.tale_id = f.tale_id
                AND tfu.user_tel_id = %s
            );
            ''',
            (group, user_tel_id)
        )
        return await data.fetchone()