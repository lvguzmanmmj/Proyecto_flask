from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
app = Flask(__name__, static_folder='css')

# mysql connection
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'usuarios'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/clientes', methods=['GET', 'POST'])
def add_clientes():
    # Consulta para generar los datos
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes')
    data = cur.fetchall()
    cur.close()
    if request.method == 'POST':
        id = request.form['id']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO clientes (id, nombre, apellido, email, telefono, direccion) VALUES (%s, %s, %s, %s, %s, %s)', 
                    (id, nombre, apellido, email, telefono, direccion))
        mysql.connection.commit()
        cur.close()
        flash('Client added successfully')
        return redirect(url_for('add_clientes'))
    return render_template('clientes.html', clientes=data)

@app.route('/delete/<string:id>')
def delete_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM clientes WHERE id = %s', [id])
    mysql.connection.commit()
    cur.close()
    flash('Client Removed Successfully')
    return redirect(url_for('add_clientes'))

@app.route('/edit/<id>')
def get_clientes(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM clientes WHERE id = %s', [id])
    data = cur.fetchall()
    return render_template('edit-table.html' , cliente = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_clientes(id):
    if request.method == 'POST':
        id = request.form['id']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        email = request.form['email']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        cur = mysql.connection.cursor()
        cur.execute(""" 
            UPDATE clientes
            SET id = %s,
                nombre = %s,
                apellido = %s,
                email = %s,
                telefono = %s,
                direccion = %s
            WHERE id = %s
        """, (id, nombre, apellido, email, telefono, direccion, id))
        mysql.connection.commit()
        flash('contact update successfully')
        return redirect(url_for('add_clientes'))


    #tabla compra

@app.route('/compra', methods=['GET', 'POST'])
def add_compra():
    # Consulta para obtener los datos de compras
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM compra')
    data = cur.fetchall()
    cur.close()
    if request.method == 'POST':
        id = request.form['id']
        cliente_id = request.form['cliente_id']
        producto_id = request.form['producto_id']
        cantidad = request.form['cantidad']
        precio_unitario = request.form['precio_unitario']
        fecha = request.form['fecha']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO compra (id, cliente_id, producto_id, cantidad, precio_unitario, fecha) VALUES (%s, %s, %s, %s, %s, %s)', 
                    (id, cliente_id, producto_id, cantidad, precio_unitario, fecha))
        mysql.connection.commit()
        cur.close()
        flash('Compra añadida correctamente')
        return redirect(url_for('add_compra'))
    return render_template('compra.html', compras=data)

@app.route('/delete_compra/<string:id>')
def delete_compra(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM compra WHERE id = %s', [id])
    mysql.connection.commit()
    cur.close()
    flash('Compra eliminada exitosamente')
    return redirect(url_for('add_compra'))

@app.route('/edit_compra/<id>')
def get_compra(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM compra WHERE id = %s', [id])
    data = cur.fetchall()
    if len(data) == 0:
        flash('Compra not found')
        return redirect(url_for('add_compra'))
    return render_template('edit-compra.html', compra=data[0])

@app.route('/update_compra/<id>', methods=['POST'])
def update_compra(id):
    if request.method == 'POST':
        id = request.form['id']
        cliente_id = request.form['cliente_id']
        producto_id = request.form['producto_id']
        cantidad = request.form['cantidad']
        precio_unitario = request.form['precio_unitario']
        fecha = request.form['fecha']
        cur = mysql.connection.cursor()
        cur.execute(""" 
            UPDATE compra
            SET id = %s,
                cliente_id = %s,
                producto_id = %s,
                cantidad = %s,
                precio_unitario = %s,
                fecha = %s
            WHERE id = %s
        """, (id, cliente_id, producto_id, cantidad, precio_unitario, fecha, id))
        mysql.connection.commit()
        flash('Compra actualizada exitosamente')
        return redirect(url_for('add_compra'))

#TABLA PRODUCTOS

@app.route('/productos', methods=['GET', 'POST'])
def add_producto():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos')
    data = cur.fetchall()
    cur.close()
    if request.method == 'POST':
        id = request.form['id']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO productos (id, nombre, descripcion, precio, stock) VALUES (%s, %s, %s, %s, %s)', 
                    (id, nombre, descripcion, precio, stock))
        mysql.connection.commit()
        cur.close()
        flash('Producto añadido correctamente')
        return redirect(url_for('add_producto'))
    return render_template('productos.html', productos=data)

@app.route('/delete_producto/<string:id>')
def delete_producto(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM productos WHERE id = %s', [id])
    mysql.connection.commit()
    cur.close()
    flash('Producto eliminado exitosamente')
    return redirect(url_for('add_producto'))

@app.route('/edit_producto/<id>')
def get_producto(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE id = %s', [id])
    data = cur.fetchall()
    if len(data) == 0:
        flash('Producto no encontrado')
        return redirect(url_for('add_producto'))
    return render_template('edit-productos.html', producto=data[0])

@app.route('/update_producto/<id>', methods=['POST'])
def update_producto(id):
    if request.method == 'POST':
        id = request.form['id']
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']
        cur = mysql.connection.cursor()
        cur.execute(""" 
            UPDATE productos
            SET id = %s,
                nombre = %s,
                descripcion = %s,
                precio = %s,
                stock = %s
            WHERE id = %s
        """, (id, nombre, descripcion, precio, stock, id))
        mysql.connection.commit()
        flash('Producto actualizado exitosamente')
        return redirect(url_for('add_producto'))


if __name__ == '__main__':
    app.run(debug=True)
