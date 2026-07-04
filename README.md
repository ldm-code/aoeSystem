# aoeSystem

- O aoeSystem consiste em um projeto que simula o fluxo de um sistema de transportes universitarios ,onde usuarios comuns podem pagar boletos e marcar presenca em datas especificas,e admins podem controlar outros adms,pagamentos ,usuarios que estao ativos ou nao e presencas.
- A ideia do projeto surgiu em uma conversa no trabalho com um amigo que comentou que iria fazer um sistema nesse estilo,mas para producao.

---

## Funcionalidades:

- Controle de presencas e de datas usando recursos do **python** e do **flask**.
- CRUD com **sqlAlchemy**.
- **HTML**  com Jinja2 para interfaces intuitivas.
- Estlizacao basica com **CSS**.
- **javascript** para funcionalidades de frontend.
- Uso de API **[PoetryDB API](https://github.com/thundercomb/poetrydb)** para retornar poesias aleatoriamente caso o usuario cometa algum erro nas partes de login ou esteja inativo.
- banco de dados **MYSql**
- **ReportLab** para gerar relatorios e boletos em formato pdf.
- **deep_Translator** para traduzir os poemas trazidos pela API.
- **requests** para fazer a ligacao do sistema com a API.
- automacao do fluxo de vizualizacao de historico de presencas com **selenium** para geracao de prints com os dados retornados e prints da tela em caso de erros,alem de geracao de arquivo.txt com os dados que aparecem na tela.
- **Playwright** para automatizar o teste de marcar presencas.
- **Pytest** para a organização de um suite de testes.
- Geracao de pdf com as respectivas presencas para aquela data especifica.
- Calculo de juros do boleto baseado em pesquisas sobre fluxos reais.
- Aplicacao de desconto por repasse caso habilitado.
---

## Tecnologias usadas:

- Python 3.13.2
- Flask
- SQLAlchemy
- Javascript
- HTML
- CSS
- Requests (para conexao com a poetrydb)
- [PoetryDB API](https://github.com/thundercomb/poetrydb)
- Mysql
- reportLab
- deep_translator
- selenium
- pytest

 
---

## Estrutura do projeto:

- aoeSystem/
- │
- ├── manage.py # Arquivo principal para rodar a aplicação
- ├── dados/ # Scripts .sql do banco de dados
- │ │   └──banco_transporte.sql
- ├── testes/ # Script do teste automatico em selenium
- │ │ ├── test_teste_boleto.py # testa o fluxo de cadastro de boletos e gera um .txt com os boletos exibidos na tela
- │ │ ├── test_presencas_dia.py # teste em playwright para testar a parte de marcacao de presencas
- │ │ └── test_relatorios_presenca.py # testa o fluxo de vizualizacao de presencas para um usuario especifico,gerando um .txt das presencas desse usuario
- ├── erros/ # pasta onde irao ser gerados as imagens da tela quando ocorrer erros.
- ├── resultados/ # onde serao geradas imagens da tela quando o teste for bem sucedido.
- ├── registros/ # onde os arquivos.txt gerados pelos testes bem sucedidos ficam 
- ├── static/
- │ ├── css/ # Arquivos de estilo
- │ │   ├── boletos.css
- │ │   ├── usuarios.css
- │ │   ├── cadastro.css
- │ │   ├── inicial_adm.css
- │ │   ├── inicial.css
- │ │   ├── ver_boletos_adm.css
- │ │   ├── presencas.css
- │ │   ├── ver_boletos.css
- │ │   └── login.css
- │ └── js/ # JavaScript
- │ │   ├── cadastro.js
- │ │   └──boletos.js
- ├── services/ # funcoes relacionadas a relatorios e dados da api
- │ │   ├── pdf_service.py
- │ │   └── poetry_service.py
- ├── utils/
- │ │   └── caculos.py
- ├── templates/ # arquivos.html do projeto
- │ │   ├── boletos.html
- │ │   ├── usuarios.html
- │ │   ├── cadastro.html
- │ │   ├── inicial_adm.html
- │ │   ├── inicial.html
- │ │   ├── ver_boletos_adm.html
- │ │   ├── tela_erro.html
- │ │   ├── ver_boletos.html
- │ │   ├── presencas.html
- │ │   └── login.html
- └── README.md

---

## Como executar 

- Apos instalar o Python 3.13 instalado em sua maquina,faca o seguinte processo:

```bash

# clone o repositorio:

git clone https://github.com/ldm-code/aoeSystem.git 
cd aoeSystem

# configure o ambiente:

# no linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate

# Instalacao de frameworks

pip install Flask
pip install Flask-SQLAlchemy
pip install requests
pip install reportlab
pip install deep-translator
pip install selenium
pip install webdriver-manager
pip install PyMySQL
pip install pytest
pip install playwright
playwright install


```

- Apos isso,execute o codigo em **banco_transportes.sql** em seu mysql workbench,faca a conexao com o banco no vs code e em seguida pode
executar o arquivo manage.py e abrir a URL gerada no terminal que ele estara funcionando.

- Para rodar o arquivo de testes automatizados em testes voce deve rodar a aplicacao flask abrir o terminal do powershell no vs code e digitar o segunte comando:
- Para testes.py digite:
```bash
# No Windows:
python testes/teste.py

# no linux:
python3 testes/teste.py

```
- Para teste_boleto.py voce digita:
```bash
# No Windows:
python testes/teste_boleto.py

# no linux:
python3 testes/teste_boleto.py

```
- Para presencas_dia.py voce digita:
```bash
# No Windows:
python testes/presencas_dia.py

# no linux:
python3 testes/presencas_dia.py

```

- Caso queria executar o suite,execute em um terminal separado:

```bash
pytest .
```
**Observacao**:
- para o selenium funcionar corretamente ,voce deve ter o google chrome instalado em sua maquina.caso nao tenha instalado voce deve instalar para funcionar a aplicação.
- caso de algum erro de driver do banco, use apos o igual dentro da aspas "mysql+pymysql antes do //

---

