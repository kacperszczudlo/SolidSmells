from src.app_factory import create_app
from src.config import FLASK_DEBUG

if __name__ == "__main__":
    create_app().run(debug=FLASK_DEBUG, host="0.0.0.0", port=5000)
