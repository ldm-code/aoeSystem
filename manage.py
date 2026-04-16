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



app=Flask(__name__)
app.secret_key = "minha_chave_super_secreta_123"
# coloque sua senha do banco de dados apos o "root:"
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:coloque sua senha do banco de dados@127.0.0.1/aue"
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
def gerar_pdf_boleto(boleto, usuario):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 800, "BOLETO DE PAGAMENTO")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(50, 760, f"Nome: {usuario.nome}")
    pdf.drawString(50, 740, f"E-mail: {usuario.email}")
    pdf.drawString(50, 720, f"Faculdade: {usuario.faculdade}")

    pdf.drawString(50, 680, f"Tipo: {boleto.tipo}")
    pdf.drawString(50, 660, f"Descrição: {boleto.descricao}")
    valor_para_pdf = calcular_valor_boleto(float(boleto.valor), boleto.data_vencimento)
    pdf.drawString(50, 640, f"Valor: R$ {valor_para_pdf}")
    pdf.drawString(50, 620, f"Vencimento: {boleto.data_vencimento}")
    pdf.drawString(50, 600, f"Status: {boleto.status}")

    pdf.drawString(50, 560, f"Data de emissão: {boleto.data_lancamento.strftime('%d/%m/%Y')}")

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    return buffer
def gerar_pdf_presencas(presencas):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elementos = []

    styles = getSampleStyleSheet()

    titulo = Paragraph("Relatório de Presenças", styles["Heading1"])
    elementos.append(titulo)
    elementos.append(Spacer(1, 12))

    dados = [["Data", "Status"]]
    for presenca in presencas:
        dados.append([
            presenca.usuario.nome,
            presenca.data_transporte.strftime("%d/%m/%Y"),
            presenca.status
        ])

    tabela = Table(dados)
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.grey),
        ("GRID", (0,0), (-1,-1), 1, colors.black),
    ]))

    elementos.append(tabela)

    doc.build(elementos)
    buffer.seek(0)
    return buffer
with app.app_context():
    db.create_all()
def dados_api():
     try:
       res=requests.get("https://poetrydb.org/random")
       dados=res.json()
     except requests.RequestException:
         dados= [{"lines": ["clique na seta acima a esquerda para retornar."]}]
     texto="<br>".join(dados[0]['lines'])
     tamanho_max = 4000
     blocos = [texto[i:i+tamanho_max] for i in range(0, len(texto), tamanho_max)]

     tradutor = GoogleTranslator(source="auto", target="pt")
     traducao = []

     for bloco in blocos:
        traducao.append(tradutor.translate(bloco))

     return "<br>".join(traducao)
def calcular_valor_boleto(valor, data_vencimento):

    hoje = datetime.now().date()
    data_protesto = data_vencimento + timedelta(days=5)
    dias_atraso = (hoje - data_vencimento).days

    multa = 0
    juros = 0
    taxa_protesto = 0

    if dias_atraso >= 0:

        multa = valor * 0.02

        juros = valor * 0.00033 * dias_atraso

    if hoje>=data_protesto:

        taxa_protesto = 50

    total = valor + multa + juros + taxa_protesto

    return round(total,2)
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
     
        return f"<h2>Cadastro ja existente,clique na seta no canto superior esquerdo e cadastre um acesso valido:</h2><p>{texto}</p>"
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
          return f"<h2>cadastro inexistente,clique na seta no canto superior esquerdo e cadastre um acesso valido:</h2><p>{texto}</p>"
     if usuario and check_password_hash(usuario.senha, senha):
         session['usuario_id'] = usuario.id 
         if usuario.status=="comum" and usuario.ativo==True:
            agora=datetime.now()
            data_transporte = agora.date()
            if agora.hour >= 17:
                 data_transporte += timedelta(days=1)
            if data_transporte.weekday() == 5:     
                  data_transporte += timedelta(days=2)
            elif data_transporte.weekday() == 6:   
                     data_transporte += timedelta(days=1)
            presenca=Presenca.query.filter_by(data_transporte=data_transporte,usuario_id=usuario.id).first()
            return render_template('inicial.html',presenca_ativa=presenca)
         if usuario.status=="admin" and usuario.ativo==True:
            agora=datetime.now()
            data_transporte = agora.date()
            if agora.hour >= 17:
                 data_transporte += timedelta(days=1)
            if data_transporte.weekday() == 5:     
                  data_transporte += timedelta(days=2)
            elif data_transporte.weekday() == 6:   
                     data_transporte += timedelta(days=1)
            presencas_confirmadas = Presenca.query.filter_by(
                 status="confirmado",
                 data_transporte=data_transporte
                    ).all()
            presenca=Presenca.query.filter_by(data_transporte=data_transporte,usuario_id=usuario.id).first()
            return render_template('inicial_adm.html',presenca_ativa=presenca,presencas_confirmadas=presencas_confirmadas)
         elif usuario.ativo==False:
             
              return f"<h1>Parece que voce ja se formou,receba esse poema em sua homenagem :)</h1> <p>{texto}</p>"
@app.route('/marcar',methods=['GET','POST'])
def marcar_presenca():
     agora=datetime.now()
     usuario_id = session.get("usuario_id")
     if not usuario_id:
        return redirect(url_for("inicio"))
     data_transporte = agora.date()
     if agora.hour >= 17:
           data_transporte += timedelta(days=1)
     if data_transporte.weekday() == 5:     
            data_transporte += timedelta(days=2)
     elif data_transporte.weekday() == 6:   
             data_transporte += timedelta(days=1)
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
     data_transporte = agora.date()
     if agora.hour >= 17:
           data_transporte += timedelta(days=1)
     if data_transporte.weekday() == 5:     
            data_transporte += timedelta(days=2)
     if data_transporte.weekday() == 6:   
             data_transporte += timedelta(days=1)
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

      for boleto in boletos:
         boleto.valor_atualizado= calcular_valor_boleto(
                float(boleto.valor),
                boleto.data_vencimento
             )
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
    for boleto in boletos:
       boleto.valor_atualizado = calcular_valor_boleto(
           float(boleto.valor),
           boleto.data_vencimento
        )
       
    return render_template("ver_boletos_adm.html", boletos=boletos)
@app.route("/listar_abertos",methods=["GET",'POST'])
def listar_abertos():
     boletos=Boleto.query.filter_by(status="aberto")
     for boleto in boletos:
       boleto.valor_atualizado = calcular_valor_boleto(
           float(boleto.valor),
           boleto.data_vencimento
        )
     return render_template("ver_boletos_adm.html",boletos=boletos)
@app.route('/boletos', methods=['GET', 'POST'])
def lancar_boleto():
    usuarios = Usuario.query.all()  

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
        poema=dados_api()
        if not usuario:
            return "Usuário não encontrado", 400
        if not usuario.ativo:
             return f"<h2>Acao invalida,usuario inativo(clique na seta no canto esquerdo acima):</h2><p>{poema}</p>"
        elif data_vencimento<=data_cadastro_str:
                  return f"<h2>data de vencimento nao pode ser inferior a data de hoje,clique na seta no canto superior esquerdo :</h2><p>{poema}</p>"
        if repasse=="sim":
             valor=valor_coletado*0.5
        elif repasse=="nao":
             valor=valor_coletado
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

    return render_template('boletos.html', usuarios=usuarios)

@app.route('/outra_tela')
def outra_tela():
    return render_template('cadastro.html')
if __name__=='__main__':
        app.run(debug=True)
