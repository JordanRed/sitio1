import os.path

from flask import Flask
from flask import render_template, request, redirect, session
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory

app=Flask(__name__)
app.secret_key="sublimatic"
mysql = MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='eust'
app.config['MYSQL_DATABASE_PASSWORD']='$0yIO#A381&'
app.config['MYSQL_DATABASE_DB']='sitio'
mysql.init_app(app)

@app.route('/')
def inicio():
    return render_template('sitio/index.html')

@app.route('/img/<imagen>')
def imagenes(imagen):
    print(imagen)
    return send_from_directory(os.path.join('templates/sitio/img'), imagen)

@app.route('/css/<archivocss>')
def css_link(archivocss):
    return send_from_directory(os.path.join('templates/sitio/css'), archivocss)



@app.route('/productos')
def productos():

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `productos`")
    productos=cursor.fetchall()
    conexion.commit()

    return render_template('sitio/productos.html', productos=productos)

@app.route('/nosotros')
def nosotros():
    return render_template('sitio/nosotros.html')

@app.route('/admin/')
def admin_index():
    if not 'login' in session:
        return redirect("/admin/login")
    return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    _usuario = request.form['txtUsuario']
    _password = request.form['txtPassword']
    print(_usuario, _password)

    if _usuario == "admin" and _password == "Gr$Te#v491":
        session["login"] = True
        session["usuario"] = "Administrador"
        return redirect("/admin")

    return render_template('admin/login.html', mensaje="Acceso denegado")

@app.route('/admin/cerrar')
def admin_login_cerrar():
    session.clear()
    return redirect('/admin/login')



@app.route('/admin/productos')
def admin_productos():

    if not 'login' in session:
        return redirect("/admin/login")

    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `productos`")
    productos=cursor.fetchall()
    conexion.commit()

    return render_template('admin/productos.html', productos=productos)

@app.route('/admin/productos/guardar', methods=['POST'])
def admin_productos_guardar():

    if not 'login' in session:
        return redirect("/admin/login")

    _nombre = request.form['txtNombre']
    _descripcion = request.form['txtDescripcion']
    _url = request.form['txtURL']
    _archivo = request.files['txtImagen']

    tiempo = datetime.now()
    horaActual = tiempo.strftime('%Y%H%M%S')
    if _archivo != "":
        nuevoNombre = horaActual + "_" + _archivo.filename
        _archivo.save("templates/sitio/img/" + nuevoNombre)

    sql='INSERT INTO `productos` (`id`, `nombre`, `descripcion`, `imagen`, `url`) VALUES (NULL, %s, %s, %s, %s); '
    datos = (_nombre, _descripcion, nuevoNombre, _url)
    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute(sql, datos)
    conexion.commit()

    return redirect('/admin/productos')

@app.route('/admin/productos/borrar', methods=['POST'])
def admin_productos_borrar():
    if not 'login' in session:
        return redirect("/admin/login")

    _id = request.form['txtID']

    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("SELECT imagen FROM `productos` WHERE `productos`.`id` = %s", (_id))
    producto = cursor.fetchall()
    conexion.commit()

    if os.path.exists("templates/sitio/img/" + str(producto[0][0])):
        os.unlink("templates/sitio/img/" + str(producto[0][0]))


    conexion = mysql.connect()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM `productos` WHERE `productos`.`id` = %s", (_id))
    #producto = cursor.fetchall()
    conexion.commit()

    return redirect('/admin/productos')



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)