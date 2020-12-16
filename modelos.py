from hashlib import sha1

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

#engine = create_engine(f'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}')
engine = create_engine('sqlite:///teste_banco.db')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Jogo(Base):
    __tablename__ = 'jogo'

    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    categoria = Column(String(50), nullable=False)
    console = Column(String(50), nullable=False)

    def __repr__(self):
        return f"Jogo {self.nome}  com ID {self.id}"


class Usuario(Base):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    senha = Column(String(50), nullable=False)


    def __repr__(self):
        return f"Usuario {self.nome} com ID {self.id}"


def cria_banco():
    Base.metadata.create_all(engine)

    jogo1 = Jogo(nome='The Sims 4', categoria='Simulacao', console='PC')
    jogo2 = Jogo(nome='Skyrim', categoria='RPG', console='PlayStation')
    jogo3 = Jogo(nome='The Witcher', categoria='RPG', console='PlayStation')

    session.add(jogo1)
    session.add(jogo2)
    session.add(jogo3)

    session.commit()

    alinni = Usuario(nome='Alinni França', senha='1234')
    ezio = Usuario(nome='Ezio Auditore', senha='insieme')
    bruce = Usuario(nome='Bruce Wayne', senha='batman')

    session.add(alinni)
    session.add(ezio)
    session.add(bruce)

    session.commit()
    # session.close()
