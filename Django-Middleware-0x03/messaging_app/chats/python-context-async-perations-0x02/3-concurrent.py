import asyncio
import aiosqlite

# وظيفة تجلب جميع المستخدمين
async def async_fetch_users():
    async with aiosqlite.connect("example.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("👥 All users:")
            print(users)
            return users

# وظيفة تجلب المستخدمين الأكبر من 40 سنة
async def async_fetch_older_users():
    async with aiosqlite.connect("example.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            older_users = await cursor.fetchall()
            print("\n🧓 Users older than 40:")
            print(older_users)
            return older_users

# تشغيل الاستعلامات بشكل متزامن
async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
