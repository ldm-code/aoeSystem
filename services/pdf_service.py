from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def gerar_pdf_boleto(boleto, usuario):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 800, "BOLETO DE PAGAMENTO")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 760, f"Nome: {usuario.nome}")
    pdf.drawString(50, 740, f"E-mail: {usuario.email}")
    pdf.drawString(50, 720, f"Faculdade: {usuario.faculdade}")

    pdf.drawString(50, 680, f"Tipo: {boleto.tipo}")
    pdf.drawString(50, 660, f"Descrição: {boleto.descricao}")
    pdf.drawString(50, 640, f"Valor: R$ {boleto.valor}")
    pdf.drawString(50, 620, f"Vencimento: {boleto.data_vencimento}")
    pdf.drawString(50, 600, f"Status: {boleto.status}")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return buffer


def gerar_pdf_presencas(presencas):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    styles = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph("Relatório de Presenças", styles["Heading1"]))
    elementos.append(Spacer(1, 12))

    dados = [["Usuário", "Data", "Status"]]

    for p in presencas:
        dados.append([
            p.usuario.nome,
            p.data_transporte.strftime("%d/%m/%Y"),
            p.status
        ])

    tabela = Table(dados)
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
    ]))

    elementos.append(tabela)

    doc.build(elementos)
    buffer.seek(0)
    return buffer