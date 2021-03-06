from flask import Flask, request, session, render_template
import json, csv, os, datetime

#iniciando app para la redirección de html.
app = Flask(__name__)

app.secret_key = 'esto-es-una-clave-muy-secreta' #encriptar session.

@app.errorhandler(404)
def page_not_found(e):
#hola
    if 'loginC' in session:
    	if session['loginC']:
    		return render_template('inicio.html')
    	else:
    		return render_template('index.html')
    else:
    	return render_template('index.html')

@app.errorhandler(405)
def method_not_allowed(e):

    if 'loginC' in session:
    	if session['loginC']:
    		return render_template('inventario.html')
    	else:
    		return render_template('index.html')
    else:
    	return render_template('index.html')

#Redirección a /index.html.
@app.route('/index.html')
def index():
	#Comprobamos si existe la session 'loginC'.
	#Si existe comprobamos si es True o False, si es True cargamos la página.
	#Si no exite la creamos en False y hacemos una redirección a index.html.
	if 'loginC' in session:
		if session['loginC']:
			return render_template('inicio.html')
		else:
			return render_template('index.html')
	else:
		return render_template('index.html')

#Redirección a /inicio.html.
@app.route('/inicio.html')
def inicio():
	#Comprobamos si 'loginC' es True
	if session['loginC']:
		return render_template('inicio.html')

	else:
		return render_template('index.html')

@app.route('/login', methods=['POST'])
def signUpUser():
    #Abrimos el archivo listaUsuarios.csv y comprobamos si esta el usuario

    session['loginC'] = False

    with open(os.getcwd()+'/Python3_SGE/datos/listaUsuarios.csv', 'r', encoding="ISO-8859-15") as File:

    	reader = csv.reader(File, delimiter=';', quotechar=';',
                        quoting=csv.QUOTE_MINIMAL)

    	for row in reader:
    		if row[1] == request.form['username'] and row[2] == request.form['password']:
    			session['idUser'] = row[0]
    			session['loginC'] = True

    if session['loginC']:
    	return json.dumps(1);

    else:
    	return json.dumps(0);

@app.route('/logout', methods=['POST'])
def logoutUser():

    if session['loginC']:

    	session['loginC'] = False
    	return json.dumps(1);

    else:
    	return json.dumps(0);

#Redireccion a /inventario.html
@app.route('/inventario.html')
def inventario():
	if 'loginC' in session:

		if session['loginC']:

			valido = False

			with open(os.getcwd()+'/Python3_SGE/datos/listaDepartamentos.csv', 'r', encoding="ISO-8859-15") as File:

				reader = csv.reader(File, delimiter=';', quotechar=';',
                        quoting=csv.QUOTE_MINIMAL)

				for row in reader: #Comprobamos si el usuario logueado tiene permisos para usar este modulo
					if row[0] == "1":
						for i in row[2]:
							if i == session['idUser']:
								valido = True

			if valido:
				return render_template('inventario.html')

			else:
				return render_template('inicio.html')

		else:
			return render_template('index.html')

	else:
		return render_template('index.html')

#Cargar la lista de los productos
@app.route('/cargarInventario', methods=['POST'])
def cargarInventario():

	datos = []

	with open(os.getcwd()+'/Python3_SGE/datos/listaInventario.csv', 'r', encoding="ISO-8859-15") as File:

		readercp = csv.reader(File, delimiter=';', quotechar=';',
                        quoting=csv.QUOTE_MINIMAL)
		datos = list(readercp)

	del datos[0] #Eliminar la primera linea de datos, para que no devulva los titulos.

	return json.dumps({'datos':datos})

#Borrar un producto seleccionado
@app.route('/borrarInventario', methods=['POST'])
def borrarInventario():

	idInventario = request.form['idInventario']

	with open(os.getcwd()+'/Python3_SGE/datos/listaInventario.csv', 'r', encoding="ISO-8859-15") as inp, open(os.getcwd()+'/Python3_SGE/datos/new.csv', 'w', encoding="ISO-8859-15") as out:

		writer = csv.DictWriter(out, dialect='unix', delimiter=";", quotechar=";",
    		fieldnames =("ID", "NOMBRE", "TIPO", "CANTIDAD", "PRECIO_COMPRA", "PRECIO_VENTA", "CONTROLES") , quoting=csv.QUOTE_MINIMAL)

		writer.writeheader() #Evitamos borrar los titulos (fieldnames)

		for rowbp in csv.DictReader(inp, dialect='unix', delimiter=";"):
			if rowbp["ID"] != idInventario: #Creamos el nuevo archivo con todos los datos menos la fila con el id devuelto
				writer.writerow(rowbp)

	os.remove(os.getcwd()+'/Python3_SGE/datos/listaInventario.csv') #Removemos el anterior archivo
	os.rename(os.getcwd()+'/Python3_SGE/datos/new.csv', os.getcwd()+'/Python3_SGE/datos/listaInventario.csv') #Cambiamos el nombre del nuevo archivo al nombre del anterior

	return json.dumps(1);

#Crear un producto
@app.route('/crearProducto', methods=['POST'])
def crearProducto():

	result = []

	with open(os.getcwd()+'/Python3_SGE/datos/listaInventario.csv', 'r', encoding="ISO-8859-15") as inp, open(os.getcwd()+'/Python3_SGE/datos/new.csv', 'w', encoding="ISO-8859-15") as out:

			writer = csv.DictWriter(out, dialect='unix', delimiter=";", quotechar=";",
	    		fieldnames =("ID", "NOMBRE", "TIPO", "CANTIDAD", "PRECIO_COMPRA", "PRECIO_VENTA", "CONTROLES"), quoting=csv.QUOTE_MINIMAL)

			writer.writeheader()

			readercp = csv.DictReader(inp, dialect='unix', delimiter=";") #Leer archivo viejo

			for rowcp in readercp:
				result.append(rowcp) #Guardamos los datos del archivo viejo en una lista

			ID = 0
			try:
				ID = int((int(rowcp['ID'][-1]) + 1)) #Recogemos el id del ultimo elemento del archivo y le sumamos 1
			except NameError:
				ID = 1 #Si no hay ningun elemento en el archivo ponemos el id a 1

			nombre = request.form['nombreP']
			tipo = request.form['tipoP']
			cantidad = request.form['contidadP']
			precioCompra = str(request.form['precioCompraP']) + "$"
			precioVenta = str(request.form['precioVentaP']) + "$"
			controles = '<button onclick="modificar({})" class="btn btn btn-outline-warning" type="button">Modificar</button><button onclick="borrar({})" class="btn btn btn-outline-danger mt-2" type="button">Borrar</button>'.format(ID, ID)

			data = {'ID': ID, 'NOMBRE': nombre, "TIPO": tipo, "CANTIDAD": cantidad, "PRECIO_COMPRA": precioCompra, "PRECIO_VENTA": precioVenta, "CONTROLES": controles}

			result.append(data) #Añadimos el nuevo elemento a la lista
			writer.writerows(result) #Añadimos los datos de la lista en el nuevo archivo

	os.remove(os.getcwd()+'/Python3_SGE/datos/listaInventario.csv')
	os.rename(os.getcwd()+'/Python3_SGE/datos/new.csv', os.getcwd()+'/Python3_SGE/datos/listaInventario.csv')

	return json.dumps(1);

#Cargar datos de un produto seleccionado
@app.route('/verProducto', methods=['POST'])
def verProducto():

	idInventario = request.form['idInventario']

	datosP = []

	with open(os.getcwd()+'/Python3_SGE/datos/listaInventario.csv', 'r', encoding="ISO-8859-15") as inp:

		for rowvp in csv.DictReader(inp, dialect='unix', delimiter=";"):

			if rowvp["ID"] == idInventario: #Añadimos los datos del elemento seleccionado(id) a la lista
				datosP.append(rowvp['ID'])
				datosP.append(rowvp['NOMBRE'])
				datosP.append(rowvp['TIPO'])
				datosP.append(rowvp['CANTIDAD'])
				datosP.append(rowvp['PRECIO_COMPRA'][:-1])
				datosP.append(rowvp['PRECIO_VENTA'][:-1])

	return json.dumps({'datos':datosP}) #Devolvemos los datos en forma json

#Modificar datos de un producto seleccionado
@app.route('/actualizarProducto', methods=['POST'])
def actualizarProducto():

	precioCompra = request.form['precioCompraAP']
	precioVenta = request.form['precioVentaAP']

	with open(os.getcwd()+'/Python3_SGE/datos/listaInventario.csv', 'r', encoding="ISO-8859-15") as inp, open(os.getcwd()+'/Python3_SGE/datos/new.csv', 'w', encoding="ISO-8859-15") as out:

		writer = csv.DictWriter(out, dialect='unix', delimiter=";", quotechar=";",
    		fieldnames =("ID", "NOMBRE", "TIPO", "CANTIDAD", "PRECIO_COMPRA", "PRECIO_VENTA", "CONTROLES") , quoting=csv.QUOTE_MINIMAL)

		writer.writeheader()

		for rowacp in csv.DictReader(inp, dialect='unix', delimiter=";"):

			if rowacp["ID"] == request.form['idAP']: #Cambiamos los datos del elemto seleccionado(id) a los nuevos datos
				rowacp['NOMBRE'] = request.form['nombreAP']
				rowacp['TIPO'] = request.form['tipoAP']
				rowacp['CANTIDAD'] = request.form['contidadAP']
				rowacp['PRECIO_COMPRA'] = str(precioCompra) + "$"
				rowacp['PRECIO_VENTA'] = str(precioVenta) + "$"

			rowacp = {'ID': rowacp['ID'], 'NOMBRE': rowacp['NOMBRE'], 'TIPO': rowacp['TIPO'], 'CANTIDAD': rowacp['CANTIDAD'], 'PRECIO_COMPRA': rowacp['PRECIO_COMPRA'], 'PRECIO_VENTA': rowacp['PRECIO_VENTA'], 'CONTROLES': rowacp['CONTROLES']}
			#Añadimos esos datos al rowacp
			writer.writerow(rowacp) #Añadimos los datos el archivo

	os.remove(os.getcwd()+'/Python3_SGE/datos/listaInventario.csv')
	os.rename(os.getcwd()+'/Python3_SGE/datos/new.csv', os.getcwd()+'/Python3_SGE/datos/listaInventario.csv')

	return json.dumps(1);

@app.route('/compras.html')
def compras():
	if 'loginC' in session:

		if session['loginC']:

			valido = False

			with open(os.getcwd()+'/Python3_SGE/datos/listaDepartamentos.csv', 'r', encoding="ISO-8859-15") as File:

				reader = csv.reader(File, delimiter=';', quotechar=';',
                        quoting=csv.QUOTE_MINIMAL)

				for row in reader: #Comprobamos si el usuario logueado tiene permisos para usar este modulo
					if row[0] == "2":
						for i in row[2]:
							if i == session['idUser']:
								valido = True

			if valido:
				return render_template('compras.html')

			else:
				return render_template('inicio.html')

		else:
			return render_template('index.html')

	else:
		return render_template('index.html')

#Cargar la lista de los productos
@app.route('/cargarCompras', methods=['POST'])
def cargarCompras():

	listaDatos = []

	with open(os.getcwd()+'/Python3_SGE/datos/listaCompras.csv', 'r', encoding="ISO-8859-15") as lc:

		readerlc = csv.reader(lc, delimiter=';', quotechar=';',
	                       quoting=csv.QUOTE_MINIMAL)

		next(readerlc)

		index = 0 #Cantidad de elementos que tiene el archivo listaCompra.csv
		borrarP = 2 #Posicion en la que borrar el id del proveedor
		borrarI = 1 #Posicion en la que borrar el id del invenario

		for rowlc in readerlc:

			datos = []

			for i in rowlc:

				datos.append(i)
				index += 1

				if index == 7:

					index = 0

				if index == 2:
					with open(os.getcwd()+'/Python3_SGE/datos/listaInventario.csv', 'r', encoding="ISO-8859-15") as lp:
						readerlp = csv.reader(lp, delimiter=';', quotechar=';',	quoting=csv.QUOTE_MINIMAL)

						next(readerlp)

						for rowlp in readerlp:

							if i == rowlp[0]:

								del datos[borrarI]
								datos.append(rowlp[1])

				if index == 3:

					with open(os.getcwd()+'/Python3_SGE/datos/listaProveedors.csv', 'r', encoding="ISO-8859-15") as lp:

						readerlp = csv.reader(lp, delimiter=';', quotechar=';',	quoting=csv.QUOTE_MINIMAL)

						next(readerlp)

						for rowlp in readerlp:

							if i == rowlp[0]:

								del datos[borrarP]
								datos.append(rowlp[1])

			listaDatos.append(datos)

	return json.dumps({'datos':listaDatos})

@app.route('/selectInventario', methods=['POST'])
def selectInventario():

	listaDatos = []

	with open(os.getcwd()+'/Python3_SGE/datos/listaInventario.csv', 'r', encoding="ISO-8859-15") as lc:

		readerlc = csv.reader(lc, delimiter=';', quotechar=';',
	                      quoting=csv.QUOTE_MINIMAL)

		next(readerlc)

		for rowlc in readerlc:
			datos = []
			datos.append(rowlc[0])
			datos.append(rowlc[1])
			datos.append(rowlc[4])
			listaDatos.append(datos)

	return json.dumps({'datos':listaDatos})

@app.route('/selectProveedor', methods=['POST'])
def selectProveedor():

	listaDatos = []

	with open(os.getcwd()+'/Python3_SGE/datos/listaProveedors.csv', 'r', encoding="ISO-8859-15") as lc:

		readerlc = csv.reader(lc, delimiter=';', quotechar=';',
	                      quoting=csv.QUOTE_MINIMAL)

		next(readerlc)

		for rowlc in readerlc:
			datos = []
			datos.append(rowlc[0])
			datos.append(rowlc[1])
			listaDatos.append(datos)

	return json.dumps({'datos':listaDatos})

@app.route('/crearCompra', methods=['POST'])
def crearCompra():

	result = []

	with open(os.getcwd()+'/Python3_SGE/datos/listaCompras.csv', 'r', encoding="ISO-8859-15") as inp, open(os.getcwd()+'/Python3_SGE/datos/new.csv', 'w', encoding="ISO-8859-15") as out:
	
			writer = csv.DictWriter(out, delimiter=";", quotechar=";",
	    		fieldnames =("ID", "PRODUCTO", "PROVEEDOR", "CANTIDAD", "PRECIO", "TOTAL", "CONTROLES"), quoting=csv.QUOTE_MINIMAL)
			
			writer.writeheader()
	
			readercp = csv.DictReader(inp, delimiter=";") #Leer archivo viejo
	
			for rowcp in readercp:
				result.append(rowcp) #Guardamos los datos del archivo viejo en una lista
	
			ID = 0
			try:
				ID = int((int(rowcp['ID'][-1]) + 1)) #Recogemos el id del ultimo elemento del archivo y le sumamos 1
			except NameError:
				ID = 1 #Si no hay ningun elemento en el archivo ponemos el id a 1
	
			producto = request.form['sProductos']
			proveedor = request.form['sProveedor']
			cantidad = str(request.form['cantidadCP'])
			precio = str(request.form['precioCP']) + "$"
			total = str(request.form['totalCP']) + "$"
			controles = '<button onclick="comprar({})" class="btn btn btn-outline-warning" type="button">Comprar</button><button onclick="borrar({})" class="btn btn btn-outline-danger mt-2" type="button">Borrar</button>'.format(ID, ID)
			
			data = {'ID': ID, 'PRODUCTO': producto, "PROVEEDOR": proveedor, "CANTIDAD": cantidad, "PRECIO": precio, "TOTAL": total, "CONTROLES": controles}
			
			result.append(data) #Añadimos el nuevo elemento a la lista
			writer.writerows(result) #Añadimos los datos de la lista en el nuevo archivo
	
	os.remove(os.getcwd()+'/Python3_SGE/datos/listaCompras.csv')
	os.rename(os.getcwd()+'/Python3_SGE/datos/new.csv', os.getcwd()+'/Python3_SGE/datos/listaCompras.csv')

	return json.dumps(1);

@app.route('/borrarCompra', methods=['POST'])
def borrarCompra():

	idCompra = request.form['idCompra']

	with open(os.getcwd()+'/Python3_SGE/datos/listaCompras.csv', 'r', encoding="ISO-8859-15") as inp, open(os.getcwd()+'/Python3_SGE/datos/new.csv', 'w', encoding="ISO-8859-15") as out:

		writer = csv.DictWriter(out, dialect='unix', delimiter=";", quotechar=";",
    		fieldnames =("ID", "PRODUCTO", "PROVEEDOR", "CANTIDAD", "PRECIO", "TOTAL", "CONTROLES") , quoting=csv.QUOTE_MINIMAL)

		writer.writeheader() #Evitamos borrar los titulos (fieldnames)

		for rowbp in csv.DictReader(inp, dialect='unix', delimiter=";"):
			if rowbp["ID"] != idCompra: #Creamos el nuevo archivo con todos los datos menos la fila con el id devuelto
				writer.writerow(rowbp)

	os.remove(os.getcwd()+'/Python3_SGE/datos/listaCompras.csv') #Removemos el anterior archivo
	os.rename(os.getcwd()+'/Python3_SGE/datos/new.csv', os.getcwd()+'/Python3_SGE/datos/listaCompras.csv') #Cambiamos el nombre del nuevo archivo al nombre del anterior

	return json.dumps(1);

@app.route('/comprarCompra', methods=['POST'])
def comprarCompra():

	ridCompra = request.form['idCompra']

	rproducto = ""
	rproveedor = ""
	rcantidad = ""
	rprecio = ""
	rtotal = ""

	rproductoNombre = ""

	now = datetime.datetime.now()

	with open(os.getcwd()+'/Python3_SGE/datos/listaCompras.csv', 'r', encoding="ISO-8859-15") as inp:

		for rowvp in csv.DictReader(inp, delimiter=";"):
	
			if rowvp["ID"] == ridCompra:
				rproducto = rowvp['PRODUCTO']
				rproveedor = rowvp['PROVEEDOR']
				rcantidad = rowvp['CANTIDAD']
				rprecio = rowvp['PRECIO']
				rtotal = rowvp['TOTAL']

	with open(os.getcwd()+'/Python3_SGE/datos/listaInventario.csv', 'r', encoding="ISO-8859-15") as inp:

		for rowvp in csv.DictReader(inp, delimiter=";"):
	
			if rowvp["ID"] == rproducto:
				rproductoNombre = rowvp['NOMBRE']

	result = []

	with open(os.getcwd()+'/Python3_SGE/datos/listaHistoricoCompras.csv', 'r', encoding="ISO-8859-15") as inp, open(os.getcwd()+'/Python3_SGE/datos/new.csv', 'w', encoding="ISO-8859-15") as out:
	
			writer = csv.DictWriter(out, delimiter=";", quotechar=";",
	    		fieldnames =("ID", "PRODUCTO", "PROVEEDOR", "CANTIDAD", "PRECIO", "TOTAL", "DATE", "NOMBREP"), quoting=csv.QUOTE_MINIMAL)
			
			writer.writeheader()
	
			readercp = csv.DictReader(inp, delimiter=";") #Leer archivo viejo
	
			for rowcp in readercp:
				result.append(rowcp) #Guardamos los datos del archivo viejo en una lista
	
			ID = 0
			try:
				ID = int((int(rowcp['ID'][-1]) + 1)) #Recogemos el id del ultimo elemento del archivo y le sumamos 1
			except NameError:
				ID = 1 #Si no hay ningun elemento en el archivo ponemos el id a 1
	
			producto = rproducto
			proveedor = rproveedor
			cantidad = rcantidad
			precio = rprecio
			total = rtotal
			date = (str(now.day) + "/" + str(now.month) + "/" + str(now.year))
			nombrep = rproductoNombre.capitalize()
			
			data = {'ID': ID, 'PRODUCTO': producto, "PROVEEDOR": proveedor, "CANTIDAD": cantidad, "PRECIO": precio, "TOTAL": total, "DATE": date, "NOMBREP": nombrep}
			
			result.append(data) #Añadimos el nuevo elemento a la lista
			writer.writerows(result) #Añadimos los datos de la lista en el nuevo archivo
	
	os.remove(os.getcwd()+'/Python3_SGE/datos/listaHistoricoCompras.csv')
	os.rename(os.getcwd()+'/Python3_SGE/datos/new.csv', os.getcwd()+'/Python3_SGE/datos/listaHistoricoCompras.csv')
	
	with open(os.getcwd()+'/Python3_SGE/datos/listaInventario.csv', 'r', encoding="ISO-8859-15") as inp, open(os.getcwd()+'/Python3_SGE/datos/new.csv', 'w', encoding="ISO-8859-15") as out:
	
			writer = csv.DictWriter(out, delimiter=";", quotechar=";",
	    		fieldnames =("ID", "NOMBRE", "TIPO", "CANTIDAD", "PRECIO_COMPRA", "PRECIO_VENTA", "CONTROLES") , quoting=csv.QUOTE_MINIMAL)
	
			writer.writeheader()
	
			for rowacp in csv.DictReader(inp, delimiter=";"):
	
				if rowacp["ID"] == rproducto: #Cambiamos los datos del elemto seleccionado(id) a los nuevos datos
					rowacp['CANTIDAD'] = int(rowacp['CANTIDAD']) + int(rcantidad)
	
				rowacp = {'ID': rowacp['ID'], 'NOMBRE': rowacp['NOMBRE'], 'TIPO': rowacp['TIPO'], 'CANTIDAD': rowacp['CANTIDAD'], 'PRECIO_COMPRA': rowacp['PRECIO_COMPRA'], 'PRECIO_VENTA': rowacp['PRECIO_VENTA'], 'CONTROLES': rowacp['CONTROLES']}
				#Añadimos esos datos al rowacp
				writer.writerow(rowacp) #Añadimos los datos el archivo
	
	os.remove(os.getcwd()+'/Python3_SGE/datos/listaInventario.csv')
	os.rename(os.getcwd()+'/Python3_SGE/datos/new.csv', os.getcwd()+'/Python3_SGE/datos/listaInventario.csv')

	
	with open(os.getcwd()+'/Python3_SGE/datos/listaCompras.csv', 'r', encoding="ISO-8859-15") as inp, open(os.getcwd()+'/Python3_SGE/datos/new.csv', 'w', encoding="ISO-8859-15") as out:
		
		writer = csv.DictWriter(out, delimiter=";", quotechar=";",
	   		fieldnames =("ID", "PRODUCTO", "PROVEEDOR", "CANTIDAD", "PRECIO", "TOTAL", "CONTROLES") , quoting=csv.QUOTE_MINIMAL)
	
		writer.writeheader() #Evitamos borrar los titulos (fieldnames)
	
		for rowbp in csv.DictReader(inp, delimiter=";"):
			if rowbp["ID"] != ridCompra: #Creamos el nuevo archivo con todos los datos menos la fila con el id devuelto
				writer.writerow(rowbp)
	
	os.remove(os.getcwd()+'/Python3_SGE/datos/listaCompras.csv') #Removemos el anterior archivo
	os.rename(os.getcwd()+'/Python3_SGE/datos/new.csv', os.getcwd()+'/Python3_SGE/datos/listaCompras.csv')

	return json.dumps(1);

@app.route('/historicoCompras.html')
def historicoCompras():
	if 'loginC' in session:

		if session['loginC']:

			valido = False

			with open(os.getcwd()+'/Python3_SGE/datos/listaDepartamentos.csv', 'r', encoding="ISO-8859-15") as File:

				reader = csv.reader(File, delimiter=';', quotechar=';',
                        quoting=csv.QUOTE_MINIMAL)

				for row in reader: #Comprobamos si el usuario logueado tiene permisos para usar este modulo
					if row[0] == "1":
						for i in row[2]:
							if i == session['idUser']:
								valido = True

			if valido:
				return render_template('historicoCompras.html')

			else:
				return render_template('inicio.html')

		else:
			return render_template('index.html')

	else:
		return render_template('index.html')

@app.route('/cargarHistorialCompras', methods=['POST'])
def cargarHistorialCompras():

	idProducto = 1

	listaDatos = []
	
	cantidad = 0
	
	index = 0
	
	with open(os.getcwd()+'/Python3_SGE/datos/listaHistoricoCompras.csv', 'r', encoding="ISO-8859-15") as lc:
	
		readerlc = csv.reader(lc, delimiter=';', quotechar=';', quoting=csv.QUOTE_MINIMAL)
	
		next(readerlc)
	
		for rowlc in readerlc:
	
			datos = []
	
			if len(listaDatos) == 0:
	
				datos.append(rowlc[1])
				datos.append(rowlc[3])
				datos.append(rowlc[4])
				datos.append(rowlc[5])
				datos.append(rowlc[6][3:-5])
				datos.append(rowlc[7])
	
				listaDatos.append(datos)
	
			else:
	
				if listaDatos[index][0] == rowlc[1] and listaDatos[index][4] == rowlc[6][3:-5]:
	
					listaDatos[index][1] = str(int(listaDatos[index][1]) + int(rowlc[3]))
	
				else:
	
					datos.append(rowlc[1])
					datos.append(rowlc[3])
					datos.append(rowlc[4])
					datos.append(rowlc[5])
					datos.append(rowlc[6][3:-5])
					datos.append(rowlc[7])
	
					listaDatos.append(datos)
	
					index += 1

	return json.dumps({'datos':listaDatos})

@app.route('/proveedor.html')
def proveedor():
	if 'loginC' in session:

		if session['loginC']:

			valido = False

			with open(os.getcwd()+'/Python3_SGE/datos/listaDepartamentos.csv', 'r', encoding="ISO-8859-15") as File:

				reader = csv.reader(File, delimiter=';', quotechar=';',
                        quoting=csv.QUOTE_MINIMAL)

				for row in reader: #Comprobamos si el usuario logueado tiene permisos para usar este modulo
					if row[0] == "2":
						for i in row[2]:
							if i == session['idUser']:
								valido = True

			if valido:
				return render_template('proveedor.html')

			else:
				return render_template('inicio.html')

		else:
			return render_template('index.html')

	else:
		return render_template('index.html')

@app.route('/cargarProveedores', methods=['POST'])
def cargarProveedores():

	listaDatos = []

	with open(os.getcwd()+'/Python3_SGE/datos/listaProveedors.csv', 'r', encoding="ISO-8859-15") as lc:

		readerlc = csv.reader(lc, delimiter=';', quotechar=';',
	                       quoting=csv.QUOTE_MINIMAL)

		next(readerlc)

		index = 0 #Cantidad de elementos que tiene el archivo listaCompra.csv
		borrarP = 2 #Posicion en la que borrar el id del proveedor
		borrarI = 1 #Posicion en la que borrar el id del invenario

		for rowlc in readerlc:

			datos = []

			for i in rowlc:

				datos.append(i)

			listaDatos.append(datos)

	return json.dumps({'datos':listaDatos})

@app.route('/newProveedor', methods=['POST'])
def crearProveedor():

	result = []

	with open(os.getcwd()+'/Python3_SGE/datos/listaProveedors.csv', 'r', encoding="ISO-8859-15") as inp, open(os.getcwd()+'/Python3_SGE/datos/new.csv', 'w', encoding="ISO-8859-15") as out:

			writer = csv.DictWriter(out, dialect='unix', delimiter=";", quotechar=";",
	    		fieldnames =("ID", "NOMBRE", "DIRECCION", "TELEFONO", "CONTROLES"), quoting=csv.QUOTE_MINIMAL)

			writer.writeheader()

			readercp = csv.DictReader(inp, dialect='unix', delimiter=";") #Leer archivo viejo

			for rowcp in readercp:
				result.append(rowcp) #Guardamos los datos del archivo viejo en una lista

			ID = 0
			try:
				ID = int((int(rowcp['ID'][-1]) + 1)) #Recogemos el id del ultimo elemento del archivo y le sumamos 1
			except NameError:
				ID = 1 #Si no hay ningun elemento en el archivo ponemos el id a 1

			nombre = request.form['nombreProveedor']
			direccion = request.form['calleProveedor']
			telefono = request.form['telefonoProveedor']

			controles = '<button onclick="modificar({})" class="btn btn btn-outline-warning" type="button">Modificar</button><button onclick="borrar({})" class="btn btn btn-outline-danger mt-2" type="button">Borrar</button>'.format(ID, ID)

			data = {'ID': ID, 'NOMBRE': nombre, "DIRECCION": direccion, "TELEFONO": telefono, "CONTROLES": controles}

			result.append(data) #Añadimos el nuevo elemento a la lista
			writer.writerows(result) #Añadimos los datos de la lista en el nuevo archivo

	os.remove(os.getcwd()+'/Python3_SGE/datos/listaProveedors.csv')
	os.rename(os.getcwd()+'/Python3_SGE/datos/new.csv', os.getcwd()+'/Python3_SGE/datos/listaProveedors.csv')

	return json.dumps(1);

@app.route('/borrarProveedor', methods=['POST'])
def borrarProveedor():

	idProveedor = request.form['idProveedor']

	with open(os.getcwd()+'/Python3_SGE/datos/listaProveedors.csv', 'r', encoding="ISO-8859-15") as inp, open(os.getcwd()+'/Python3_SGE/datos/new.csv', 'w', encoding="ISO-8859-15") as out:

		writer = csv.DictWriter(out, dialect='unix', delimiter=";", quotechar=";",
    		fieldnames =("ID", "NOMBRE", "DIRECCION", "TELEFONO", "CONTROLES") , quoting=csv.QUOTE_MINIMAL)

		writer.writeheader() #Evitamos borrar los titulos (fieldnames)

		for rowbp in csv.DictReader(inp, dialect='unix', delimiter=";"):
			if rowbp["ID"] != idProveedor: #Creamos el nuevo archivo con todos los datos menos la fila con el id devuelto
				writer.writerow(rowbp)

	os.remove(os.getcwd()+'/Python3_SGE/datos/listaProveedors.csv') #Removemos el anterior archivo
	os.rename(os.getcwd()+'/Python3_SGE/datos/new.csv', os.getcwd()+'/Python3_SGE/datos/listaProveedors.csv') #Cambiamos el nombre del nuevo archivo al nombre del anterior

	return json.dumps(1);

@app.route('/verProveedor', methods=['POST'])
def verProveedor():

	idProveedor = request.form['idProveedor']

	datosP = []

	with open(os.getcwd()+'/Python3_SGE/datos/listaProveedors.csv', 'r', encoding="ISO-8859-15") as inp:

		for rowvp in csv.DictReader(inp, dialect='unix', delimiter=";"):

			if rowvp["ID"] == idProveedor: #Añadimos los datos del elemento seleccionado(id) a la lista
				datosP.append(rowvp['ID'])
				datosP.append(rowvp['NOMBRE'])
				datosP.append(rowvp['DIRECCION'])
				datosP.append(rowvp['TELEFONO'])

	return json.dumps({'datos':datosP}) #Devolvemos los datos en forma json

@app.route('/actualizarProveedor', methods=['POST'])
def actualizarProveedor():

	with open(os.getcwd()+'/Python3_SGE/datos/listaProveedors.csv', 'r', encoding="ISO-8859-15") as inp, open(os.getcwd()+'/Python3_SGE/datos/new.csv', 'w', encoding="ISO-8859-15") as out:

		writer = csv.DictWriter(out, dialect='unix', delimiter=";", quotechar=";",
    		fieldnames =("ID", "NOMBRE", "DIRECCION", "TELEFONO", "CONTROLES") , quoting=csv.QUOTE_MINIMAL)

		writer.writeheader()

		for rowacp in csv.DictReader(inp, dialect='unix', delimiter=";"):

			if rowacp["ID"] == request.form['idProveedor']: #Cambiamos los datos del elemto seleccionado(id) a los nuevos datos
				rowacp['NOMBRE'] = request.form['nProveedor']
				rowacp['DIRECCION'] = request.form['cProveedor']
				rowacp['TELEFONO'] = request.form['tProveedor']

			rowacp = {'ID': rowacp['ID'], 'NOMBRE': rowacp['NOMBRE'], 'DIRECCION': rowacp['DIRECCION'], 'TELEFONO': rowacp['TELEFONO'], 'CONTROLES': rowacp['CONTROLES']}
			#Añadimos esos datos al rowacp
			writer.writerow(rowacp) #Añadimos los datos el archivo

	os.remove(os.getcwd()+'/Python3_SGE/datos/listaProveedors.csv')
	os.rename(os.getcwd()+'/Python3_SGE/datos/new.csv', os.getcwd()+'/Python3_SGE/datos/listaProveedors.csv')

	return json.dumps(1);

@app.route('/ventas.html')
def ventas():
	if 'loginC' in session:

		if session['loginC']:

			valido = False

			with open(os.getcwd()+'/Python3_SGE/datos/listaDepartamentos.csv', 'r', encoding="ISO-8859-15") as File:

				reader = csv.reader(File, delimiter=';', quotechar=';',
                        quoting=csv.QUOTE_MINIMAL)

				for row in reader: #Comprobamos si el usuario logueado tiene permisos para usar este modulo
					if row[0] == "3":
						for i in row[2]:
							if i == session['idUser']:
								valido = True

			if valido:
				return render_template('ventas.html')

			else:
				return render_template('inicio.html')

		else:
			return render_template('index.html')

	else:
		return render_template('index.html')

@app.route('/cargarVentas', methods=['POST'])
def cargarVentas():

	listaDatos = []

	with open(os.getcwd()+'/Python3_SGE/datos/listaVentas.csv', 'r', encoding="ISO-8859-15") as lc:

		readerlc = csv.reader(lc, delimiter=';', quotechar=';',
	                       quoting=csv.QUOTE_MINIMAL)

		next(readerlc)

		index = 0 #Cantidad de elementos que tiene el archivo listaCompra.csv
		borrarP = 2 #Posicion en la que borrar el id del proveedor
		borrarI = 1 #Posicion en la que borrar el id del invenario

		for rowlc in readerlc:

			datos = []

			for i in rowlc:

				datos.append(i)
				index += 1

				if index == 7:

					index = 0

				if index == 2:
					with open(os.getcwd()+'/Python3_SGE/datos/listaInventario.csv', 'r', encoding="ISO-8859-15") as lp:
						readerlp = csv.reader(lp, delimiter=';', quotechar=';',	quoting=csv.QUOTE_MINIMAL)

						next(readerlp)

						for rowlp in readerlp:

							if i == rowlp[0]:

								del datos[borrarI]
								datos.append(rowlp[1])

				if index == 3:

					with open(os.getcwd()+'/Python3_SGE/datos/listaClientes.csv', 'r', encoding="ISO-8859-15") as lp:

						readerlp = csv.reader(lp, delimiter=';', quotechar=';',	quoting=csv.QUOTE_MINIMAL)

						next(readerlp)

						for rowlp in readerlp:

							if i == rowlp[0]:

								del datos[borrarP]
								datos.append(rowlp[1])

			listaDatos.append(datos)

	return json.dumps({'datos':listaDatos})

@app.route('/selectCliente', methods=['POST'])
def selectCliente():

	listaDatos = []

	with open(os.getcwd()+'/Python3_SGE/datos/listaClientes.csv', 'r', encoding="ISO-8859-15") as lc:

		readerlc = csv.reader(lc, delimiter=';', quotechar=';',
	                      quoting=csv.QUOTE_MINIMAL)

		next(readerlc)

		for rowlc in readerlc:
			datos = []
			datos.append(rowlc[0])
			datos.append(rowlc[1])
			listaDatos.append(datos)

	return json.dumps({'datos':listaDatos})

@app.route('/crearVenta', methods=['POST'])
def crearVenta():

	result = []

	with open(os.getcwd()+'/Python3_SGE/datos/listaVentas.csv', 'r', encoding="ISO-8859-15") as inp, open(os.getcwd()+'/Python3_SGE/datos/new.csv', 'w', encoding="ISO-8859-15") as out:
	
			writer = csv.DictWriter(out, delimiter=";", quotechar=";",
	    		fieldnames =("ID", "PRODUCTO", "CLIENTE", "CANTIDAD", "PRECIO", "TOTAL", "CONTROLES"), quoting=csv.QUOTE_MINIMAL)
			
			writer.writeheader()
	
			readercp = csv.DictReader(inp, delimiter=";") #Leer archivo viejo
	
			for rowcp in readercp:
				result.append(rowcp) #Guardamos los datos del archivo viejo en una lista
	
			ID = 0
			try:
				ID = int((int(rowcp['ID'][-1]) + 1)) #Recogemos el id del ultimo elemento del archivo y le sumamos 1
			except NameError:
				ID = 1 #Si no hay ningun elemento en el archivo ponemos el id a 1
	
			producto = request.form['sProductos']
			cliente = request.form['sCliente']
			cantidad = str(request.form['cantidadCP'])
			precio = str(request.form['precioCP']) + "$"
			total = str(request.form['totalCP']) + "$"
			controles = '<button onclick="vender({})" class="btn btn btn-outline-warning" type="button">Vender</button><button onclick="borrar({})" class="btn btn btn-outline-danger mt-2" type="button">Borrar</button>'.format(ID, ID)
			
			data = {'ID': ID, 'PRODUCTO': producto, "CLIENTE": cliente, "CANTIDAD": cantidad, "PRECIO": precio, "TOTAL": total, "CONTROLES": controles}
			
			result.append(data) #Añadimos el nuevo elemento a la lista
			writer.writerows(result) #Añadimos los datos de la lista en el nuevo archivo
	
	os.remove(os.getcwd()+'/Python3_SGE/datos/listaVentas.csv')
	os.rename(os.getcwd()+'/Python3_SGE/datos/new.csv', os.getcwd()+'/Python3_SGE/datos/listaVentas.csv')

	return json.dumps(1);

@app.route('/borrarVenta', methods=['POST'])
def borrarVenta():

	idCompra = request.form['idCompra']

	with open(os.getcwd()+'/Python3_SGE/datos/listaVentas.csv', 'r', encoding="ISO-8859-15") as inp, open(os.getcwd()+'/Python3_SGE/datos/new.csv', 'w', encoding="ISO-8859-15") as out:

		writer = csv.DictWriter(out, dialect='unix', delimiter=";", quotechar=";",
    		fieldnames =("ID", "PRODUCTO", "CLIENTE", "CANTIDAD", "PRECIO", "TOTAL", "CONTROLES") , quoting=csv.QUOTE_MINIMAL)

		writer.writeheader() #Evitamos borrar los titulos (fieldnames)

		for rowbp in csv.DictReader(inp, dialect='unix', delimiter=";"):
			if rowbp["ID"] != idCompra: #Creamos el nuevo archivo con todos los datos menos la fila con el id devuelto
				writer.writerow(rowbp)

	os.remove(os.getcwd()+'/Python3_SGE/datos/listaVentas.csv') #Removemos el anterior archivo
	os.rename(os.getcwd()+'/Python3_SGE/datos/new.csv', os.getcwd()+'/Python3_SGE/datos/listaVentas.csv') #Cambiamos el nombre del nuevo archivo al nombre del anterior

	return json.dumps(1);

@app.route('/realizarVenta', methods=['POST'])
def realizarVenta():

	ridVenta = request.form['idVenta']

	rproducto = ""
	rcliente = ""
	rcantidad = ""
	rprecio = ""
	rtotal = ""

	rproductoNombre = ""

	now = datetime.datetime.now()

	with open(os.getcwd()+'/Python3_SGE/datos/listaVentas.csv', 'r', encoding="ISO-8859-15") as inp:

		for rowvp in csv.DictReader(inp, delimiter=";"):
	
			if rowvp["ID"] == ridVenta:
				rproducto = rowvp['PRODUCTO']
				rcliente = rowvp['CLIENTE']
				rcantidad = rowvp['CANTIDAD']
				rprecio = rowvp['PRECIO']
				rtotal = rowvp['TOTAL']

	with open(os.getcwd()+'/Python3_SGE/datos/listaInventario.csv', 'r', encoding="ISO-8859-15") as inp:

		for rowvp in csv.DictReader(inp, delimiter=";"):
	
			if rowvp["ID"] == rproducto:
				rproductoNombre = rowvp['NOMBRE']

	result = []
	
	with open(os.getcwd()+'/Python3_SGE/datos/listaInventario.csv', 'r', encoding="ISO-8859-15") as inp, open(os.getcwd()+'/Python3_SGE/datos/new.csv', 'w', encoding="ISO-8859-15") as out:
	
			writer = csv.DictWriter(out, delimiter=";", quotechar=";",
	    		fieldnames =("ID", "NOMBRE", "TIPO", "CANTIDAD", "PRECIO_COMPRA", "PRECIO_VENTA", "CONTROLES") , quoting=csv.QUOTE_MINIMAL)
	
			writer.writeheader()
	
			for rowacp in csv.DictReader(inp, delimiter=";"):
	
				if rowacp["ID"] == rproducto: #Cambiamos los datos del elemto seleccionado(id) a los nuevos datos
					rowacp['CANTIDAD'] = int(rowacp['CANTIDAD']) - int(rcantidad)
	
				rowacp = {'ID': rowacp['ID'], 'NOMBRE': rowacp['NOMBRE'], 'TIPO': rowacp['TIPO'], 'CANTIDAD': rowacp['CANTIDAD'], 'PRECIO_COMPRA': rowacp['PRECIO_COMPRA'], 'PRECIO_VENTA': rowacp['PRECIO_VENTA'], 'CONTROLES': rowacp['CONTROLES']}
				#Añadimos esos datos al rowacp
				writer.writerow(rowacp) #Añadimos los datos el archivo
	
	os.remove(os.getcwd()+'/Python3_SGE/datos/listaInventario.csv')
	os.rename(os.getcwd()+'/Python3_SGE/datos/new.csv', os.getcwd()+'/Python3_SGE/datos/listaInventario.csv')

	
	with open(os.getcwd()+'/Python3_SGE/datos/listaVentas.csv', 'r', encoding="ISO-8859-15") as inp, open(os.getcwd()+'/Python3_SGE/datos/new.csv', 'w', encoding="ISO-8859-15") as out:
		
		writer = csv.DictWriter(out, delimiter=";", quotechar=";",
	   		fieldnames =("ID", "PRODUCTO", "CLIENTE", "CANTIDAD", "PRECIO", "TOTAL", "CONTROLES") , quoting=csv.QUOTE_MINIMAL)
	
		writer.writeheader() #Evitamos borrar los titulos (fieldnames)
	
		for rowbp in csv.DictReader(inp, delimiter=";"):
			if rowbp["ID"] != ridVenta: #Creamos el nuevo archivo con todos los datos menos la fila con el id devuelto
				writer.writerow(rowbp)
	
	os.remove(os.getcwd()+'/Python3_SGE/datos/listaVentas.csv') #Removemos el anterior archivo
	os.rename(os.getcwd()+'/Python3_SGE/datos/new.csv', os.getcwd()+'/Python3_SGE/datos/listaVentas.csv')

	return json.dumps(1);

@app.route('/cliente.html')
def cliente():
	if 'loginC' in session:

		if session['loginC']:

			valido = False

			with open(os.getcwd()+'/Python3_SGE/datos/listaDepartamentos.csv', 'r', encoding="ISO-8859-15") as File:

				reader = csv.reader(File, delimiter=';', quotechar=';',
                        quoting=csv.QUOTE_MINIMAL)

				for row in reader: #Comprobamos si el usuario logueado tiene permisos para usar este modulo
					if row[0] == "3":
						for i in row[2]:
							if i == session['idUser']:
								valido = True

			if valido:
				return render_template('cliente.html')

			else:
				return render_template('inicio.html')

		else:
			return render_template('index.html')

	else:
		return render_template('index.html')

@app.route('/cargarClientes', methods=['POST'])
def cargarClientes():

	listaDatos = []

	with open(os.getcwd()+'/Python3_SGE/datos/listaClientes.csv', 'r', encoding="ISO-8859-15") as lc:

		readerlc = csv.reader(lc, delimiter=';', quotechar=';',
	                       quoting=csv.QUOTE_MINIMAL)

		next(readerlc)

		index = 0 #Cantidad de elementos que tiene el archivo listaCompra.csv
		borrarP = 2 #Posicion en la que borrar el id del proveedor
		borrarI = 1 #Posicion en la que borrar el id del invenario

		for rowlc in readerlc:

			datos = []

			for i in rowlc:

				datos.append(i)

			listaDatos.append(datos)

	return json.dumps({'datos':listaDatos})

@app.route('/newCliente', methods=['POST'])
def newCliente():

	result = []

	with open(os.getcwd()+'/Python3_SGE/datos/listaClientes.csv', 'r', encoding="ISO-8859-15") as inp, open(os.getcwd()+'/Python3_SGE/datos/new.csv', 'w', encoding="ISO-8859-15") as out:

			writer = csv.DictWriter(out, dialect='unix', delimiter=";", quotechar=";",
	    		fieldnames =("ID", "NOMBRE", "DIRECCION", "TELEFONO", "CONTROLES"), quoting=csv.QUOTE_MINIMAL)

			writer.writeheader()

			readercp = csv.DictReader(inp, dialect='unix', delimiter=";") #Leer archivo viejo

			for rowcp in readercp:
				result.append(rowcp) #Guardamos los datos del archivo viejo en una lista

			ID = 0
			try:
				ID = int((int(rowcp['ID'][-1]) + 1)) #Recogemos el id del ultimo elemento del archivo y le sumamos 1
			except NameError:
				ID = 1 #Si no hay ningun elemento en el archivo ponemos el id a 1

			nombre = request.form['nombreCliente']
			direccion = request.form['calleCliente']
			telefono = request.form['telefonoCliente']

			controles = '<button onclick="modificar({})" class="btn btn btn-outline-warning" type="button">Modificar</button><button onclick="borrar({})" class="btn btn btn-outline-danger mt-2" type="button">Borrar</button>'.format(ID, ID)

			data = {'ID': ID, 'NOMBRE': nombre, "DIRECCION": direccion, "TELEFONO": telefono, "CONTROLES": controles}

			result.append(data) #Añadimos el nuevo elemento a la lista
			writer.writerows(result) #Añadimos los datos de la lista en el nuevo archivo

	os.remove(os.getcwd()+'/Python3_SGE/datos/listaClientes.csv')
	os.rename(os.getcwd()+'/Python3_SGE/datos/new.csv', os.getcwd()+'/Python3_SGE/datos/listaClientes.csv')

	return json.dumps(1);

@app.route('/borrarCliente', methods=['POST'])
def borrarCliente():

	idCliente = request.form['idCliente']

	with open(os.getcwd()+'/Python3_SGE/datos/listaClientes.csv', 'r', encoding="ISO-8859-15") as inp, open(os.getcwd()+'/Python3_SGE/datos/new.csv', 'w', encoding="ISO-8859-15") as out:

		writer = csv.DictWriter(out, dialect='unix', delimiter=";", quotechar=";",
    		fieldnames =("ID", "NOMBRE", "DIRECCION", "TELEFONO", "CONTROLES") , quoting=csv.QUOTE_MINIMAL)

		writer.writeheader() #Evitamos borrar los titulos (fieldnames)

		for rowbp in csv.DictReader(inp, dialect='unix', delimiter=";"):
			if rowbp["ID"] != idCliente: #Creamos el nuevo archivo con todos los datos menos la fila con el id devuelto
				writer.writerow(rowbp)

	os.remove(os.getcwd()+'/Python3_SGE/datos/listaClientes.csv') #Removemos el anterior archivo
	os.rename(os.getcwd()+'/Python3_SGE/datos/new.csv', os.getcwd()+'/Python3_SGE/datos/listaClientes.csv') #Cambiamos el nombre del nuevo archivo al nombre del anterior

	return json.dumps(1);

@app.route('/verCliente', methods=['POST'])
def verCliente():

	idCliente = request.form['idCliente']

	datosP = []

	with open(os.getcwd()+'/Python3_SGE/datos/listaClientes.csv', 'r', encoding="ISO-8859-15") as inp:

		for rowvp in csv.DictReader(inp, dialect='unix', delimiter=";"):

			if rowvp["ID"] == idCliente: #Añadimos los datos del elemento seleccionado(id) a la lista
				datosP.append(rowvp['ID'])
				datosP.append(rowvp['NOMBRE'])
				datosP.append(rowvp['DIRECCION'])
				datosP.append(rowvp['TELEFONO'])

	return json.dumps({'datos':datosP}) #Devolvemos los datos en forma json

@app.route('/actualizarCliente', methods=['POST'])
def actualizarCliente():

	with open(os.getcwd()+'/Python3_SGE/datos/listaClientes.csv', 'r', encoding="ISO-8859-15") as inp, open(os.getcwd()+'/Python3_SGE/datos/new.csv', 'w', encoding="ISO-8859-15") as out:

		writer = csv.DictWriter(out, dialect='unix', delimiter=";", quotechar=";",
    		fieldnames =("ID", "NOMBRE", "DIRECCION", "TELEFONO", "CONTROLES") , quoting=csv.QUOTE_MINIMAL)

		writer.writeheader()

		for rowacp in csv.DictReader(inp, dialect='unix', delimiter=";"):

			if rowacp["ID"] == request.form['idCliente']: #Cambiamos los datos del elemto seleccionado(id) a los nuevos datos
				rowacp['NOMBRE'] = request.form['nCliente']
				rowacp['DIRECCION'] = request.form['cCliente']
				rowacp['TELEFONO'] = request.form['tCliente']

			rowacp = {'ID': rowacp['ID'], 'NOMBRE': rowacp['NOMBRE'], 'DIRECCION': rowacp['DIRECCION'], 'TELEFONO': rowacp['TELEFONO'], 'CONTROLES': rowacp['CONTROLES']}
			#Añadimos esos datos al rowacp
			writer.writerow(rowacp) #Añadimos los datos el archivo

	os.remove(os.getcwd()+'/Python3_SGE/datos/listaClientes.csv')
	os.rename(os.getcwd()+'/Python3_SGE/datos/new.csv', os.getcwd()+'/Python3_SGE/datos/listaClientes.csv')

	return json.dumps(1);


#Inicio de la aplicación.
if __name__ == "__main__":
    app.run()