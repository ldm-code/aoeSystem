# aoeSystem

- O aoeSystem consiste em um projeto que simula o fluxo de um sistema de transportes universitarios ,onde usuarios comuns podem pagar boletos e maracar presenca em datas 
especificas,e admins podem controlar outros adms,pagamentos ,usuarios que estao ativos ou nao e presencas.
- A ideia do projeto surgiu em uma conversa no trabalho com um amigo que comentou que iria fazer um sistema nesse estilo,mas para producao.
---

## Funcionalidades:

- Controle de presencas e de datas usando recursos do **python** e do **flask**.
- CRUD com **sqlAlchemy**.
- **HTML**  com Jinja2 para interfaces intuitivas.
- Estlizacao basica com **CSS**
- **javascript** para funcionalidades de frontend
- Uso de API **[PoetryDB API](https://github.com/thundercomb/poetrydb)** para retornar poesias aleatoriamente caso o usuario cometa algum erro nas partes de login ou esteja inativo.
- banco de dados **MYSql**
- **ReportLab** para gerar os boletos em formato pdf
- **deep_Translator** para traduzir os poemas trazidos pela API
- **requests** para fazer a ligacao do sistema com a API

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

## Estrutura do projeto:

- aoeSystem/
- │
- ├── manage.py # Arquivo principal para rodar a aplicação
- ├── dados/ # Scripts .sql do banco de dados
- │ │   └──banco_transporte.sql
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
- ├── templates/ # arquivos.html do projeto
- │ │   ├── boletos.html
- │ │   ├── usuarios.html
- │ │   ├── cadastro.html
- │ │   ├── inicial_adm.html
- │ │   ├── inicial.html
- │ │   ├── ver_boletos_adm.html
- │ │   ├── ver_boletos.html
- │ │   ├── presencas.html
- │ │   └── login.html
- └── README.md

## Como executar 

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


```

- apos isso,execute o codigo em **banco_transportes.sql** em seu mysql workbench,faca a conexao com o banco no vs code e em seguida pode
executar o arquivo manage.py e abrir a URL gerada no terminal que ele estara funcionando
