from datetime import datetime,timedelta
from functools import lru_cache
def calcular_valor_boleto(valor, data_vencimento):

    hoje = datetime.now().date()
    data_protesto = data_vencimento + timedelta(days=5)
    dias_atraso = (hoje - data_vencimento).days

    multa = 0
    juros = 0
    taxa_protesto = 0

    if dias_atraso > 0:

        multa = valor * 0.02

        juros = valor * 0.00033 * dias_atraso

    if hoje>=data_protesto:

        taxa_protesto = 50

    total = valor + multa + juros + taxa_protesto

    return round(total,2)
def aplicar_repasse(valor, repasse):
    if repasse == "sim":
        return valor * 0.5
    return valor