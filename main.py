
from flask import Flask, render_template, redirect, request, flash, url_for
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cesar'

logado = False

@app.route('/')
def home():
    global logado
    logado = False
    return render_template('login.html')

@app.route('/adm')
def adm():
    if logado == True:
        with open('D:/proj_login/usuarios.json') as usuario_temporaria:
            usuarios = json.load(usuario_temporaria)
        return render_template('admin.html', usuarios=usuarios)
    if logado == False:
        return redirect('/')

@app.route('/login', methods=['POST'])
def login():

    global logado

    nome = request.form.get('nome')
    senha = request.form.get('senha')

    with open('D:/proj_login/usuarios.json') as usuario_temporaria:
        usuarios = json.load(usuario_temporaria)
        cont = 0    
        for usuario in usuarios:
            cont += 1
            if nome == 'adm' and senha == '222':
                logado = True
                return redirect('/adm')
            
            if usuario["nome"] == nome and usuario["senha"] == senha:
                return render_template('usuario.html')
            
            if cont >= len(usuarios):
                flash('USUARIO INVALIDO')
                return redirect('/')
            
@app.route('/cadastro_user', methods=['POST'])
def cadastro_user():
    user = []
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    user = [
        {
            'nome': nome,
            'senha': senha
        }
    ]

    with open('D:/PagAutentc_python/usuarios.json') as usuario_temporaria:
        usuarios = json.load(usuario_temporaria)

    novo_user = usuarios + user  

    with open('D:/PagAutentc_python/usuarios.json', 'w') as cadastro_temp:
        json.dump(novo_user, cadastro_temp, indent=4)

    return redirect('/adm')
    




if __name__ in "__main__":
    app.run(debug=True)