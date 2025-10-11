
from flask import Flask, render_template, redirect, request, flash, url_for, send_from_directory
import json
import ast
import os
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cesar'

logado = False

@app.route('/')
def home():
    global logado
    logado = False
    return render_template('login.html', menssagem='')

@app.route('/adm')
def adm():
    if logado == True:
        conect_BD = mysql.connector.connect(host='localhost', database='usuarios', user='root', password='9458Cf9590&')    
        
        if conect_BD.is_connected():
            print('conectado')
            cursor = conect_BD.cursor()
            cursor.execute('select * from users;')
            usuarios = cursor.fetchall()
            print('==========')
        return render_template('admin.html', usuarios=usuarios)
    if logado == False:
        return redirect('/')
    
    
@app.route('/usuarios')
def usuarios():
    if logado == True:
        arquivo = []
        for documento in os.listdir('D:/proj_login/arquivos'):
            arquivo.append(documento)
        return render_template('usuarios.html', arquivos=arquivo)
    else:
        return redirect('/')
        

@app.route('/login', methods=['POST'])
def login():

    global logado

    nome = request.form.get('nome')
    senha = request.form.get('senha')

    conect_BD = mysql.connector.connect(host='localhost', database='usuarios', user='root', password='9458Cf9590&')
    cont = 0
    if conect_BD.is_connected():
        print('conectado')
        cursor = conect_BD.cursor()
        cursor.execute('select * from users;')

        usuariosBD = cursor.fetchall()

        for usuario in usuariosBD:
            cont += 1
            usuario_nome = str(usuario[1])
            usuario_senha = str(usuario[2])

            if nome == 'adm' and senha == '222':
                logado = True
                return redirect('/adm')
            
            if usuario_nome == nome and usuario_senha == senha:
                logado = True
                return redirect('/usuarios')
                
            
            if cont >= len(usuariosBD):
                flash('USUARIO INVALIDO')
                return redirect('/')
            
@app.route('/cadastro_user', methods=['POST'])
def cadastro_user():
    global logado
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    conect_BD = mysql.connector.connect(host='localhost', database='usuarios', user='root', password='9458Cf9590&')

    if conect_BD.is_connected():
        cursor = conect_BD.cursor()
        cursor.execute(f"insert into users values (default, '{nome}','{senha}');")
        conect_BD.commit()
    if  conect_BD.is_connected():
        cursor.close()
        conect_BD.close()

    logado = True
    flash(F'{nome} Cadastrado com Sucesso!')
    return redirect('/adm')
    

@app.route('/delet_user', methods=['POST'])
def delet_user():
    global logado
    logado = True
    nome = request.form.get('nome')
    usuarioID = request.form.get('del_user')
    conect_BD = mysql.connector.connect(host='localhost', database='usuarios', user='root', password='9458Cf9590&')

    if conect_BD.is_connected():
        cursor = conect_BD.cursor()
        cursor.execute(f"delete from users where id='usuarioID'")
        
    if  conect_BD.is_connected():
        cursor.close()
        conect_BD.close()


    flash(F'{nome}: Excluido com Sucesso!')
    return redirect('/adm')

@app.route('/upload', methods=['POST'])
def uplaod():
    global logado
    logado = True

    arquivo = request.files.get('documento')
    nome_arquiv = arquivo.filename.replace(' ','_')
    pasta_destino = 'D:/proj_login/arquivos'
    os.makedirs(pasta_destino, exist_ok=True)
    arquivo.save(os.path.join(pasta_destino, nome_arquiv))

    flash('Arquivo salvo com Sucesso!')
    return redirect('/adm')

@app.route('/download', methods=['POST'])
def download():
    nome_arqi = request.form.get('arquivosP_download')

    return send_from_directory('arquivos', nome_arqi, as_attachment=True)


if __name__ in "__main__":
    app.run(debug=True)