import os
from dotenv import load_dotenv
from api.index import app
from api.scheduler import start_scheduler

load_dotenv()

if __name__ == "__main__":
    start_scheduler()
    app.run(host="0.0.0.0", port=5000, debug=True)
