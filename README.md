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
- Uso de API **poetrydb** para retornar poesias aleatoriamente caso o usuario cometa algum erro nas partes de login ou esteja inativo.
- link da API usada nesse projeto : [PoetryDB API](https://github.com/thundercomb/poetrydb)
-banco de dados **MYSql**

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




