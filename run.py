import os

from app import create_app

app = create_app(os.environ['APP_ENV'])

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
