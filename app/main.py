from fastapi import FastAPI

from app.routers.booking import booking_router
from app.routers.meeting_room import meeting_room_router
from app.routers.user import user_router


app = FastAPI()

app.include_router(meeting_room_router)
app.include_router(user_router)
app.include_router(booking_router)


@app.get("/")
def root():
    return {"message": "Meeting Room Booking Api", "version": "1.0.0"}