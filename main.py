from fastapi import FastAPI
from routes.meeting_room import meeting_room_router
from routes.user import auth_router
import uvicorn


app = FastAPI()

app.include_router(meeting_room_router)
app.include_router(auth_router)

if __name__ == '__main__':
    uvicorn.run(app)