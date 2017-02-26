import os
from app import (create_app)
from lib import Base, sql_engine

Base.metadata.create_all(sql_engine)
app = create_app(config=os.environ.get('ENV', 'Development'))

if __name__ == '__main__':
    app.run(host="0.0.0.0")
