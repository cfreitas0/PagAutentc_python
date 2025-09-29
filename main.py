
from flask import Flask, render_template, redirect, request, flash, url_for
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cesar'

@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():

    nome = request.form.get('nome')
    senha = request.form.get('senha')

    with open('D:/PagAutentc_python/usuarios.json') as usuario_temporaria:
        usuarios = json.load(usuario_temporaria)
        cont = 0    
        for usuario in usuarios:
            cont += 1
            if nome == 'adm' and senha == '222':
                return render_template('admin.html')
            
            if usuario["nome"] == nome and usuario["senha"] == senha:
                return render_template('usuario.html')
            
            if cont >= len(usuarios):
                flash('USUARIO INVALIDO')
                return redirect('/')

    print(usuarios)
    return "Login processado!"


if __name__ in "__main__":
    app.run(debug=True)