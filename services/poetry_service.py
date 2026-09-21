
import requests
from deep_translator import GoogleTranslator
from deep_translator.exceptions import TooManyRequests
from functools import lru_cache


def traduzir_texto_longo(texto, tradutor):
    palavras = texto.split()
    resultado = []
    bloco = ""

    try:
        for palavra in palavras:
            if len(bloco) + len(palavra) + 1 < 4500:
                bloco += " " + palavra
            else:
                resultado.append(tradutor.translate(bloco))
                bloco = palavra

        if bloco:
            resultado.append(tradutor.translate(bloco))

        return " ".join(resultado)

    except TooManyRequests:
        return "Não foi possível traduzir o poema agora. Tente novamente mais tarde."

    except Exception:
        return "Ocorreu um erro ao traduzir o poema."


@lru_cache(maxsize=10)
def dados_api():
    try:
        res = requests.get(
            "https://poetrydb.org/random",
            timeout=5
        )

        if res.status_code != 200:
            return "Erro ao buscar poema."

        dados = res.json()

    except requests.RequestException:
        return "Erro de conexão com API."

    except ValueError:
        return "Erro ao interpretar JSON."

    try:
        texto = "\n".join(dados[0]["lines"])

        tradutor = GoogleTranslator(
            source="auto",
            target="pt"
        )

        return traduzir_texto_longo(texto, tradutor)

    except Exception:
        return "Não foi possível carregar o poema. Tente novamente mais tarde."