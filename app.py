from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

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