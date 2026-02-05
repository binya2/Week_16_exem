import uvicorn
from fastapi import FastAPI

from config import settings
from connection import connect_to_mongo, seed_database, close_mongo_connection
from routes import router

app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG
)


async def startup_event():
    connect_to_mongo()
    seed_database()


# app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", close_mongo_connection)

app.include_router(router)

if __name__ == "__main__":
    print(f"Starting server on {settings.SERVER_HOST}:{settings.SERVER_PORT} (Debug={settings.DEBUG})")
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG
    )
