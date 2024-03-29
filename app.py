from flask import Flask
from flask import render_template,request, redirect,url_for,session, flash
from flaskext.mysql import MySQL
from flask import send_from_directory
from datetime import datetime
import os

app=Flask(__name__)
# Base de datos con sql express/desarrollador
app=Flask(__name__)
app.secret_key="tienda"
mysql=MySQL()
app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='tienda'
mysql.init_app(app)
# ruta de inicio
@app.route("/")
def usuario():
    return redirect('/inicio')

@app.route("/inicio")
def usuario2():
    return render_template('sitio/index.html')
# Ruta para cerrar seccion
@app.route("/cerrar")
def cerrar():
    session.clear()
    return redirect('/')


# Ruta para iniciar sesion como admin
@app.route("/admin")
def admin():
    if not 'login' in session:
        return redirect('/')
    return render_template('admin/admin.html')

@app.route("/agregar")
def agre():
    if not 'login' in session:
        return redirect('/')
    sql="SELECT * FROM `productos`;"
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql)
    productos=cursor.fetchall()
    conn.commit()
    return render_template('admin/masprodad.html',productos=productos)

@app.route('/edid/<int:id>')
def edid(id):
    if not 'login' in session:
        return redirect('/')
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM productos WHERE Codigo=%s",(id))
    productos=cursor.fetchall()
    conn.commit()
    return render_template('invet/edid.html',productos=productos)

@app.route("/act", methods=['POST'])
def act():
    if not 'login' in session:
        return redirect('/')
    id=request.form['Codigo']
    _nom=request.form['Nombre']
    _prev=request.form['preciodecompra']
    _prec=request.form['preciodeventa']
    _exi=request.form['existencia']
    _rest=request.form['restriccion']
    sql="UPDATE productos SET `Nombre`=%s, `preciodecompra`=%s, `preciodeventa`=%s, `existencia`=%s, `restriccion`=%s WHERE codigo=%s ;"
    datos=(_nom,_prev,_prec	,_exi,_rest,id)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/agregar')

@app.route("/act2", methods=['POST'])
def act2():
    if not 'login' in session:
        return redirect('/')
    id=request.form['Codigo']
    _nom=request.form['Nombre']
    _prev=request.form['preciodecompra']
    _prec=request.form['preciodeventa']
    _exi=request.form['existencia']
    _rest=request.form['restriccion']
    sql="UPDATE productos SET `Nombre`=%s, `preciodecompra`=%s, `preciodeventa`=%s, `existencia`=%s, `restriccion`=%s WHERE codigo=%s ;"
    datos=(_nom,_prev,_prec	,_exi,_rest,id)
    conn=mysql.connect()
    cursor=conn.cursor()
    cursor.execute(sql,datos)
    conn.commit()
    return redirect('/productoad')

# Ruta de inicio de seccion correcto como admin
@app.route("/Loginadmin")
def Loginadmin():
    if 'login' in session:
        return redirect('/admin')
    return render_template('admin/loginadmin.html')

@app.route("/Loginadmin", methods=['POST'])
def ad_log():
    _corr=request.form['txtcorreo']
    _con=request.form['txtcontra']

    if _corr=='' or _con=="":
        flash('Recuerda llenar los datos de los campos')
        return render_template('admin/loginadmin.html')

    sql="SELECT * FROM `administrador` WHERE usuario=%s;"
    conn=mysql.connect()
    cursor=conn.cursor()
    dato=(_corr)
    cursor.execute(sql,dato)
    _corrv=cursor.fetchall()
    conn.commit()
    print(_corrv)
    if _corrv is ():
        return render_template('admin/loginadmin.html')

    if _corr==_corrv[0][3] and _con==_corrv[0][4]:
        session["login"]=True
        session["usuario"]=_corrv[0][1]
        session["rango"]="admin"
        return redirect('/admin')
    return render_template('admin/loginadmin.html')


@app.route("/Productos")

def productos1():
    return render_template('sitio/Productos.html')

# Cargar imagenes    
CARPETA= os.path.join('uploads')
app.config['CARPETA']=CARPETA

@app.route('/uploads/<nombreFoto>')
def uploads(nombreFoto):
    return send_from_directory(app.config['CARPETA'],nombreFoto)

CARPETA1= os.path.join('reTIEN')
app.config['CARPETA1']=CARPETA1

@app.route('/reTIEN/<nombreFoto1>')
def reTIEN(nombreFoto1):
    return send_from_directory(app.config['CARPETA1'],nombreFoto1)

# Fin de cargar imagenes
if __name__ == '__main__':
    app.run(debug=True)



