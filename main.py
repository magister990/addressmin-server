from api import app
from db import engine, session, Base

if __name__ == '__main__':
    Base.metadata.create_all()
    app.run()
