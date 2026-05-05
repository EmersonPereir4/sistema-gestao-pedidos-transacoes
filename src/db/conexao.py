# Importa a biblioteca responsável por conectar com o postgreSQL
import psycopg2

# Função responsável por criar e retornar uma conexão com o banco de dados PostgreSQL.

# Retorno:
# - Objeto de conexão (connection) se tudo der certo.
# - None caso ocorra algum erro.

# Observação:
# - Essa função centraliza a conexão com o banco de dados, facilitando manutenção e evitando repetição de código em várias partes do sistema.

def conectar():
    try: # Tenta estabelecer a conexão com o banco de dados.
        return psycopg2.connect(
            host = "localhost", # Servidor do banco de dados (local).
            database = "sistema_gestao_pedidos_transacoes", # Nome do banco de dados.
            user = "postgres", # Usuário do banco de dados.
            password = "20130207" # Senha do banco de dados.
        )
    except Exception as erro: # Exibe o erro caso a conexão falhe.
        print("\nErro ao conectar: ", erro)
        return None # Retorna None para indicar a falha.