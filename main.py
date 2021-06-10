from flask import Flask, jsonify, request

from conexion import crear_usuarios, get_usuarios, iniciar_sesion
from conexion import insertar_artista, get_artista, insertar_album, get_albumes, get_albumess
from conexion import modificar_album, eliminar_album, get_artistas

from conexion import insertar_track, modificar_track, eliminar_track, get_tracks, get_trackss
app = Flask(__name__)

@app.route("/api/v2/usuario", methods = ["POST", "GET"])
@app.route("/api/v2/usuario/<int:id>/artistas", methods = ["GET"])
#@app.route("/api/v1/usuarios/<int:id>/artistas/albumes", methods = ["GET"])
def usuario(id = None):
    if request.method == "POST" and request.is_json:
        try:
            data = request.get_json()
            print(data)

            if crear_usuarios(data["correo"], data["contrasenia"]):
                return jsonify({"code": "ok"})
            else:
                return jsonify({"code": "existe"})
        except:
            return jsonify({"code": "error"})
    elif request.method == "GET" and id is not None:
        return jsonify(get_artista(id))
    
    # elif request.method == "GET" and id is not None:
    #     return jsonify(get_albumes(id))
    
    # elif request.method == "GET" and id is not None:
    #     return jsonify(get_tracks_album(id))

@app.route("/api/v2/usuarios", methods = ["GET"])
def getUsuarios():
    if request.method == "GET":
        users = get_usuarios()

    return jsonify(users)

@app.route("/api/v2/sesiones", methods = ["POST"])
def sesion():
    if request.method == "POST" and request.is_json:
        try:
            data = request.get_json()
            correo = data["correo"]
            contrasenia = data["contrasenia"]
            print(correo, contrasenia)
            identificacion, ok = iniciar_sesion(correo, contrasenia)
            if ok:
                return jsonify({"code": "ok", "id": identificacion})
            else:
                return jsonify({"code": "noexiste"})
        except:
            return jsonify({"code": "error"})

@app.route("/api/v2/artistas", methods=["GET", "POST"])
@app.route("/api/v2/artistas/<int:id>", methods=["GET"]) 
def artistas(id = None):
    if request.method == "POST" and request.is_json:
        try:
            data = request.get_json()
            print(data)
            if insertar_artista(data):
                return jsonify({"code": "ok"})
            else:
                return jsonify({"code": "no"})
        except:
            return jsonify({"code": "errorArtista"})
    elif request.method == "GET" and id is None:
        return jsonify(get_artistas())
    elif request.method == "GET" and id is not None:
        return jsonify(get_artista(id))
    # elif request.method == "PATCH" and id is not None and request.is_json:
    #     data = request.get_json()
    #     columna = data['columna']
    #     valor = data['valor']

    #     if modificar_artista(id, columna, valor):
    #         return jsonify(code='ok')
    #     else:
    #         return jsonify(code='error')
    # elif request.method == "DELETE" and id is not None:
    #     if eliminar_artista(id):
    #         return jsonify(code='ok')
    #     else:
    #         return jsonify(code='ok')

@app.route("/api/v2/albumes", methods=["GET", "POST"])
@app.route("/api/v2/albumes/<int:artistaId>", methods=["GET", "PATCH", "DELETE"]) 
def albumes(artistaId = None):
    if request.method == "POST" and request.is_json:
        try:
            data = request.get_json()
            print(data)
            if insertar_album(data):
                return jsonify({"code": "ok"})
            else:
                return jsonify({"code": "no"})
        except:
            return jsonify({"code": "errorAlbum"})
    elif request.method == "GET" and artistaId is None:
        return jsonify(get_albumess())
    elif request.method == "GET" and artistaId is not None:
        return jsonify(get_albumes(artistaId))
    elif request.method == "PATCH" and artistaId is not None and request.is_json:
        data = request.get_json()
        albumId = data["albumId"]
        link = data['link']

        if modificar_album(albumId, link):
            return jsonify({"code": 'ok'})
        else:
            return jsonify({"code": 'error'})
    elif request.method == "DELETE" and artistaId is not None:
        data = request.get_json()
        albumId = data["albumId"]

        if eliminar_album(albumId):
            return jsonify({"code": 'ok'})
        else:
            return jsonify({"code": 'ok'})

@app.route("/api/v2/tracks", methods=["GET", "POST"])
@app.route("/api/v2/tracks/<int:albumId>", methods=["GET", "PATCH", "DELETE"]) 
def tracks(albumId = None):
    if request.method == "POST" and request.is_json:
        try:
            data = request.get_json()
            print(data)
            if insertar_track(data):
                return jsonify({"code": "ok"})
            else:
                return jsonify({"code": "no"})
        except:
            return jsonify({"code": "errorTracks"})
    elif request.method == "GET" and albumId is None:
        return jsonify(get_trackss())
    elif request.method == "GET" and albumId is not None:
        return jsonify(get_tracks(albumId))
    elif request.method == "PATCH" and albumId is not None and request.is_json:
        data = request.get_json()
        titulo = data["titulo"]
        columna = data['columna']
        valor = data['valor']

        if modificar_track(titulo, columna, valor):
            return jsonify(code='ok')
        else:
            return jsonify(code='error')
    elif request.method == "DELETE" and albumId is not None:
        data = request.get_json()
        titulo = data["titulo"]

        if eliminar_track(albumId, titulo):
            return jsonify(code = 'ok')
        else:
            return jsonify(code = 'error')


app.run(debug = True) #Para que se recargue la página si modificamos algo
