from playwright.sync_api import sync_playwright,expect
import time
import os

def test():
          emails=["roblox@gmail.com","noal@gmail.com","bruna@gmail.com",
                  "joana@gmail.com","duda@gmail.com","ana@gmail.com","helen@gmail.com"]
          with sync_playwright() as p:
                    browser=p.chromium.launch(headless=True)

                    pagina=browser.new_page()
                    
                    for email in emails:
                              pagina.goto("http://127.0.0.1:5000/")
                              pagina.fill("[name='email']",email)
                              pagina.fill("[name='senha']",'123')
                              pagina.get_by_role("button",name="Entrar").click()
                              pagina.locator("text=Pagar boletos:").click()

                              boletos=pagina.locator("[name='acao']").count()
                              print(boletos)
                              
                              for boleto in range(boletos):
                                
                                      boleto=pagina.locator("[name='acao']").nth(0)
                                     
                                      boleto.click()
                                      pagina.wait_for_timeout(500)
                              #         boletos_clique.pop(0)

                    browser.close()     
                    
if __name__=="__main__":
        test()