from db.conexao import conectar # Responsável por criar e retornar uma conexão com o banco de dados
from utils.helpers import limpar_tela, perguntar_sn
from services.cliente import listar_clientes, validar_cliente
from services.produto import listar_produtos

import json


# =================================================================================================
# CRIAR PEDIDO
# =================================================================================================
def criar_pedido(usuario_logado):
    conexao = conectar() # Abre conexão com o banco

    if not conexao:
        return
    
    cursor = conexao.cursor()

    try:
        print("\n===== CRIAR PEDIDO =====")

        # Dados do usuário logado
        id_usuario = usuario_logado[0]
        tipo = usuario_logado[2]

        # ----- Define o tipo do cliente = 'ADMIN' 'FUNCIONARIO'  'CLIENTE' -----
        if tipo == "CLIENTE": # Se for CLIENTE, usa o mesmo ID do login
            id_cliente = usuario_logado[3]
        
        else: # Se for ADMIN ou FUNCIONARIO, o cliente é escolhido manualmente
            while True:
                listar_clientes()
                
                try:
                    id_cliente = int(input("\nDigite o ID do cliente: "))
                
                except:
                    print("\nEntrada inválida!")
                    continue

                if validar_cliente(cursor, id_cliente):
                    break
                else:
                    print("\nCliente inválido! Tente novamente.")

        limpar_tela()

        print("\n===== CRIAR PEDIDO =====")

        # ----- Criar pedido -----
        cursor.execute("""INSERT INTO pedido (id_cliente, id_usuario, valor_total, status)
                       VALUES (%s, %s, 0, 'PENDENTE')
                       RETURNING id_pedido""",
                       (id_cliente, id_usuario))
        
        id_pedido = cursor.fetchone()[0]
        total_pedido = 0 # Variável para acumular o total de pedidos

        # ----- Loop de produtos -----
        while True:
            listar_produtos()

            try:
                id_produto = int(input("\nDigite o ID do produto: "))
                quantidade = int(input("Digite a quantidade de apostas: "))
            
            except:
                print("\nEntrada inválida!")
                continue

            # ----- Buscar valor do produto -----
            cursor.execute("""SELECT valor_unitario, numeros_por_aposta, numero_maximo
                           FROM produto
                           WHERE id_produto = %s AND ativo = TRUE
                           """, (id_produto,))
            
            produto = cursor.fetchone()

            if not produto:
                print("\nProduto inválido!!!")
                continue

            valor_unitario, qtd_numeros, numero_max = produto
            valor_total_item = valor_unitario * quantidade # Calcula o valor total do item

            # ----- Inserir item -----
            cursor.execute("""INSERT INTO item_pedido (id_pedido, id_produto, quantidade, valor_unitario, valor_total)
                           VALUES (%s, %s, %s, %s, %s)
                           RETURNING id_item
                           """, (id_pedido, id_produto, quantidade, valor_unitario, valor_total_item))
            
            id_item = cursor.fetchone()[0]
            
           # ----- Apostas -----
            for i in range(quantidade):
                print(f"\nAposta {i+1}")

                print(f"\nEscolha {qtd_numeros} números entre 1 e {numero_max}")

                numeros = []

                # Loop até preencher todos os números da aposta
                while len(numeros) < qtd_numeros:

                    try:
                        n = int(input(f"Número {len(numeros)+1}: "))

                        # Valida o intervalo permitido
                        if n < 1 or n > numero_max:
                            print("\nNúmero inválido!\n")
                            continue

                        # Evita números repetidos
                        if n in numeros:
                            print("Número repetido!\nDigite um número válido.")
                            continue

                        numeros.append(n)

                    except:
                        print("\nEntrada inválida!")
                
                # Corvete lista para JSON (para salvar no banco de dados)
                numeros_json = json.dumps(numeros)

                # ----- Inserir aposta -----
                cursor.execute("""INSERT INTO aposta (id_item, numeros)
                               VALUES (%s, %s)
                               """, (id_item, numeros_json))
            
            # Soma no total do pedido
            total_pedido += valor_total_item
        
            # Opção se o usuário deseja fazer outro jogos            
            resposta = perguntar_sn("\nDeseja adicionar outro jogo? (s/n): ")

            if resposta == 's':
                    continue
                
            elif resposta == 'n':
                   break
                

                   
         # Atualizar o total final
        cursor.execute("""UPDATE pedido
                    SET valor_total = %s
                    WHERE id_pedido = %s
                    """, (total_pedido, id_pedido))
            
        # Salva todas as operações no banco de dados
        conexao.commit()
        print(f"\nPedido criado com sucesso! ID: {id_pedido}")
        print(f"Ttotal: R$ {total_pedido: .2f}")


    # Desfaz tudo se der erro
    except Exception as erro:
        print("Erro ao criar pedido:", erro)
        conexao.rollback()

    finally:
        cursor.close()
        conexao.close()


# =================================================================================================
# LISTAR PEDIDOS
# =================================================================================================
def listar_pedidos(usuario_logado):
    conexao = conectar() # Abre conexao com o banco

    if not conexao:
        return # Se não conectar, sai da função
    
    cursor = conexao.cursor() # Cria cursor

    try:
        id_usuario = usuario_logado[0]
        tipo = usuario_logado[2]

        # Filtra pedidos apenas do usuário CLIENTE
        if tipo == "CLIENTE":
            # Junta pedido com cliente para mostrar o nome
            cursor.execute ("""SELECT id_cliente
                            FROM cliente
                            WHERE id_usuario = %s
                            """, (id_usuario,))
            
            resultado = cursor.fetchone()
            
            if not resultado:
                print("\nCliente não encontrado!")
                return

            id_cliente = resultado[0]

            cursor.execute ("""SELECT p.id_pedido, c.nome, p.valor_total, p.status
                            FROM pedido p
                            JOIN cliente c ON p.id_cliente = c.id_cliente
                            WHERE p.id_cliente = %s
                            ORDER BY p.id_pedido ASC
                            """, (id_cliente,))

        # ADMIN / FUNCIONARIO -> Lista todos os clientes
        else:
            cursor.execute ("""SELECT p.id_pedido, c.nome, p.valor_total, p.status
                            FROM pedido p
                            JOIN cliente c ON p.id_cliente = c.id_cliente
                            ORDER BY p.id_pedido ASC
                            """)
        
        pedidos = cursor.fetchall() # Pega todos os resultados

        if not pedidos:
            print("\nNenhum pedido foi encontrado!")
            return
        
        for p in pedidos:

            print(f"ID: {p[0]} | Cliente: {p[1]} | Valor: R$ {p[2]} | Status: {p[3]}")
            # p[0] = id_pedido
            # p[1] = nome cliente
            # p[2] = valor_total
            # p[3] = status

        #voltar()
        #limpar_tela()

    except Exception as erro:
        print("Erro ao listar pedidos: ", erro)

    finally:
        cursor.close()
        conexao.cursor()


# =================================================================================================
# DETALHAR PEDIDO
# =================================================================================================
def detalhar_pedido(usuario_logado):
    conexao = conectar()

    if not conexao:
        return
    
    cursor = conexao.cursor()

    try:
        print("\n===== DETALHAR PEDIDO =====")

        # Dados do usuário logado
        id_usuario = usuario_logado[0]
        tipo = usuario_logado[2]

        # Lista todos os pedidos
        # CLIENTE vê apenas os dele
        # ADMIN / FUNCIONARIO vê todos
        listar_pedidos(usuario_logado)

        try:
            id_pedido = int(input("\nDigite o ID do pedido: "))

        except:
            print("\nID inválido!")

        # Buscar dados do pedido + cliente
        cursor.execute("""SELECT p.id_pedido, c.id_cliente, c.nome, p.valor_total, p.status, p.data_criacao
                       FROM pedido p
                       JOIN cliente c ON p.id_cliente = c.id_cliente
                       WHERE p. id_pedido = %s
                       """, (id_pedido,))
        
        pedido = cursor.fetchone()

        if not pedido:
            print("\nPedido não encontrado!")
            return
        
        id_pedido, id_cliente, nome_cliente, valor_total, status, data_criacao = pedido
        
        if tipo == "CLIENTE":
            cursor.execute("""SELECT id_cliente
                           FROM cliente
                           WHERE id_usuario = %s
                           """, (id_usuario,))
            
            resultado = cursor.fetchone()

            if not resultado:
                print("\nCliente não encontrado!")
                return
            
            id_cliente_logado = resultado[0]

            if id_cliente != id_cliente_logado:
                print("Você não tem acesso a esse pedido!")
        
        limpar_tela()

        # Exibir dados do pedido
        print(f"\nPedido: {id_pedido}")
        print(f"ID Cliente: {id_cliente}")
        print(f"Cliente: {nome_cliente}")
        print(f"Valor: R$ {valor_total}")
        print(f"Status: {status}")
        print(f"\nData: {data_criacao}")

        # Itens do pedido
        cursor.execute("""SELECT i.id_item, pr.nome, i.quantidade, i.valor_total
                       FROM item_pedido i
                       JOIN produto pr ON i.id_produto = pr.id_produto
                       WHERE i.id_pedido = %s
                       """, (id_pedido,))

        itens = cursor.fetchall()

        if not itens:
                print("\nNenhum item encontrado!")
                return

        for item in itens:
            id_item, nome_produto, quantidade, valor_item = item

            print(f"\nProduto: {nome_produto}")
            print(f"Quantidade: {quantidade}")
            print(f"Valor: R$ {float(valor_item):.2f}")

            print("\n===============================================")

            # Apostas do item
            cursor.execute("""SELECT numeros
                        FROM aposta
                        WHERE id_item = %s
                        """, (id_item,))
            
            apostas = cursor.fetchall()

            if not apostas:
                print("\nNenhuma aposta encontrada!")
                continue
            
            for i, aposta in enumerate(apostas, start = 1):        
                print(f"    Aposta {i}: {aposta[0]}") 

                print("===============================================")

        #voltar()
        #limpar_tela()


    except Exception as erro:
        print("Erro ao detalhar pedido: ", erro)

    finally:
        cursor.close()
        conexao.close()