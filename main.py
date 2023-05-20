import uvicorn
from fastapi import FastAPI
from routers.users import user_router
from routers.courses import courses_router



app = FastAPI()
app.include_router(user_router)
app.include_router(courses_router)




# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)