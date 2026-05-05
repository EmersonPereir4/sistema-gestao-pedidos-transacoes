from db.conexao import conectar # Responsável por criar e retornar uma conexão com o banco de dados
from utils.helpers import voltar, limpar_tela

# =================================================================================================
# CADASTRAR CLIENTE
# =================================================================================================
def cadastrar_cliente():
    conexao = conectar()
    cursor = conexao.cursor()

    if not conexao:
        return

    try:
        print("\n====== CADASTRO DE CLIENTE ======\n")

        # Dados para login
        login = input("Login: ")
        senha = input("Senha: ")

        # Dados pessoais
        nome = input("Nome: ")
        cpf = input("CPF (Somente números): ")
        telefone = input("Telefone (Somente números): ")
        
        # Inserir usuário
        cursor.execute("""INSERT INTO usuario (login, senha, tipo)
                       VALUES (%s, %s, 'CLIENTE')
                       RETURNING id_usuario
                       """, (login, senha))

        id_usuario = cursor.fetchone()[0]

        # Inserir cliente
        cursor.execute("""INSERT INTO cliente (id_usuario, nome, cpf, telefone)
                       VALUES (%s, %s, %s, %s)
                       """, (id_usuario, nome, cpf, telefone))

        # Confirma a transação no banco (salva)
        conexao.commit()

        print("\nCliente cadastrado com sucesso!")

        voltar()
        limpar_tela()
        
    # Se der erro, desfaz a operação
    except Exception as erro:
        print("\nErro ao cadastrar: ", erro)
        conexao.rollback()

    finally:
        cursor.close() # Fecha cursor
        conexao.close() # Fecha conexão


# =================================================================================================
# LISTAR CLIENTES
# =================================================================================================
def listar_clientes():
    conexao = conectar() # Abre conexao com o banco de dados

    if not conexao:
        return # Se falhar, sai da função
    
    cursor = conexao.cursor() # Cria corsor para executar SQL

    try:
        # Busca todos os clientes ativos ordenados por nome
        cursor.execute("""SELECT id_cliente, nome, telefone, cpf
                       FROM cliente
                       WHERE ativo = TRUE
                       ORDER BY id_cliente ASC
                       """)
        
        clientes = cursor.fetchall() # Pega todos os resultados

        print("\n ------ CLIENTES ------\n")

        if not clientes:
            print("Nenhum cliente cadastrado.")
            return
        
        for c in clientes:
            print(f"{c[0]} - {c[1]} | Tel: {c[2]} | CPF: {c[3]}")
            # c[0] = id_cliente
            # c[1] = nome
            # c[2] = telefone
            # c[3] = cpf

    except Exception as erro:
        print("Erro ao listar clientes:", erro)

    finally:
        cursor.close()
        conexao.close()


def validar_cliente(cursor, id_cliente):
    cursor.execute("""SELECT id_cliente
                   FROM cliente
                   WHERE id_cliente = %s AND ativo = TRUE
                   """, (id_cliente,))
    
    return cursor.fetchone()