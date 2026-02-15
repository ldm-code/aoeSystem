from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import datetime

def test():
           driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()))
           def teste(driver,by,selector,timeout=30):
                   return  WebDriverWait(driver,timeout).until(EC.visibility_of_element_located((by,selector)))
           try:
                  timestamp= datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                 
                  try:
                    print("abriu")
                    driver.get("http://127.0.0.1:5000/")
                  except Exception as e:
                       driver.save_screenshot(f"erros/erro_{timestamp}.png")
                       print(f"erro ,{e}")  
                  print("abrindo login")
                  teste(driver,By.NAME,"email").send_keys("joao@gmail.com") #altere essa linha para algum email de usuario cujo status seja de adm
                  teste(driver,By.NAME,"senha").send_keys("123") #altere para a senha do usuario admin no email acima
                  teste(driver,By.ID,"btn").click()
                  print("vendo presenca")
                  teste(driver,By.ID,"presentes").click()
                  teste(driver,By.NAME,"nome").send_keys("joao")
                  teste(driver,By.ID,"buscar").click()
                  print("buscando a presenca")
                  driver.save_screenshot(f"resultados/teste_{timestamp}.png")
                  presencas=driver.find_elements(By.CSS_SELECTOR,"body table")
                  print("achou elemento")
                  with open("registros/presencas.txt", "w", encoding="utf-8") as f:
                           pass  

                  with open("registros/presencas.txt","a",encoding="utf-8") as arquivo:
                    try:
                       for m in presencas:
                          print(m.text)
                          arquivo.write(m.text +"\n")
                    except Exception as e:
                          print(f"nao funcionou, {e}")
                          driver.save_screenshot(f"erros/erro_{timestamp}.png")
                  print("teste bem sucedido")
           except Exception as e:
                       driver.save_screenshot(f"erros/erro_{timestamp}.png")
                       print(f"erro ,{e}")          

           finally:
                               driver.quit()
if __name__=="__main__":
        test()