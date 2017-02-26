import config
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import (declarative_base)
from sqlalchemy.orm import (sessionmaker)

conf = getattr(config, os.environ.get('ENV', 'Development') + 'Config')

# sql_engine = create_engine('+psycopg2://%s:%s@%s/%s' % (conf.DB_USERNAME, conf.DB_PASSWORD, conf.DB_HOST, conf.DB_NAME))
sql_engine = create_engine('sqlite:///taylor.db')
Session = sessionmaker(bind=sql_engine)
session = Session()
Base = declarative_base()
