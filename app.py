from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///conteudo.sqlite3'
db = SQLAlchemy(app)

class Admin(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    pagina = db.Column(db.String(150))
    texto = db.Column(db.String(250))

    def __init__(self, pagina, texto):
        self.pagina = pagina
        self.texto = texto

class Produtos(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    produto = db.Column(db.String(150))
    descricao = db.Column(db.String(250))
    valor = db.Column(db.String(10))

    def __init__(self, produto, descricao, valor):
        self.produto = produto
        self.descricao = descricao
        self.valor = valor

@app.before_first_request
def create_tables():
    db.create_all()

@app.route("/")
def index():
    produto  = Produtos.query.all()
    return render_template("index.html", produto = produto)

@app.route("/admin")
def admin():
    conteudo = Admin.query.all()
    produto  = Produtos.query.all()
    return render_template("admin.html", conteudo = conteudo, produto = produto)

@app.route("/add", methods = ['GET', 'POST'])
def add():
    if request.method == 'POST':
        conteudo = Admin(request.form['pagina'], request.form['texto'])
        db.session.add(conteudo)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template("add.html")

@app.route("/addprod", methods = ['GET', 'POST'])
def addprod():
    if request.method == 'POST':
        produto = Produtos(request.form['produto'], request.form['descricao'],
         request.form['valor'])
        db.session.add(produto)
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template("addprod.html")

@app.route("/edit/<int:id>", methods = ['GET', 'POST'])
def edit(id):
    conteudo = Admin.query.get(id)
    if request.method == 'POST':
        conteudo.pagina = request.form['pagina']
        conteudo.texto = request.form['texto']
        db.session.commit()
        return redirect(url_for('admin'))
    return render_template("edit.html", conteudo = conteudo)

@app.route("/editprod/<int:id>", methods = ['GET', 'POST'])
def editprod(id):
    produto = Produtos.query.get(id)
    if request.method == 'POST':
        produto.produto = request.form['produto']
        produto.descricao = request.form['descricao']
        produto.valor = request.form['valor']
        db.session.commit()
        return redirect(url_for('admin')) 
    return render_template("editprod.html", produto = produto)

@app.route("/delete/<int:id>")
def delete(id):
    conteudo = Admin.query.get(id)
    db.session.delete(conteudo)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route("/deleteprod/<int:id>")
def deleteprod(id):
    produto = Produtos.query.get(id)
    db.session.delete(produto)
    db.session.commit()
    return redirect(url_for('admin'))

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/quemsomos")
def quemsomos():
    return render_template("quemsomos.html")

@app.route("/suporte")
def suporte():
    return render_template("suporte.html")

@app.route("/assinar")
def assinar():
    produto = request.args.get("prod")
    valor = request.args.get("valor")
    return render_template("assinar.html", prod = produto, valor = valor)

@app.route("/obrigado")
def obrigado():

    nome = request.args.get("nome")
    email = request.args.get("email")
    mensagem = request.args.get("mensagem")
    return render_template("obrigado.html", nome = nome, email = email, mensagem = mensagem)

if __name__ == "__main__":
    app.run()