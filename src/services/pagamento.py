from db.conexao import conectar # Responsável por criar e retornar uma conexão com o banco de dados
from utils.helpers import perguntar_sn
from decimal import Decimal

def realizar_pagamento(usuario_logado):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        print("\n===== PAGAMENTO =====")

        id_usuario = usuario_logado[0]
        tipo = usuario_logado[2]

        # Se usuário for CLIENTE lista apenas os pedidos pendentes dele
        if tipo == "CLIENTE":
            cursor.execute("""SELECT p.id_pedido, p.valor_total
                           FROM pedido p
                           WHERE p.status = 'PENDENTE'
                           AND p.id_cliente = (SELECT id_cliente FROM cliente WHERE id_usuario = %s)
                           ORDER BY p.id_pedido
                           """, (id_usuario,))
        
        # Se usuário for ADM ou FUNCIONARIO lista todos os pedidos pendentes
        else:
            cursor.execute("""SELECT p.id_pedido, c.nome, p.valor_total
                           FROM pedido p
                           JOIN cliente c ON p.id_cliente = c.id_cliente
                           WHERE p.status = 'PENDENTE'
                           ORDER BY c.nome, p.id_pedido""")

        
        pedidos = cursor.fetchall()

        if not pedidos:
            print("\nNenhum pedido pendente")
            return
        
        print("\n------- Pedidos -------")

        cliente_atual = None

        for pedido in pedidos:
            
            if tipo == "CLIENTE":
                id_pedido, valor_total = pedido
                print(f"{id_pedido} | R$ {float(valor_total):.2f}")

            else:
                id_pedido, nome_cliente, valor_total = pedido

                # Agrupar por cliente
                if nome_cliente != cliente_atual:
                    
                    print(f"\nCliente: {nome_cliente}\n")
                    cliente_atual = nome_cliente
            
                print(f"{id_pedido} | R$ {float(valor_total):.2f}")
            

        # Escolher pedido para o pagamento
        try:
            id_pedido = int(input("\nDigite o ID do pedido: "))
        except:
            print("\nID inválido!")
            return

        # Buscar valor do pedido
        if tipo == "CLIENTE":
            cursor.execute("""SELECT id_pedido, valor_total
                           FROM pedido
                           WHERE id_pedido = %s
                           AND status = 'PENDENTE'
                           AND id_cliente = (SELECT id_cliente FROM cliente WHERE id_usuario = %s)
                           """, (id_pedido, id_usuario))
        
        # ADMIM / FUNCIONARIO só valida a existência
        else:
            cursor.execute("""SELECT id_pedido, valor_total
                           FROM pedido
                           WHERE id_pedido = %s
                           AND status = 'PENDENTE'
                           """, (id_pedido,))
        
        pedido = cursor.fetchone()

        if not pedido:
            print("\nPedido inválido ou já pago!")
            return
        
        id_pedido, valor_total = pedido

        # Confirmar pagamento        
        print(f"\nTotal: R$ {float(valor_total):.2f}")

        while True:
            # Forma de pagamento
            print("\nForma de pagamento:")
            print("\n1 - Dinheiro")
            print("2 - PIX")
            print("3 - Crédito")
            print("4 - Débito")

            opcao = input("\nEscolha: ")

            formas = {
                "1": "DINHEIRO",
                "2": "PIX",
                "3": "CREDITO",
                "4": "DEBITO"
            }

            forma_pagamento = formas.get(opcao)

            if not forma_pagamento:
                print("\nForma de pagamento inválida!")
                continue

            valor_pago = valor_total
            troco = 0
            
            # Pagamento em dinheiro
            if forma_pagamento == "DINHEIRO":
                try:
                    valor_pago = Decimal(input("\nValor recebido: R$ "))
                except:
                    print("\nValor inválido!")
                    continue
                
                if valor_pago < valor_total:
                    print("\nValor insuficiente!")
                    continue
                
                troco = valor_pago - valor_total
            break

        # Confirmar pagamento
        print(f"\nForma de pagamento: {forma_pagamento}")
        print(f"Valor pago: R$ {float(valor_pago):.2f}")
        if troco > 0:
            print(f"Troco: R$ {float(troco):.2f}")

        confirmar = perguntar_sn("\nConfirmar pagamento? (s/n): ")

        if confirmar != "s":
            print("\nPagamento cancelado.")
            return
        
        # Inserir pagamento
        cursor.execute("""INSERT INTO pagamento (id_pedido, id_usuario, forma_pagamento, valor_pago, troco)
                       VALUES (%s, %s, %s, %s, %s)
                       """, (id_pedido, id_usuario, forma_pagamento, valor_pago, troco))
        
        # Atualizar pedido
        cursor.execute("""UPDATE pedido
                       SET status = 'PAGO'
                       WHERE id_pedido = %s
                       """, (id_pedido,))

        conexao.commit()

        print("\nPagamento realizado com sucesso!")

    #voltar()
    #limpar_tela()

    except Exception as erro:
        print("Erro ao pagar: ", erro)
        conexao.rollback()

    finally:
        cursor.close()
        conexao.close()