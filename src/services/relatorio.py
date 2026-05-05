from db.conexao import conectar # Responsável por criar e retornar uma conexão com o banco de dados
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from decimal import Decimal
from datetime import datetime


def gerar_relatorio_pdf(usuario_logado):
    conexao = conectar()
    cursor = conexao.cursor()

    try:
        print("\n===== RELATÓRIO =====")

        # Controle de acesso
        tipo = usuario_logado[2]

        if tipo != "ADMIN":
            print("\nApenas ADMIN pode acessar relatórios")
            return
        
        # Escolha do período
        print("\nTipo do relatório:")
        print("\n1 - Mensal")
        print("2 - Ultimos 15 dias")

        opcao = input("\nEscolha uma opcao: ")

        if opcao == "1":
            filtro_data = "AND DATE_TRUNC('month', data_pagamento) = DATE_TRUNC('month', CURRENT_DATE)"
            descricao_periodo = "Relatório Mensal"
        elif opcao == "2":
            filtro_data = "AND data_pagamento >= CURRENT_DATE - INTERVAL '15 days'"
            descricao_periodo = "Últimos 15 dias"
        else:
            print("\nOpção inválida!")
            return

        # Iniciar PDF
        doc = SimpleDocTemplate("relatorio.pdf")
        styles = getSampleStyleSheet()
        elementos = []

        # Título
        elementos.append(Paragraph("Relatório Geral do Sistema", styles["Title"]))
        elementos.append(Spacer(1, 12))

        # Data e período
        data_atual = datetime.now().strftime("%d/%m/%y %H:%M")
        elementos.append(Paragraph(f"Gerado em: {data_atual}", styles["Normal"]))
        elementos.append(Paragraph(f"Período: {descricao_periodo}", styles["Normal"]))
        elementos.append(Spacer(1, 12))

        # Total Faturado
        cursor.execute(f"""Select SUM(p.valor_total)
                       FROM pedido p
                       Join pagamento pg ON p.id_pedido = pg.id_pedido
                       WHERE p.status = 'PAGO' {filtro_data}""")
        
        total = cursor.fetchone()[0] or Decimal("0")

        elementos.append(Paragraph(f"Total faturado: R$ {total:.2f}", styles["Normal"]))
        elementos.append(Spacer(1, 12))

        # Total de Pedidos
        cursor.execute(f"""SELECT COUNT(DISTINCT p.id_pedido)
                       FROM pedido p
                       JOIN pagamento pg ON p.id_pedido = pg.id_pedido
                       WHERE p.status = 'PAGO' {filtro_data}""")
        
        total_pedidos = cursor.fetchone()[0] or 0

        elementos.append(Paragraph(f"Pedidos pagos: {total_pedidos}", styles["Normal"]))
        elementos.append(Spacer(1, 12))

        # Tiket Médio
        tiket_medio = Decimal("0")

        if total_pedidos > 0:
            tiket_medio = total / total_pedidos

        elementos.append(Paragraph(f"Tiket médio: R$ {tiket_medio:.2f}", styles["Normal"]))
        elementos.append(Spacer(1, 12))

        # Formas de Pagamento
        elementos.append(Paragraph("Formas de pagamento:", styles["Heading2"]))

        cursor.execute(f"""SELECT pg.forma_pagamento, COUNT(*), SUM(pg.valor_pago)
                       FROM pagamento pg
                       WHERE 1 = 1 {filtro_data}
                       GROUP BY pg.forma_pagamento
                       ORDER BY COUNT(*) DESC""")
        
        formas = cursor.fetchall()

        for forma, quantidade, total_forma in formas:
            texto = f"{forma} -> {quantidade} pagamentos -> R$ {total_forma:.2f}"
            elementos.append(Paragraph(texto, styles["Normal"]))

        elementos.append(Spacer(1, 12))

        #Forma mais usada
        if formas:
            forma_top = formas[0][0]
            elementos.append(Paragraph(f"Forma mais utilizada: {forma_top}", styles["Normal"]))

        # Gerar PDF
        doc.build(elementos)

        print("\nRelatório gerado com sucesso!")

    except Exception as erro:
        print("Erro ao gerar relatório: ", erro)

    finally:
        cursor.close()
        conexao.close()