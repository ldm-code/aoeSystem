from playwright.sync_api import sync_playwright,expect
import time
import os

def gerar_txt(valor):
    pasta = "resultados"
    
    # cria a pasta se não existir
    os.makedirs(pasta, exist_ok=True)

    caminho_arquivo = os.path.join(pasta, "arquivo.txt")

    with open(caminho_arquivo, "a", encoding="utf-8") as arquivo:
        arquivo.write(valor + "\n")
def test():
 emails=["joao@gmail.com","duda@gmail.com","joana@gmail.com"]
 with sync_playwright() as p:
          browser=p.chromium.launch(headless=False)
          pagina=browser.new_page()
          for email in emails:
             pagina.goto("http://127.0.0.1:5000/")
             pagina.fill("[name='email']",email)     
             pagina.fill("[name='senha']","123")
             pagina.get_by_role('button',name="Entrar").click()
             pagina.locator('[name="acao"]').click()
             gerar_txt(email)
             print(f'testado email de {email}')

          browser.close()
if __name__=="__main__":
        test()