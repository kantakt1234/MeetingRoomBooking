from fastapi import FastAPI

from routes.booking import booking_router
from routes.meeting_room import meeting_room_router
from routes.user import user_router


app = FastAPI()

app.include_router(meeting_room_router)
app.include_router(user_router)
app.include_router(booking_router)
