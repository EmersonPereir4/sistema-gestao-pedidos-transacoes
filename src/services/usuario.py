from db.conexao import conectar
from utils.helpers import limpar_tela

def login():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        limpar_tela()
        print("\n===== LOGIN =====")
        login = input("\nLogin: ")
        senha = input("Senha: ")

        cursor.execute("""SELECT u.id_usuario, u.login, u.tipo, c.id_cliente
                       FROM usuario u
                       LEFT JOIN cliente c ON c.id_usuario = u.id_usuario
                       WHERE u.login = %s AND u.senha = %s AND u.ativo = TRUE
                       """, (login, senha))
        
        usuario = cursor.fetchone()

        if usuario:
            print(f"\nBem-vindo, {usuario[1]}!")
            return usuario # (id, nome, tipo)
        else:
            print("\nLogin ou senha inválidos!")
            return None
        
    except Exception as erro:
        print("\nErro no login: ", erro)
        return
        
    finally:
        cursor.close()
        conexao.close()

def cadastrar_funcionario(usuario_logado):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        print("\n===== CADASTRAR FUNCIONÁRIO =====")

        # Verifica se é ADMIN
        tipo = usuario_logado[2]

        if tipo != "ADMIN":
            print("\nApenas ADMIN pode cadastrar funcionários!")
            return
        
        # Dados do funcionário

        login = input("\nLogin: ")
        senha = input("Senha: ")

        # Inserir usuário
        cursor.execute("""INSERT INTO usuario (login, senha, tipo)
                       VALUES (%s, %s, 'FUNCIONARIO')
                       """, (login, senha))
        
        conexao.commit()

        print("\nFuncionário cadastrado com sucesso!")

    except Exception as erro:
        print("\nErro ao cadastrar funcionário: ", erro)
        conexao.rollback()

    finally:
        cursor.close()
        conexao.close()

def listar_funcionarios(usuario_logado):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        print("\n===== FUNCIONÁRIOS =====")

        # Verifica permissão
        tipo = usuario_logado[2]

        if tipo != "ADMIN":
            print("Apenas ADMIN pode ver funcionários!")
            return
        
        cursor.execute("""SELECT id_usuario, login
                      FROM usuario
                      WHERE tipo = 'FUNCIONARIO'
                      ORDER BY id_usuario""")
        
        funcionarios = cursor.fetchall()

        if not funcionarios:
            print("\nNenhum funcionário cadastrado...")
            return
        
        print("\n------ Lista de Funcionários ------")

        for funcionario in funcionarios:
            id_usuario, login = funcionario

            print(f"\nID: {id_usuario}")
            print(f"Login: {login}")

    except Exception as erro:
        print("\nErro ao listar funcionários: ", erro)
    
    finally:
        cursor.close()
        conexao.close()