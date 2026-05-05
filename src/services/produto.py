from db.conexao import conectar # Responsável por criar e retornar uma conexão com o banco de dados
#from utils.helpers import voltar, limpar_tela

# =================================================================================================
# LISTAR PRODUTOS
# =================================================================================================
def listar_produtos(): # Busca todos os produtos ativos no banco de dados e exibe no terminal
    conexao = conectar() # Cria conexão

    if not conexao: # Se não conectar, interrompe a função
        return
    
    cursor = conexao.cursor() # Cria um cursor (objeto que executa comandos SQL)

    try:
        # Executa consulta SQL
        cursor.execute("""SELECT id_produto, nome, valor_unitario
                       FROM produto
                       WHERE ativo = TRUE
                       """)

        # Recupera todos os resultados
        produtos = cursor.fetchall()

        # Exibição no terminal
        print("\n------ PRODUTOS ------\n")

        # Percorre os produtos e imprime
        for p in produtos:
            print(f"ID: {p[0]} | Nome: {p[1]} | Valor: R$ {p[2]}")
            # p[0] = id_produto
            # p[1] = nome
            # p[2] = valor

        #voltar()
        #limpar_tela()

    # Caso dê erro na consulta
    except Exception as erro:
        print("Erro ao buscar produtos:", erro)

    finally:
        cursor.close() # Fecha o cursor
        conexao.close() # Fecha a conexão com o banco de dados

def cadastrar_produto():
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        print("\n===== CADASTRAR PRODUTO =====")

        nome = input("\nNome do jogo: ")
        descricao = input("Descrição: ")
        valor = float(input("Valor da aposta: "))

        numeros = int(input("Quantidade de números por aposta: "))
        maximo = int(input("Número máximo da aposta: "))
        
        cursor.execute("""INSERT INTO produto (nome, descricao, valor_unitario, numeros_por_aposta, numero_maximo)
                       VALUES (%s, %s, %s, %s, %s)
                       """, (nome, descricao, valor, numeros, maximo))
        
        conexao.commit()

        print("\nProduto cadastrado com sucesso!")

    except Exception as erro:
        print("\nErro ao cadastrar produto", erro)
        conexao.rollback()

    finally:
        cursor.close()
        conexao.close()
