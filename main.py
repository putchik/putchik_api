from fastapi import FastAPI, Depends

from app.config.init_app import initiate_database
from app.applications.users.routes import router as UserRouter
from app.core.auth.routers.login import router as AuthRouter

app = FastAPI()


@app.on_event("startup")
async def start_database():
    await initiate_database()


app.include_router(AuthRouter, tags=["Auth"], prefix="/api/auth/login")
app.include_router(UserRouter, tags=["Users"], prefix="/user")
# app.include_router(StudentRouter,tags=["Students"],prefix="/student",dependencies=[Depends(token_listener)],)
