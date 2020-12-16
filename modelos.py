from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

SECRET_KEY = 'auditore'
HOST = "localhost"
USER = "franca"
PASSWORD = "1234"
DB = "jogoteca"
PORT = 3306
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'

engine = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Jogo(Base):
    __tablename__ = 'jogo'

    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    categoria = Column(String(50), nullable=False)
    console = Column(String(50), nullable=False)


class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    senha = Column(String(50), nullable=False)


Base.metadata.create_all(engine)

jogo1 = Jogo(id=10, nome='The Sims 4', categoria='Simulacao', console='PC')
jogo2 = Jogo(id=20, nome='Skyrim', categoria='RPG', console='PlayStation')
jogo3 = Jogo(id=30, nome='The Witcher', categoria='RPG', console='PlayStation')

session.add(jogo1)
session.add(jogo2)
session.add(jogo3)

session.commit()

alinni = Usuario(id=1, nome='Alinni França', senha='1234')
ezio = Usuario(id=2, nome='Ezio Auditore', senha='insieme')
bruce = Usuario(id=3, nome='Bruce Wayne', senha='batman')

session.add(alinni)
session.add(ezio)
session.add(bruce)

session.commit()
session.close()
