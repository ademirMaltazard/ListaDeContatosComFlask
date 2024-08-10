from flask import Flask, render_template, request, redirect, url_for
from database import Contatos, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "YOUTHSPACE"
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

if __name__ == "__main__":
    app.run()

