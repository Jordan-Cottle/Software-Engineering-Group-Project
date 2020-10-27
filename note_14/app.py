import os

from server import app

if __name__ == "__main__":
    app.run(
        host=os.getenv("IP", "127.0.0.1"), port=int(os.getenv("PORT", 5000)), debug=True
    )