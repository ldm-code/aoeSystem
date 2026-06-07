from flask import Flask,render_template,request,url_for,redirect,session, send_file
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash,generate_password_hash
import requests
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from deep_translator import GoogleTranslator
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from services.poetry_service import dados_api
from services.pdf_service import gerar_pdf_boleto,gerar_pdf_presencas
from utils.calculos import calcular_valor_boleto,aplicar_repasse
from utils.data import calcular_data_transporte
from dotenv import load_dotenv
import os
from functools import lru_cache

@lru_cache(maxsize=1)
def calcular_data_transporte_cache():
    return calcular_data_transporte()


load_dotenv()
app=Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
# coloque sua senha do banco de dados apos o "root:"
app.config['SQLALCHEMY_DATABASE_URI']  = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)


class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)

    nome = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), nullable=False, unique=True)

    faculdade = db.Column(db.String(120), nullable=False)

    senha = db.Column(db.String(255), nullable=False)

    status = db.Column(db.String(20), nullable=False, default="comum")

    ativo = db.Column(db.Boolean, nullable=False, default=True)
    presencas = db.relationship("Presenca", backref="usuario", lazy=True)
class Presenca(db.Model):
    __tablename__ = "presencas"

    id = db.Column(db.Integer, primary_key=True)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    data_transporte = db.Column(db.Date, nullable=False)

    status = db.Column(
        db.String(20),
        nullable=False,
        default="confirmado"
    )

    data_registro = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    data_cancelamento = db.Column(db.DateTime)

    __table_args__ = (
        db.UniqueConstraint("usuario_id", "data_transporte"),
    )
   
class Boleto(db.Model):
    __tablename__ = "boletos"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False
    )

    tipo = db.Column(
        db.Enum("mensalidade", "multa"),
        nullable=False
    )

    descricao = db.Column(db.String(255))

    valor = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    status = db.Column(
        db.Enum("aberto", "pago", "cancelado"),
        nullable=False,
        default="aberto"
    )

    data_vencimento = db.Column(
        db.Date,
        nullable=False
    )

    data_pagamento = db.Column(
        db.DateTime,
        nullable=True
    )

    data_lancamento = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp(),
        nullable=False
    )

    usuario = db.relationship("Usuario", backref="boletos")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.valor_atualizado = None

def preparar_boletos(boletos):
    for b in boletos:
        b.valor_atualizado = calcular_valor_boleto(float(b.valor), b.data_vencimento)
    return boletos

@app.route('/')
def inicio():
    return render_template("login.html")
@app.route('/cadastrar',methods=['POST'])
def fazer_cadastro():
    nome=request.form.get('nome')
    email=request.form.get('email')
    senha=request.form.get('senha')
    faculdade=request.form.get('faculdade')
    
    texto=dados_api()
    usuario_existente = Usuario.query.filter_by(email=email).first()
    if usuario_existente:
     
        return  render_template("tela_erro.html", mensagem="Usuário já cadastrado",poema=texto)
    senha_hash=generate_password_hash(senha)
    dados=Usuario(nome=nome,email=email,senha=senha_hash,faculdade=faculdade)
    db.session.add(dados)
    db.session.commit()
    return render_template('login.html')
@app.route('/login',methods=['POST'])
def fazer_login():
     email=request.form.get('email').strip()
     senha=request.form.get('senha').strip()
     usuario=Usuario.query.filter_by(email=email).first()
   
     texto=dados_api()
     if not usuario or not check_password_hash(usuario.senha, senha):
           return  render_template("tela_erro.html", mensagem="Login Invalido",poema=texto)
     if usuario and check_password_hash(usuario.senha, senha):
         session['usuario_id'] = usuario.id 
         if usuario.status=="comum" and usuario.ativo==True:
            data_transporte=calcular_data_transporte_cache()
            presenca=Presenca.query.filter_by(data_transporte=data_transporte,usuario_id=usuario.id).first()
            return render_template('inicial.html',presenca_ativa=presenca)
         if usuario.status=="admin" and usuario.ativo==True:
           
            data_transporte = calcular_data_transporte_cache()
         
            presencas_confirmadas = Presenca.query.filter_by(
                 status="confirmado",
                 data_transporte=data_transporte
                    ).all()
            presenca=Presenca.query.filter_by(data_transporte=data_transporte,usuario_id=usuario.id).first()
            return render_template('inicial_adm.html',presenca_ativa=presenca,presencas_confirmadas=presencas_confirmadas)
         elif usuario.ativo==False:
             
              return render_template('tela_erro.html',mensagem="seu usuario esta como inativo",poema=texto)
@app.route('/presenca', methods=['GET', 'POST'])
def marcar_presenca():
     agora=datetime.now()
     usuario_id = session.get("usuario_id")
     if not usuario_id:
        return redirect(url_for("inicio"))
     data_transporte = calcular_data_transporte_cache()
     presenca = Presenca.query.filter_by(
        usuario_id=usuario_id,
        data_transporte=data_transporte,
        
      ).first()
     if request.method=='POST':
       acao=request.form.get('acao')
       
       if acao== "marcar" and not presenca:
     
          nova =Presenca(usuario_id=usuario_id,data_transporte=data_transporte)
          db.session.add(nova)
          db.session.commit()
       elif acao=="cancelar" and presenca and presenca.status == "confirmado":
            presenca.status = "cancelado"
            presenca.data_cancelamento = agora
            db.session.commit()
       elif acao=="marcar" and presenca and presenca.status=="cancelado":
            presenca.status="confirmado"
            presenca.data_cancelamento=None
            db.session.commit()
       return redirect(url_for('marcar_presenca'))
     return render_template("inicial.html", presenca_ativa=presenca)


@app.route('/adm',methods=['GET','POST'])
def marcar_presenca_adm():
     agora=datetime.now()
     usuario_id = session.get("usuario_id")
     relatorio=request.form.get("relatorio")

     if not usuario_id:
        return redirect(url_for("inicio"))
     data_transporte = calcular_data_transporte_cache()
     presenca = Presenca.query.filter_by(
        usuario_id=usuario_id,
        data_transporte=data_transporte,
        
      ).first()
     presencas_confirmadas = Presenca.query.filter_by(
        status="confirmado",
        data_transporte=data_transporte
     ).all()
    
     if request.method=='POST':
       acao=request.form.get('acao')
       
       if acao== "marcar" and not presenca:
     
          nova =Presenca(usuario_id=usuario_id,data_transporte=data_transporte)
          db.session.add(nova)
          db.session.commit()
       elif acao=="cancelar" and presenca and presenca.status == "confirmado":
            presenca.status = "cancelado"
            presenca.data_cancelamento = agora
            db.session.commit()
       elif acao=="marcar" and presenca and presenca.status=="cancelado":
            presenca.status="confirmado"
            presenca.data_cancelamento=None
            db.session.commit()
       return redirect(url_for('marcar_presenca_adm'))
    
     return render_template("inicial_adm.html", presenca_ativa=presenca,presencas_confirmadas=presencas_confirmadas)
@app.route("/relatorio",methods=["GET"])
def gerar_relatorio():
          agora=datetime.now()
          data_transporte=agora.date()
      
          presencas_confirmadas =  (
                       Presenca.query
                       .join(Usuario)
                       .filter(
                            Presenca.status == "confirmado",
                            Presenca.data_transporte == data_transporte
                        )
                        .all()
          )
          pdf= gerar_pdf_presencas(presencas_confirmadas)
          return send_file(
                pdf,
                as_attachment=True,
                download_name=f"Presencas_dia_{data_transporte}.pdf",
                mimetype="application/pdf"
            )
          
@app.route('/tela_promocao')
def tela_promocao():
     usuarios=Usuario.query.all()
     return render_template('usuarios.html',usuarios=usuarios)
@app.route('/alterar_status',methods=['GET','POST'])
def tornar_adm():
     user_id=request.form.get('user_id')
     usuario = Usuario.query.get(user_id)
     if usuario.status=="comum":
          usuario.status="admin"
          db.session.commit()
     elif usuario.status=="admin":
          usuario.status="comum"
          db.session.commit()
     usuarios=Usuario.query.all()
     return render_template('usuarios.html',usuarios=usuarios)
@app.route('/inativo', methods=['GET','POST'])
def inativar():
     id_user=request.form.get('id_user')
     usuario = Usuario.query.get(id_user)
     if usuario.ativo==True:
          usuario.ativo=False
          db.session.commit()
     elif usuario.ativo==False:
          usuario.ativo=True
          db.session.commit()
     usuarios=Usuario.query.all()
     return render_template('usuarios.html',usuarios=usuarios)


@app.route("/presencas", methods=["GET", "POST"])
def listar_presencas():


    if request.method == "POST":

        presenca_id = request.form.get("presenca_id")

        if presenca_id:
            presenca = Presenca.query.get(presenca_id)

            if presenca.status == "confirmado":
                presenca.status = "cancelado"
            else:
                presenca.status = "confirmado"

            db.session.commit()

        return redirect(url_for("listar_presencas"))



    nome = request.args.get("nome")
    acao = request.args.get("acao")

    if nome:
        presencas = (
            Presenca.query
            .join(Usuario)
            .filter(Usuario.nome.ilike(f"%{nome}%"))
            .all()
        )

      
        if acao == "relatorio":

            pdf = gerar_pdf_presencas(presencas)

            return send_file(
                pdf,
                as_attachment=True,
                download_name=f"relatorio_{nome}.pdf",
                mimetype="application/pdf"
            )

    else:
        presencas = Presenca.query.all()
        if acao == "relatorio":
            pdf = gerar_pdf_presencas(presencas)

            return send_file(
                pdf,
                as_attachment=True,
                download_name=f"relatorio_{nome}.pdf",
                mimetype="application/pdf"
            )
    return render_template("presencas.html", presencas=presencas)

@app.route('/listar_boletos_user',methods=['GET','POST'])
def listar_boletos_user():
      id_user=session.get('usuario_id')
      if request.method == "POST":
        
        boleto_id = request.form.get("boleto_id")
        boleto = Boleto.query.get(boleto_id)
        if  boleto and boleto.status == "aberto" :
            
            boleto.status = "pago"
            db.session.commit()
        return redirect(url_for("listar_boletos_user"))
      usuario=Usuario.query.get(id_user)
      
      boletos = Boleto.query.filter_by(usuario_id=id_user, status='aberto').all()

   
      boletos = preparar_boletos(boletos)

      return render_template('ver_boletos.html',boletos=boletos,usuario=usuario)
@app.route("/baixar_boleto/<int:boleto_id>")
def baixar_boleto(boleto_id):
    usuario_id = session.get("usuario_id")
    if not usuario_id:
        return redirect(url_for("inicio"))

    boleto = Boleto.query.get_or_404(boleto_id)


    if boleto.usuario_id != usuario_id:
        return "Acesso negado", 403

    usuario = Usuario.query.get(usuario_id)

    pdf = gerar_pdf_boleto(boleto, usuario)
    
    return send_file(
        pdf,
        as_attachment=True,
        download_name=f"boleto_{boleto.tipo}_{usuario.nome}.pdf",
        mimetype="application/pdf"
    )

@app.route("/marcar_boleto_pago/<int:boleto_id>", methods=["POST"])
def marcar_boleto_pago(boleto_id):
    boleto = Boleto.query.get_or_404(boleto_id)

    if boleto.status != "aberto":
        return redirect(url_for("listar_boletos"))

    boleto.status = "pago"
    boleto.data_pagamento = datetime.now()
    db.session.commit()

    return redirect(url_for("listar_boletos"))

@app.route("/listar_boletos", methods=["GET", "POST"])
def listar_boletos():
    if request.method == "POST":
      
        boleto_id = request.form.get("boleto_id")
        boleto = Boleto.query.get(boleto_id)
        if boleto and boleto.status == "aberto":
            boleto.status = "cancelado"
            db.session.commit()
      
       
              
        return redirect(url_for("listar_boletos"))

    boletos = Boleto.query.all()

    boletos = preparar_boletos(boletos)

       
    return render_template("ver_boletos_adm.html", boletos=boletos)
@app.route("/listar_abertos",methods=["GET",'POST'])
def listar_abertos():
     boletos=Boleto.query.filter_by(status="aberto").all()
   
     boletos = preparar_boletos(boletos)

     return render_template("ver_boletos_adm.html", boletos=boletos)
     
@app.route('/boletos', methods=['GET', 'POST'])
def lancar_boleto():
    usuarios = Usuario.query.all()  
    mensagem=""
    if request.method == 'POST':
        nome_usuario = request.form.get('usuario_nome') 
        tipo = request.form.get('tipo')
        valor_coletado = float (request.form.get('valor'))
        repasse=request.form.get('repasse')
        descricao = request.form.get('descricao')
        data_vencimento = request.form.get('data_vencimento')
        data_passada=datetime.strptime(data_vencimento, "%Y-%m-%d").date()
        data_cadastro = datetime.now()
        data_cadastro_str = data_cadastro.strftime("%Y-%m-%d %H:%M:%S")
        usuario = Usuario.query.filter_by( nome = nome_usuario).first()
        if not usuario:
            return render_template("boletos.html", usuarios=usuarios, mensagem="Usuário não encontrado")

        if not usuario.ativo:
            return render_template("boletos.html", usuarios=usuarios, mensagem="Usuário inativo")

        if data_passada < datetime.now().date():
            return render_template("boletos.html", usuarios=usuarios, mensagem="Data inválida")
        
        if tipo == "mensalidade":
            valor = aplicar_repasse(valor_coletado, repasse)
        else:
            valor = valor_coletado
        boleto = Boleto(
            usuario_id=usuario.id,
            tipo=tipo,
            valor=valor,
            descricao=descricao,
            data_vencimento=data_passada
        )
        db.session.add(boleto)
        db.session.commit()

        return redirect(url_for('listar_boletos')) 

    return render_template('boletos.html', usuarios=usuarios,mensagem=mensagem)

@app.route('/outra_tela')
def outra_tela():
    return render_template('cadastro.html')
if __name__=='__main__':
        app.run(debug=False)
