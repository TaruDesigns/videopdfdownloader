import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers import router

app = FastAPI()

app.include_router(router)
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5987)
