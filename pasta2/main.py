import mysql.connector
from mysql.connector import Error

# Função genérica de conexão
def conectar_banco():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='bd_teste_estagio'
    )

def criar_tabela():
    try:
        #é uma boa prática usar o with, porque ele fecha a conexão automaticamente
        with conectar_banco() as conexao:          # abre a conexão
            with conexao.cursor() as cursor:       # abre o cursor
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    email VARCHAR(100) NOT NULL UNIQUE,
                    idade INT NOT NULL
                )
                """)
                conexao.commit()
                print("Tabela 'usuarios' criada com sucesso!")
    except Error as e:
        print(f"Erro ao criar tabela: {e}")
        
def pedidos():
    try:
        with conectar_banco() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("""
                CREATE TABLE IF NOT EXISTS pedidos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    usuario_id INT,
                    produto VARCHAR(100) NOT NULL,
                    quantidade INT NOT NULL,
                    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                )
                """)
                conexao.commit()
                print("Tabela 'pedidos' criada com sucesso!")
    except Error as e:
        print(f"Erro ao criar tabela: {e}")

def inserir_usuario(nome, email, idade):
    try:
        with conectar_banco() as conexao:          # abre conexão só aqui
            with conexao.cursor() as cursor:
                comando_sql = "INSERT INTO usuarios (nome, email, idade) VALUES (%s, %s, %s)"
                valores = (nome, email, idade)
                cursor.execute(comando_sql, valores)
                conexao.commit()
                print("Usuário inserido com sucesso!")
    except Error as e:
        print(f"Erro ao inserir usuário: {e}")
        
def inserir_pedido(usuario_id, produto, quantidade):
    try:
        with conectar_banco() as conexao:
            with conexao.cursor() as cursor:
                comando_sql = "INSERT INTO pedidos (usuario_id, produto, quantidade) VALUES (%s, %s, %s)"
                valores = (usuario_id, produto, quantidade)
                cursor.execute(comando_sql, valores)
                conexao.commit()
                print("Pedido inserido com sucesso!")
    except Error as e:
        print(f"Erro ao inserir pedido: {e}")
        
def deletar_usuario(nome):
    try:
        with conectar_banco() as conexao:
            with conexao.cursor() as cursor:
                comando_sql = "DELETE FROM usuarios WHERE nome = %s"
                cursor.execute(comando_sql, (nome,)) # tupla de um elemento(um elemento precisa da vírgula)
                conexao.commit()
                print("Usuário deletado com sucesso!")
    except Error as e:
        print(f"Erro ao deletar usuário: {e}")
        
def mostrar_usuarios():
    try:
        with conectar_banco() as conexao:
            with conexao.cursor() as cursor:
                comando_sql = "SELECT * FROM usuarios"
                cursor.execute(comando_sql)
                resultados = cursor.fetchall()
                for row in resultados:
                    nome = row[1]
                    email = row[2]
                    idade = row[3]
                    print(f"Nome: {nome}, Email: {email}, Idade: {idade}")
    except Error as e:
        print(f"Erro ao buscar usuários: {e}")
        
def mostrar_usuarios_pedidos():
    try:
        with conectar_banco() as conexao:
            with conexao.cursor() as cursor:
                comando_sql = """
                SELECT usuarios.nome, pedidos.produto
                FROM usuarios JOIN pedidos 
                ON usuarios.id = pedidos.usuario_id;
                """
                cursor.execute(comando_sql)
                resultados = cursor.fetchall()
                for row in resultados:
                    nome = row[0]
                    produto = row[1]
                    print(f"Nome: {nome}, Produto: {produto}")
    except Error as e:
        print(f"Erro ao buscar usuários e pedidos: {e}")
    
def atualizar_usuario(nova_idade, nome):
    try:
        with conectar_banco() as conexao:
            with conexao.cursor() as cursor:
                comando_sql = "UPDATE usuarios SET idade = %s WHERE nome = %s"
                valores = (nova_idade, nome)
                cursor.execute(comando_sql, valores)
                
                if cursor.rowcount == 0:
                    print("Nenhum usuário encontrado com esse nome.")
                else:
                    conexao.commit()
                    print("Usuário atualizado com sucesso!")
    except Error as e:
        print(f"Erro ao atualizar usuário: {e}")
    
# ---- Programa principal ----

"""inserir_usuario("João", "joao@email.com", 25)
mostrar_usuarios()
atualizar_usuario(30, "João")
mostrar_usuarios()
deletar_usuario("João")
mostrar_usuarios()"""


mostrar_usuarios_pedidos()
