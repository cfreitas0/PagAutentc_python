
from flask import Flask, render_template, redirect, request, flash, url_for
import json
import ast

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
    global logado
    user = []
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    user = [
        {
            'nome': nome,
            'senha': senha
        }
    ]

    with open('D:/proj_login/usuarios.json') as usuario_temporaria:
        usuarios = json.load(usuario_temporaria)

    novo_user = usuarios + user  

    with open('D:/proj_login/usuarios.json', 'w') as cadastro_temp:
        json.dump(novo_user, cadastro_temp, indent=4)
    logado = True
    flash(F'{nome} Cadastrado com Sucesso!')
    return redirect('/adm')
    

@app.route('/delet_user', methods=['POST'])
def delet_user():
    global logado
    logado = True
    usuario = request.form.get('del_user')
    user_dict = ast.literal_eval(usuario)
    nome = user_dict['nome']
    with open('D:/proj_login/usuarios.json') as usuario_temporaria:
        user_json = json.load(usuario_temporaria)
        for c in user_json:
            if c == user_dict:
                user_json.remove(user_dict)
                with open('D:/proj_login/usuarios.json', 'w') as del_user:
                    json.dump(user_json, del_user, indent=4)

    flash(F'{nome}Excluido com Sucesso!')
    return redirect('/adm')


if __name__ in "__main__":
    app.run(debug=True)