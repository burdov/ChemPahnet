import aiosqlite
import datetime

DB_PATH = "votes.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS votes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            vote TEXT,
            date TEXT
        )''')
        await db.commit()

async def has_voted_today(user_id):
    today = datetime.date.today().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT 1 FROM votes WHERE user_id=? AND date=?", (user_id, today)) as cursor:
            row = await cursor.fetchone()
            return row is not None

async def save_vote(user_id, vote):
    today = datetime.date.today().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("INSERT INTO votes (user_id, vote, date) VALUES (?, ?, ?)", (user_id, vote, today))
        await db.commit()

async def get_today_stats():
    today = datetime.date.today().isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT vote, COUNT(*) FROM votes WHERE date=? GROUP BY vote", (today,)) as cursor:
            svalka = govno = 0
            async for row in cursor:
                if row[0] == "svalka":
                    svalka = row[1]
                elif row[0] == "govno":
                    govno = row[1]
            return svalka, govno

async def get_history(days=7):
    start_date = (datetime.date.today() - datetime.timedelta(days=days-1)).isoformat()
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("""
            SELECT date, 
                   SUM(vote = 'svalka') as svalka, 
                   SUM(vote = 'govno') as govno
            FROM votes
            WHERE date >= ?
            GROUP BY date
            ORDER BY date DESC
            LIMIT ?
        """, (start_date, days)) as cursor:
            result = []
            async for row in cursor:
                result.append((row[0], row[1], row[2]))
            result.sort()
            return result
