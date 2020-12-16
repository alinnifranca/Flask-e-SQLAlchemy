from flask import Flask, render_template, request, redirect, session as flask_session, flash, url_for, send_from_directory
from modelos import Jogo, session, Usuario
import time
import os

app: Flask = Flask(__name__)
app.secret_key = b"frase secreta"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/jogoteca.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# db = SQLAlchemy(app)

# jogo_dao = JogoDao(db)
# usuario_dao = UsuarioDao(db)


@app.route('/')
def index():
    query_jogo = session.query(Jogo)
    lista = query_jogo.all()
    return render_template('lista.html', titulo='Jogos', jogos=lista)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in flask_session or flask_session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')


@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form.get('nome', '')
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome=nome, categoria=categoria, console=console)
    session.add(jogo)
    session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    arquivo.save(f'{upload_path}/capa{jogo.id}-{timestamp}.jpg')
    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in flask_session or flask_session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))

    query_jogo = session(Jogo)
    jogo = query_jogo.filter_by(id=id).all()[0]
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
    sessio.add(Jogo)
    session.commit()

    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    jogo = session.query(Jogo).filter_by(id=id).all()
    if len(jogo == 1):
        session.delete(jogo[0])
        session.commit()
        flash(f"Jogo {jogo.nome} removido com sucesso!")
    else:
        flash("Jogo não encontrado")

    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    nome_usuario = request.form['usuario']

    usuarios = session.query(Usuario).filter_by(nome=nome_usuario).all()
    if len(usuarios) != 1:
        flash('Não logado, tente de novo!')
        return redirect(url_for('login'))

    usuario = usuarios[0]

    if usuario.senha == request.form['senha']:
        flask_session['usuario_logado'] = usuario.id
        flash(usuario.nome + ' logou com sucesso!')
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina)
    else:
        flash('Não logado, tente de novo!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    flask_session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))


@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)


if __name__ == '__main__':
    app.run(debug=True)
    
