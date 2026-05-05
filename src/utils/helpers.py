import os # Biblioteca padrão para interagir com o sistema operacional (ex: limpar terminal)

# =================================================================================================
# LIMPAR TELA
# =================================================================================================
def limpar_tela():
    # Limpa o terminal dependendo do sistema operacional:
    # Windows -> cls
    # Linux/mac -> clear

    os.system('cls' if os.name == 'nt' else 'clear')


# =================================================================================================
# Voltar a tela anterior
# =================================================================================================
def voltar():
    while True:
            # Solicita a entrada do usuário
            resp = input("\nDigite 0 (zero) para voltar: ")

            if resp == '0':
                print("\nSaindo...")
                break
                        
            # Caso contrário, informa erro e repete o loop
            print("\nOpçao inválida!")


# =================================================================================================
# MENSAGEM CONTINUAR/SAIR
# =================================================================================================
def perguntar_sn(mensagem):
    # Função garante que o usuário digite apenas 's' ou 'n'
    
    # Parametro:
    # - Mensagem de texto que será exibido para o usuário

    # Retorno:
    # 's' para continuar
    # 'n' para sair
    # (sempre validado)

    while True:
        # Solicita a entrada do usuário
        resp = input(mensagem)

        # Remove espaços extras e transforma em minúsculo
        resp = resp.strip().lower()

        # Verifica se a resposta é válida
        if resp in ['s', 'n']:
            return resp # Retorna apenas se for válido
        
        # Caso contrário, informa erro e repete o loop
        print("\nOpçao inválida! \nDigite apenas 's' ou 'n'.")


# =================================================================================================
# MENSAGEM CONTINUAR/SAIR
# =================================================================================================
def perguntar_sn(mensagem):
    # Função garante que o usuário digite apenas 's' ou 'n'
    
    # Parametro:
    # - Mensagem de texto que será exibido para o usuário

    # Retorno:
    # 's' para continuar
    # 'n' para sair
    # (sempre validado)

    while True:
        # Solicita a entrada do usuário
        resp = input(mensagem)

        # Remove espaços extras e transforma em minúsculo
        resp = resp.strip().lower()

        # Verifica se a resposta é válida
        if resp in ['s', 'n']:
            return resp # Retorna apenas se for válido
        
        # Caso contrário, informa erro e repete o loop
        print("\nOpçao inválida! \nDigite apenas 's' ou 'n'.")