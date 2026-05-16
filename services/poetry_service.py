import requests
from deep_translator import GoogleTranslator
from functools import lru_cache
def traduzir_texto_longo(texto, tradutor):
    palavras = texto.split()
    resultado = []
    bloco = ""

    for palavra in palavras:
        if len(bloco + " " + palavra) < 4500:
            bloco += " " + palavra
        else:
            resultado.append(tradutor.translate(bloco))
            bloco = palavra

    if bloco:
        resultado.append(tradutor.translate(bloco))

    return " ".join(resultado)
@lru_cache(maxsize=10)
def dados_api():
    try:
        res = requests.get("https://poetrydb.org/random", timeout=5)

        if res.status_code != 200:
            return "Erro ao buscar poema."

        dados = res.json()

    except requests.RequestException:
        return "Erro de conexão com API."

    except ValueError:
        return "Erro ao interpretar JSON."

    texto = "\n".join(dados[0]['lines'])
   

    tradutor = GoogleTranslator(source="auto", target="pt")

    if len(texto) < 4500:
        return traduzir_texto_longo(texto, tradutor)

    return traduzir_texto_longo(texto, tradutor)