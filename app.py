from flask import Flask, render_template, request, redirect, url_for
from database import Contatos, Users, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "youthSpace"
app.secret_key = os.urandom(24)
mensagem = ''
@app.route("/")
def index():
    contatos = session.query(Contatos).all()
    global mensagem
    return render_template("index.html", contatos=contatos)

@app.route("/salvar_contato", methods=['POST'])
def add_contato():
    email = request.form['email']
    contato = session.query(Contatos).filter_by(email=email).first()
    if contato:
        global mensagem
        mensagem = 'Email já cadastrado!'
        return redirect(url_for("#add_modal_alert"))
    else:
        novo_contato = Contatos(
            nome_contato=request.form['nome'],
            email=email,
            celular=request.form['celular'],
            celular_alt=request.form.get("celular_alt", ""),
            tags=request.form['tags'],
        )
        session.add(novo_contato)
        session.commit()
        return redirect("/")

@app.route("/deletar_contato", methods=['POST'])
def deletarContato():
    email = request.form['email']
    contato = session.query(Contatos).filter_by(email=email).first()
    if contato:
        session.delete(contato)
        session.commit()
    return redirect("/")

@app.route("/atualizar_contato", methods=['POST'])
def atualizarContato():
    contato_id = request.form['id_contato']
    contato = session.query(Contatos).get(contato_id)
    if contato:
        contato.nome_contato = request.form['nome']
        contato.email = request.form['email']
        contato.celular = request.form['celular']
        contato.celular_alt = request.form.get("celular_alt", "")
        contato.tags = request.form['tags']
        session.commit()
    return redirect("/")

@app.route("/registrar", methods=['GET', 'POST'])
def registrar_se():
    if request.method == 'POST':

        senha = request.form['password']

        '''if user:
            global mensagem
            mensagem = 'Nome de usuario indisponivel!'
            return redirect(url_for("#add_modal_alert", mensagem=mensagem))
        elif senha != confirmacao_senha:
            mensagemSenha = 'As senhas não são iguais!'
            return redirect(url_for("#add_modal_alert", mensagemSenha=mensagemSenha))
        else:'''

        hashed_password = generate_password_hash(senha)
        print('hash code', hashed_password)
        novo_usuario = Users(
            nome=request.form['nome'],
            username=request.form['user'],
            senha=hashed_password
        )
        session.add(novo_usuario)
        session.commit()
        return redirect("/login")
    return render_template('/registro.html')

@app.route("/login")
def login():
    if request.method == 'POST':
        username = request.form['user']
    return render_template("Login.html")


if __name__ == "__main__":
    app.run()

