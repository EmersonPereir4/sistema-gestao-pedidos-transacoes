# =================================================================================================
# VALIDAÇÃO DE USUÁRIO
# =================================================================================================
from menu import menu_inicial, menu_admin, menu_funcionario, menu_cliente

# =================================================================================================
# EXECUÇÃO DO PROGRAMA
# =================================================================================================
if __name__ == "__main__":
    
    usuario_logado = menu_inicial()

    if not usuario_logado:
        print("Encerramento do sistema...")
        exit()

    tipo = usuario_logado[2]

    if tipo == "ADMIN":
        menu_admin(usuario_logado)
    
    elif tipo == "FUNCIONARIO":
        menu_funcionario(usuario_logado)
    
    else:
        menu_cliente(usuario_logado)