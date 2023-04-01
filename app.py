from routes import app

if __name__ == "__main__":
    import os

    os.environ["SERVER_PROTOCOL"] = "HTTP/1.1"
    #TODO replace secret key with env variable
    app.secret_key = "super secret"
    app.run()
