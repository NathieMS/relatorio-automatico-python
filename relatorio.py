import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

EMAIL      = "nathaliemenezes.adv@gmail.com"
SENHA      = "sua-senha-de-app-aqui"
DESTINATARIO = "nathaliemenezes.adv@gmail.com"

caminho_csv = os.path.join(os.path.expanduser("~"),"OneDrive", "Desktop", "vendas.csv")

vendas = []
with open(caminho_csv, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for linha in reader:
        vendas.append({
            "produto":    linha["produto"],
            "quantidade": int(linha["quantidade"]),
            "valor":      float(linha["valor_unitario"]),
        })

total_geral = sum(v["quantidade"] * v["valor"] for v in vendas)
mais_vendido = max(vendas, key=lambda v: v["quantidade"])

linhas_tabela = ""
for v in vendas:
    subtotal = v["quantidade"] * v["valor"]
    linhas_tabela += f"  {v['produto']:<15} {v['quantidade']:>4} un   R$ {subtotal:>9.2f}\n"

corpo = f"""Relatório de Vendas
===================

{linhas_tabela}
-----------------------------------
Total geral:       R$ {total_geral:.2f}
Produto destaque:  {mais_vendido['produto']} ({mais_vendido['quantidade']} unidades)

Relatório gerado automaticamente por Python.
"""

msg = MIMEMultipart()
msg["From"]    = EMAIL
msg["To"]      = DESTINATARIO
msg["Subject"] = "Relatório de Vendas - Automático"
msg.attach(MIMEText(corpo, "plain"))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
    servidor.login(EMAIL, SENHA)
    servidor.sendmail(EMAIL, DESTINATARIO, msg.as_string())

print("E-mail enviado com sucesso!")