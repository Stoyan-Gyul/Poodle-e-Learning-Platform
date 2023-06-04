import uvicorn
from fastapi import FastAPI
from routers.users import user_router
from routers.courses.admin_functions import course_router
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.include_router(user_router)
app.include_router(course_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with the appropriate list of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Replace with the appropriate list of allowed HTTP methods
    allow_headers=["*"],  # Replace with the appropriate list of allowed headers
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)