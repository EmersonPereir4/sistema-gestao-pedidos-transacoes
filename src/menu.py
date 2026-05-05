from utils.helpers import voltar, limpar_tela

from services.usuario import login, cadastrar_funcionario, listar_funcionarios

from services.produto import listar_produtos, cadastrar_produto

from services.cliente import cadastrar_cliente, listar_clientes

from services.pedido import criar_pedido, listar_pedidos, detalhar_pedido

from services.pagamento import realizar_pagamento

from services.relatorio import gerar_relatorio_pdf

#from services.pagamento import realizar_pagamento

# =================================================================================================
# MENU INICIAL
# =================================================================================================
def menu_inicial():
    # Loop infinito até o usuário sair
    while True: # Loop infinito até o usuário sair
        #limpar_tela()
        print("\n======= BEM VINDO =======\n")
        print("1 - Login")
        print("2 - Cadastrar")
        print("0 - Sair\n")

        # Recebe a opção escolhida pelo usuário
        opcao = input("Escolha: ")

        if opcao == "1":
            limpar_tela()
            return login()
        
        elif opcao == "2":
            limpar_tela()
            cadastrar_cliente() # Chama a função cadastrar pedido

        elif opcao == "0":
            limpar_tela()
            return None

        else:
            print("\nOpção inválida!") # Caso digite algo errado


# =================================================================================================
# MENU ADMIN
# =================================================================================================
def menu_admin(usuario_logado):
    while True:
        limpar_tela()
        print("\n======= MENU ADMIN  =======\n")
        print("1 - Listar Produtos")
        print("2 - Cadastrar Produtos")
        print("3 - Cadastrar Clientes")
        print("4 - Cadastrar Funcionários")
        print("5 - Listar Clientes")
        print("6 - Listar Funcionários")
        print("7 - Criar Pedido")
        print("8 - Listar Pedidos")
        print("9 - Detalhar Pedido")
        print("10 - Realizar Pagamento")
        print("11 - Gerar Relatório")
        print("0 - Voltar ao Início\n")

        # Recebe a opção escolhida pelo usuário
        opcao = input("Escolha: ")

        if opcao == "1":
            limpar_tela()
            listar_produtos() # Chama a função listar produtos
            voltar()
        
        elif opcao == "2":
            limpar_tela()
            cadastrar_produto() # Chama a função cadastrar produto
            voltar()

        elif opcao == "3":
            limpar_tela()
            cadastrar_cliente() # Chama a função cadastrar cliente
            voltar()
        
        elif opcao == "4":
            limpar_tela()
            cadastrar_funcionario(usuario_logado) # Chama a função cadastrar funcionário
            voltar()
        
        elif opcao == "5":
            limpar_tela()
            listar_clientes() # Chama a função listar cliente
            voltar()
        
        elif opcao == "6":
            limpar_tela()
            listar_funcionarios(usuario_logado) # Chama a função listar funcionarios
            voltar()
        
        elif opcao == "7":
            limpar_tela()
            criar_pedido(usuario_logado) # Chama a função criar pedido
            voltar()

        elif opcao == "8":
            limpar_tela()
            print("\n====== PEDIDOS ======\n")
            listar_pedidos(usuario_logado) # Chama a função listar pedidos
            voltar()
        
        elif opcao == "9":
            limpar_tela()
            detalhar_pedido(usuario_logado) # Chama a função detalhar pedido
            voltar()
        
        elif opcao == "10":
            limpar_tela()
            realizar_pagamento(usuario_logado) # Chama a função realizar pagamento
            voltar()

        elif opcao == "11":
            limpar_tela()
            gerar_relatorio_pdf(usuario_logado) # Chama a função gerar relatório
            voltar()

        elif opcao == "0":
            print("\nSaindo...\n")
            limpar_tela()
            return menu_inicial()

        else:
            print("\nOpção inválida!") # Caso digite algo errado


# =================================================================================================
# MENU FUNCIONARIO
# =================================================================================================
def menu_funcionario(usuario_logado):
    while True:
        limpar_tela()
        print("\n======= MENU COLABORADOR  =======\n")
        print("1 - Listar Produtos")
        print("2 - Cadastrar Clientes")
        print("3 - Listar Clientes")
        print("4 - Criar Pedido")
        print("5 - Listar Pedidos")
        print("6 - Detalhar pedido")
        print("7 - Realizar pagamento")
        print("0 - Sair\n")

        # Recebe a opção escolhida pelo usuário
        opcao = input("Escolha: ")

        if opcao == "1":
            limpar_tela()
            listar_produtos() # Chama a função listar produtos
            voltar()
        
        elif opcao == "2":
            limpar_tela()
            cadastrar_cliente() # Chama a função cadastrar cliente
            voltar()
        
        elif opcao == "3":
            limpar_tela()
            listar_clientes() # Chama a função listar cliente
            voltar()
        
        elif opcao == "4":
            limpar_tela()
            criar_pedido(usuario_logado) # Chama a função criar pedido
            voltar()

        elif opcao == "5":
            limpar_tela()
            print("\n====== PEDIDOS ======\n")
            listar_pedidos(usuario_logado) # Chama a função listar pedidos
            voltar()
        
        elif opcao == "6":
            limpar_tela()
            detalhar_pedido(usuario_logado) # Chama a função detalhar pedido
            voltar()
        
        elif opcao == "7":
            limpar_tela()
            realizar_pagamento(usuario_logado) # Chama a função realizar pagamento
            voltar()

        elif opcao == "0":
            print("\nSaindo...\n")
            limpar_tela()
            return menu_inicial()

        else:
            print("\nOpção inválida!") # Caso digite algo errado


# =================================================================================================
# MENU CLIENTE
# =================================================================================================
def menu_cliente(usuario_logado):
    while True:
        limpar_tela()
        print("\n======= BEM VINDO  =======\n")
        print("1 - Listar Produtos")
        print("2 - Criar Pedido")
        print("3 - Listar Pedidos")
        print("4 - Detalhar pedido")
        print("5 - Realizar pagamento")
        print("0 - Sair\n")

        # Recebe a opção escolhida pelo usuário
        opcao = input("Escolha: ")

        if opcao == "1":
            limpar_tela()
            listar_produtos() # Chama a função listar produtos
            voltar()

        elif opcao == "2":
            limpar_tela()
            criar_pedido(usuario_logado) # Chama a função criar pedido
            voltar()

        elif opcao == "3":
            limpar_tela()
            print("\n====== PEDIDOS ======\n")
            listar_pedidos(usuario_logado) # Chama a função listar pedidos
            voltar()
        
        elif opcao == "4":
            limpar_tela()
            detalhar_pedido(usuario_logado) # Chama a função detalhar pedido
            voltar()
        
        elif opcao == "5":
            limpar_tela()
            realizar_pagamento(usuario_logado) # Chama a função realizar pagamento
            voltar()

        elif opcao == "0":
            print("\nSaindo...\n")
            limpar_tela()
            return menu_inicial()

        else:
            print("\nOpção inválida!") # Caso digite algo errado
