import motor.motor_asyncio
import asyncio

async def test_connection():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")  # Replace with your MongoDB URI
    try:
        db = client["your_database_name"]
        await client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
    finally:
        client.close()

asyncio.run(test_connection())
