from flask import Flask, render_template, request, redirect, session, flash, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from prepara_banco import Jogo
from dao import JogoDao, UsuarioDao
import time
import os

app: Flask = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/jogoteca.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

jogo_dao = JogoDao(db)
usuario_dao = UsuarioDao(db)


@app.route('/')
def index():
    lista = jogo_dao.listar()
    return render_template('lista.html', titulo='Jogos', jogos=lista)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')


@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    jogo = jogo_dao.salvar(jogo)

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')
    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    jogo = jogo_dao.busca_por_id(id)
    nome_imagem = recupera_imagem(id)
    return render_template('editar.html', titulo='Editando Jogo', jogo=jogo
                           , capa_jogo=nome_imagem or 'capa_padrao.jpg')


def recupera_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa{id}' in nome_arquivo:
            return nome_arquivo


def deleta_arquivo(id):
    arquivo = recupera_imagem(id)
    os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))


@app.route('/atualizar', methods=['POST',])
def atualizar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console, id=request.form['id'])

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deleta_arquivo(jogo.id)
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')
    jogo_dao.salvar(jogo)
    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    jogo_dao.deletar(id)
    flash('O jogo foi removido com sucesso!')
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Não logado, tente denovo!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)


if __name__ == '__main__':
    app.run(debug=True)
    
    -------------------------------------------------------------------------
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
-------------------------------------------------------------------------------------------------

from prepara_banco import Jogo, Usuario, session, Session

DELETA_JOGO = 'delete from jogo where id = %s'
JOGO_POR_ID = 'SELECT id, nome, categoria, console from jogo where id = %s'
USUARIO_POR_ID = 'SELECT id, nome, senha from usuario where id = %s'
ATUALIZA_JOGO = 'UPDATE jogo SET nome=%s, categoria=%s, console=%s where id = %s'
BUSCA_JOGOS = 'SELECT id, nome, categoria, console from jogo'
CRIA_JOGO = 'INSERT into jogo (nome, categoria, console) values (%s, %s, %s)'


class JogoDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, jogo):
        cursor = self.__db.connection.cursor()

        if (jogo.id):
            cursor.execute(ATUALIZA_JOGO, (jogo.nome, jogo.categoria, jogo.console, jogo.id))
        else:
            cursor.execute(CRIA_JOGO, (jogo.nome, jogo.categoria, jogo.console))
            jogo.id = cursor.lastrowid
        self.__db.connection.commit()
        return jogo

    def listar(self):
        jogos = session.query(BUSCA_JOGOS)
        for jogos in Jogo:
            print(Jogo.id, Jogo.nome, Jogo.categoria, Jogo.console)
        return jogos

    def busca_por_id(self, Jogo):
        for Jogo in Session.query(Jogo.id).distinct():
            session.query(Jogo.id).all()

    def deletar(self,id):
        jogo = session.query(Jogo).filter(Jogo.id == id)
        jogo.delete()
        session.commit()

class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def busca_por_id(self, Usuario):
        for Usuario in Session.query(Usuario.id).distinct():
            session.query(Usuario.id).all()

    def traduz_jogos(jogos):
        def cria_jogo_com_tupla(tupla):
            return Jogo(tupla[1], tupla[2], tupla[3], id=tupla[0])

        return list(map(cria_jogo_com_tupla, jogos))

    def traduz_usuario(tupla):
        return Usuario(tupla[0], tupla[1], tupla[2])
