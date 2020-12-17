""" Main module for actually running the flask application """

import os

from server import app
from config import UPLOAD_FOLDER

from database import ENGINE
from models import Base


if __name__ == "__main__":
    # Create database schema
    Base.metadata.create_all(ENGINE.engine)
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(
        host=os.getenv("IP", "127.0.0.1"),
        port=int(os.getenv("PORT", "5000")),
        debug=True,
    )
