from modelos import Jogo, Usuario, session, Session

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
