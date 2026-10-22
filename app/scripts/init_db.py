import sys
from pathlib import Path

from sqlalchemy.orm import Session

from app.core.auth import get_password_hash
from app.core.config import settings
from app.core.db import engine
from app.models import User

sys.path.append(str(Path(__file__).parent.parent))


def init_db() -> None:
    with Session(engine) as session:
        user = session.query(User).where(User.login == settings.SUPERUSER_LOGIN).first()
        if not user:
            password = get_password_hash(settings.SUPERUSER_PASSWORD)
            new_user = User()
            new_user.name = settings.SUPERUSER_NAME
            new_user.is_admin = True
            new_user.login = settings.SUPERUSER_LOGIN
            new_user.password_hash = password
            session.add(new_user)
            session.commit()


if __name__ == "__main__":
    print("Инициализация базы данных...")
    init_db()
    print("Готово!")