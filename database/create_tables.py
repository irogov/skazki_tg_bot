import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from psycopg import AsyncConnection, Error
from connection import get_pg_connection, db_name, host, port, user, password

if sys.platform.startswith("win") or os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def main():
    connection: AsyncConnection | None = None

    try:
        connection = await get_pg_connection(
            db_name=db_name,
            host=host,
            port=port,
            user=user,
            password=password,
        )
        async with connection:
            async with connection.transaction():
                async with connection.cursor() as cursor:
                    await cursor.execute(
                        '''
                            CREATE TABLE IF NOT EXISTS Users (
                                user_id SERIAL PRIMARY KEY,
                                user_tel_id BIGINT NOT NULL UNIQUE,
                                is_alive BOOLEAN,
                                banned BOOLEAN,
                                role VARCHAR,
                                paid BOOLEAN
                            )
                        '''
                    )
                    await cursor.execute(
                        '''
                            CREATE TABLE IF NOT EXISTS Fairytales (
                                tale_id SERIAL PRIMARY KEY,
                                tale_text VARCHAR,
                                tale_group INT,
                                rating INT
                            )
                        '''
                    )
                    await cursor.execute(
                        '''
                            CREATE TABLE IF NOT EXISTS tales_for_users (
                                user_tel_id BIGINT NOT NULL REFERENCES Users(user_tel_id),
                                tale_id INT NOT NULL REFERENCES Fairytales(tale_id),
                                PRIMARY KEY (user_tel_id, tale_id)
                            )
                        '''
                    )
    except Error as db_error:
        print("Database-specific error: %s", db_error)
    except Exception as e:
        print("Unhandled error: %s", e)
    finally:
        if connection:
            await connection.close()
            print("Connection to Postgres closed")
    
asyncio.run(main())
