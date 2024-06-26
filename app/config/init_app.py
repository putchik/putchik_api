from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import settings


def get_app_list():
    app_list = [
        f"app.{settings.APPLICATIONS_MODULE}.{app}.models.User"
        for app in settings.APPLICATIONS
    ]
    return app_list


async def initiate_database():
    app_list = ["app.applications.users.models.User", "app.applications.users.models.SmsAuthCode"]

    client = AsyncIOMotorClient(settings.DATABASE_URL)
    await init_beanie(
        database=client.get_default_database(), document_models=app_list
    )
