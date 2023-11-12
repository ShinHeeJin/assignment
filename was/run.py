from app import create_app
from dotenv import load_dotenv
import os

load_dotenv()

app = create_app(os.environ.get("APP_CONFIG"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)