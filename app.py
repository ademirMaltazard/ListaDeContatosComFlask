from flask import Flask, render_template, request, redirect, url_for, session as flask_session
from database import Contatos, Users, session
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "youthSpace"
app.secret_key = os.urandom(24)
mensagem = ''
@app.route("/")
def index():
    if 'id_user' not in flask_session:
        return redirect('/login')
    id_user = flask_session["id_user"]
    user = session.query(Users).filter_by(id_user=id_user).first()
    contatos = session.query(Contatos).filter_by(id_user=id_user).all()
    return render_template("index.html", contatos=contatos, user=user)

@app.route("/salvar_contato", methods=['POST'])
def add_contato():
    email = request.form['email']
    user = flask_session["id_user"]
    contato = session.query(Contatos).filter_by(id_user=user, email=email).first()
    print(contato)

    if "id_user" not in flask_session:
        return redirect("/login")

    if not contato:
        id_user = flask_session["id_user"]
        novo_contato = Contatos(
            nome_contato=request.form['nome'],
            email=email,
            celular=request.form['celular'],
            celular_alt=request.form.get("celular_alt", ""),
            tags=request.form['tags'],
            id_user=id_user
        )
        session.add(novo_contato)
        session.commit()
        return redirect("/")
    return render_template("index.html")

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
        confirmacao_senha = request.form['confirm_password']
        user = session.query(Users).filter_by(username=request.form["user"]).first()
        print("user: ", user)
        print("aaaaaaaaaaaaaaaaa")
        if user:
            user_return = 'Nome de usuario indisponivel!'
            return render_template("/registro.html", user_return=user_return)
        elif senha != confirmacao_senha:
            password_return = 'As senhas não são iguais!'
            return render_template("/registro.html", password_return=password_return)
        else:
            hashed_password = generate_password_hash(senha)
            print("-"*20)
            print('hash code', hashed_password)
            print(request.form['user'])
            novo_usuario = Users(
                nome=request.form['nome'],
                username=request.form['user'],
                senha=hashed_password
            )
            session.add(novo_usuario)
            session.commit()
            return redirect("/login")
    return render_template('/registro.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']
        user = session.query(Users).filter_by(username=username).first()

        if user and check_password_hash(user.senha, password):
            flask_session["id_user"] = user.id_user
            print("ativando SESSION: ", flask_session)
            return redirect("/")
        else:
            error = "Login falhou, confira suas credenciais ou "
            register_link = "<a href='/registrar'>registre-se aqui</a>"
            return render_template('Login.html', error=error + register_link)
    return render_template("Login.html")

@app.route("/logout", methods=['GET'])
def logout():
    print("Antes: ", flask_session["id_user"])
    flask_session.pop('id_user', None)
    return redirect("/login")


if __name__ == "__main__":
    app.run()


