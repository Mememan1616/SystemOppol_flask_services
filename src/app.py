from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
from config import config
from datetime import datetime
import base64
fecha_hora_actual = datetime.now()

hora = fecha_hora_actual.strftime("%H:%M:%S")
tomafecha = fecha_hora_actual.date()
fecha = str(tomafecha)
app=Flask(__name__)

CORS(app ,origins=["http://localhost:4200"])
conexion = MySQL(app)

@app.route('/municipios', methods=['GET'])
def mostrar_municipios():
    try:
        cursor=conexion.connection.cursor()
        sql="call municipios()"
        cursor.execute(sql)
        datos= cursor.fetchall()
        municipios=[]
        #print(datos)
        for fila in datos:
            municipio={ 'idMunicipio' : fila[0], 'municipio':fila[1]}
            municipios.append(municipio)
        
        return jsonify({'municipios':municipios, 'mensaje':"Municipios listados.", 'exito':True})
        
    except Exception as ex:
        return jsonify({'mensaje':"Error: {}".format(ex), 'exito':False})


@app.route('/colonias/<cp>', methods=['GET'])
def mostrar_colonias(cp):
    try:
        cursor=conexion.connection.cursor()
        sql="call buscaColonias('{0}')".format(cp)
        cursor.execute(sql)
        datos=cursor.fetchall()
        colonias=[]
        print(datos)
        for fila in datos:
            colonia={'idColonia': fila[0], 'colonia':fila[1]}
            colonias.append(colonia)

        return jsonify({'colonias':colonias, 'mensaje':"Colonias listadas.", 'exito':True})

    except Exception as ex:
        return jsonify({'mensaje':"Error: {}".format(ex), 'exito':False})
        

@app.route('/distritos', methods=['GET'])
def mostrar_distritos():
    try:
        cursor=conexion.connection.cursor()
        sql="select * from distritos_locales"
        cursor.execute(sql)
        datos= cursor.fetchall()
        distritos=[]
        for fila in datos:
            distrito={'idDistrito':fila[0], 'distrito': fila[1]}
            distritos.append(distrito)
        return jsonify({'distritis':distritos, 'mensaje':"Distritos listados.", 'exito':True})
    except Exception as ex:
        return jsonify({'mensaje':"Error: {}".format(ex), 'exito':False})



@app.route('/buscardistritos/<id>', methods=['GET'])
def buscar_distritos(id):
    try:
        cursor=conexion.connection.cursor()
        sql="call distrito_municipio({0})".format(id)
        cursor.execute(sql)
        datos = cursor.fetchall()
        distritos=[]
        for fila in datos:
            distrito={'idDistrito':fila[0], 'distrito': fila[1]}
            distritos.append(distrito)
        return jsonify({'distritos':distritos, 'mensaje':"Distritos listados.", 'exito':True})   


    except Exception as ex:
        return jsonify({'mensaje':"Error: {}".format(ex), 'exito':False})


@app.route('/secciones/<id1>/<id2>', methods=['GET'])
def buscar_secciones(id1,id2):
    try:
        cursor=conexion.connection.cursor()
        sql="call secciones_distrito({0},{1})".format(id1,id2)
        cursor.execute(sql)
        datos = cursor.fetchall()
        secciones=[]
        for fila in datos:
            seccion={'idSeccion':fila[0], 'seccion':fila[1]}
            secciones.append(seccion)
        return jsonify({'secciones':secciones, 'mensaje':"Secciones listadas.", 'exito':True}) 
    
    except Exception as ex:
        return jsonify({'mensaje':"Error: {}".format(ex), 'exito':False})




#-----------------------------------------------------------------------------------------------------------------


@app.route('/newusuario', methods=['POST'])
def insertar_usuarios():
    try:
        # Verificar los datos que llegaron
        print("Datos recibidos:", request.json)

        # Usar parámetros en lugar de formateo de cadenas
        cursor = conexion.connection.cursor()
        sql = """INSERT INTO usuarios (idUsuario, usuario, password, nombre, cargo_id, cargo) 
                 VALUES (null, %s, %s, %s, %s, %s)"""
        
        # Imprimir la consulta antes de ejecutarla
        print("Consulta SQL:", sql)
        
        # Ejecutar la consulta con parámetros
        cursor.execute(sql, (
            request.json['usuario'],
            request.json['password'], 
            request.json['nombre'], 
            request.json['cargoID'], 
            request.json['cargo']
        ))
        
        # Confirmar la transacción
        cursor.connection.commit()
        
        return jsonify({'mensaje': "Usuario registrado.", 'exito': True})
    except Exception as ex:
        print("Error al insertar usuario:", ex)
        return jsonify({'mensaje': f"Error: {ex}", 'exito': False})


@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    try:
        cursor=conexion.connection.cursor()
        sql="call usuarios()"
        cursor.execute(sql)
        datos = cursor.fetchall()
        usuarios=[]
        for fila in datos:
            usuario={'idUsuario':fila[0], 'usuario':fila[1] ,'nombre':fila[2], 'cargo':fila[3]}
            usuarios.append(usuario)
        return jsonify({'usuarios':usuarios, 'mensaje':"Usuarios listados.", 'exito':True}) 
    
    except Exception as ex:
        return jsonify({'mensaje':"Error: {}".format(ex), 'exito':False})


@app.route('/validaUsuario/<user>/<password>', methods=['GET'])
def valida_usuarios(user,password):
    try:
        cursor=conexion.connection.cursor()
        sql="call validarUsuario('{0}','{1}')".format(user, password)
        print(sql)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            usuario={'idUsuario':datos[0],'usuario':datos[1],  'cargoID':datos[2]}
            return usuario
        else:
            return None
    
        return jsonify({'usuarios':usuarios, 'mensaje':"Usuarios listados.", 'exito':True}) 
    
    except Exception as ex:
        return jsonify({'mensaje':"Error: {}".format(ex), 'exito':False})

@app.route('/buscar_usuario/<id>', methods=['GET'])
def buscar_usuario(id):
    try:
        cursor=conexion.connection.cursor()
        sql="select*from usuarios where idUsuario={0}".format(id)
        #print(sql)
        cursor.execute(sql)
        datos=cursor.fetchone()
        if datos != None:
            usuario={'idUsuario':datos[0], 'usuario':datos[1], 'password':datos[2],'nombre':datos[3], 'cargoID':datos[4]}
            return usuario
        else:
            return None
    except Exception as ex:
        return jsonify({'mensaje':"Error: {}".format(ex), 'exito':False})



@app.route('/eliminar_usuario/<id>', methods=['PUT'])
def eliminar_usuario(id):
    #print(f"Solicitud recibida para eliminar usuario con ID: {id}")
    try:
        cursor = conexion.connection.cursor()
        sql = "CALL borrarUsuario({0})".format(id)
        #print(f"SQL: {sql} - ID: {id}")
        cursor.execute(sql)
        cursor.connection.commit()
        return jsonify({'mensaje': "Usuario eliminado.", 'exito': True})
    except Exception as ex:
        #print(f"Error al eliminar el usuario: {ex}")
        return jsonify({'mensaje': f"Error: {ex}", 'exito': False}), 500



@app.route('/modificar_usuario/<id>', methods=['PUT'])
def modificar_usuario(id):
    try:
        cursor=conexion.connection.cursor()
        sql="call modificarUsuario({0},'{1}','{2}','{3}',{4},'{5}')".format(
                    id,
                    request.json['usuario'],
                    request.json['password'],
                    request.json['nombre'],
                    request.json['cargoID'],
                    request.json['cargo'],
                    )
        print(sql)
        cursor.execute(sql)
        cursor.connection.commit()
        return jsonify({'mensaje': sql , 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje':"Error: {}".format(ex), 'exito':False})
    

#-----------------------------------------------------------------------------------------------------------------

@app.route('/simpatizantes', methods=['POST'])
def insertar_simpatizantes():
    try:
        cursor=conexion.connection.cursor()
        
        apellidoP= request.json['apellidoP']
        apellidoM= request.json['apellidoM']
        nombre=request.json['nombre']
        fechaN=request.json['fechaN']
        telefono=request.json['telefono']
        correo=request.json['correo']
        distrito=request.json['distrito']
        municipio=request.json['municipio']
        seccion=request.json['seccion']
        codigoP=request.json['codigoP']
        colonia=request.json['colonia']
        direccion= request.json['direccion']
        vinculacion=request.json['vinculacion']
        liderazgo=request.json['liderazgo']
        fcredencial=request.json['fcredencial']
        bcredencial=request.json['bcredencial']

       

        sql=""" INSERT INTO simpatizantes( 
        apellidoP, apellidoM, nombre, fecha_registro, hora_registro, 
        fecha_nacimiento, whatsapp, email, id_distrito_local, id_municipio,
        seccion, 
        codigo_postal, id_colonia, 
        direccion, 
        tipo_vinculacion, 
        liderazgo_id, 
        credencial_front, credencial_back) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
        values=(apellidoP,apellidoM,nombre,
        fecha,hora,fechaN,
        telefono,correo,
        distrito,municipio,seccion,codigoP,
        colonia,direccion,
        vinculacion, liderazgo, 
        fcredencial, bcredencial)

        #print(values)
        cursor.execute(sql, values)

        #print("Consulta ejecutada correctamente.")

        cursor.connection.commit()
        print("Transacción confirmada.")

        return jsonify({'mensaje': "Registro completado", 'exito': True})
        
    except Exception as ex:
        import traceback
        print("Error en el servidor:", traceback.format_exc())  # Más detalles en consola
        return jsonify({'mensaje': "Error en el servidor.", 'exito': False})


#---------------------------------------
@app.route('/simpatizantes', methods=['GET'])
def simpatizantes():
    try:
        cursor=conexion.connection.cursor()
        sql="call listarSimpatizantes()"
        cursor.execute(sql)
        datos = cursor.fetchall()
        simpatizantes=[]
        for fila in datos:
            s={'idSimpatizante':fila[0], 'seccion':fila[1] ,'distrito':fila[2], 
            'apellidoP':fila[3], 'apellidoM': fila[4], 'nombre':fila[5],
            'encuestador':fila[6]
            }
            simpatizantes.append(s)
        return jsonify({'simpatizantes':simpatizantes, 'mensaje':"Simpatizantes listados.", 'exito':True}) 

    except Exception as ex:
        import traceback
        print("Error en el servidor:", traceback.format_exc())  # Más detalles en consola
        return jsonify({'mensaje': "Error en el servidor.", 'exito': False})

@app.route('/buscarSimpatizante/<id>', methods=['GET'])
def buscarSimpatizante(id):
    try:
        cursor=conexion.connection.cursor()
        sql="call buscaSimpatizante({0})".format(id) 
        cursor.execute(sql)
        datos=cursor.fetchone()
        if datos != None:
            usuario={
            'idSimpatizante': datos[0], 'apellidoP': datos[1], 
                'apellidoM': datos[2], 'nombre': datos[3], #'fecha_reg': datos[4],
                #'hora_reg': datos[5].strftime('%H:%M:%S') if datos[5] else None, 
                'fechaNac': datos[6], 'telefono': datos[7],
                'correo': datos[8], 'distrito': datos[9], 'municipio': datos[10],
                'seccion': datos[11], 'cp': datos[12], 'colonia': datos[13],
                'direccion': datos[14], 'vinculacion': datos[15], 'lid': datos[16],
                # Si necesitas estas claves, descoméntalas:
                'fcredencial': str(datos[17]),
                'bcredencial': str(datos[18])
            }
            return usuario
        else:
            return None
        
    except Exception as ex:
        import traceback
        print("Error en el servidor:", traceback.format_exc())  # Más detalles en consola
        return jsonify({'mensaje': "Error en el servidor.", 'exito': False})

@app.route('/modificar_sp/<id>', methods=['PUT'])
def modificar_sp(id):
    try:
        cursor=conexion.connection.cursor()
        sql="call editaSimpatizante({0},'{1}','{2}','{3}','{4}','{5}','{6}',{7},{8},'{9}','{10}',{11},'{12}','{13}',{14})".format(
                    id,
                    request.json['apellidoP'],
                    request.json['apellidoM'],
                    request.json['nombre'],
                    request.json['fechaN'],
                    request.json['telefono'],
                    request.json['correo'],
                    request.json['distrito'],
                    request.json['municipio'],
                    request.json['seccion'],
                    request.json['codigoP'],
                    request.json['colonia'],
                    request.json['direccion'],
                    request.json['vinculacion'],
                    request.json['liderazgo'],
                    )
        print(sql)
        cursor.execute(sql)
        cursor.connection.commit()
        return jsonify({'mensaje': sql , 'exito': True})
    except Exception as ex:
        return jsonify({'mensaje':"Error: {}".format(ex), 'exito':False})

@app.route('/eliminar_sp/<id>', methods=['PUT'])
def eliminar_sp(id):
    #print(f"Solicitud recibida para eliminar usuario con ID: {id}")
    try:
        cursor = conexion.connection.cursor()
        sql = "CALL eliminaSimpatizante({0})".format(id)
        #print(f"SQL: {sql} - ID: {id}")
        cursor.execute(sql)
        cursor.connection.commit()
        return jsonify({'mensaje': "simpatizante eliminado.", 'exito': True})
    except Exception as ex:
        #print(f"Error al eliminar el usuario: {ex}")
        return jsonify({'mensaje': f"Error: {ex}", 'exito': False}), 500

def pagina_no_encontrada(error):
    return"<h1>Pagina no encontrada</h1>",404

if __name__=='__main__':
    app.config.from_object(config['develoment'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()