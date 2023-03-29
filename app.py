from routes import app

if __name__ == "__main__":
    import os

    os.environ["SERVER_PROTOCOL"] = "HTTP/1.1"

    app.secret_key = "any random string"
    app.run()
