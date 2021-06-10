import mysql.connector
import hashlib #para hasheo

bd = mysql.connector.connect(
    user = 'ximena', password = '123',
    database = 'songapp'
)

cursor = bd.cursor() #lo que hará la conexión del
                     #script y la base de datos


#USUARIOS******************************
def get_usuarios():
    consulta = "SELECT * FROM usuario"

    cursor.execute(consulta)
    usuarios = []
    for row in cursor.fetchall():
        usuario = {
            "id": row[0],
            "correo": row[1],
            "contrasenia": row[2]
        }
        usuarios.append(usuario)
    return usuarios

def existe_usuario(correo):
    query = "SELECT COUNT(*) FROM usuario WHERE correo = %s"
    cursor.execute(query, (correo,)) #tupla de un elemento

    if cursor.fetchone()[0] == 1:
        return True
    else:
        return False


def crear_usuarios(correo, contrasenia):
    if existe_usuario(correo):
        return False
    else:
        h = hashlib.new("sha256", bytes(contrasenia, "utf-8")) 
        h = h.hexdigest() #cadena
        insertar = "INSERT INTO usuario(correo, contrasenia) VALUES(%s, %s)"
        cursor.execute(insertar, (correo, h))

        bd.commit()
        return True

def iniciar_sesion(correo, contrasenia):
    h = hashlib.new("sha256", bytes(contrasenia, "utf-8")) 
    h = h.hexdigest() #cadena
    query = "SELECT id FROM usuario WHERE correo = %s AND contrasenia = %s"
    cursor.execute(query, (correo, h))
    identificacion = cursor.fetchone()
    if identificacion:
        return identificacion[0], True
    else:
        return None, False

#ARTISTA~~~~~~~~~~~~
def insertar_artista(artista):
    nombre = artista['nombre']
    genero = artista['genero']
    biografia = artista['biografia']
    imagen = artista['imagen']

    usuarioId = artista['usuarioId']

    insertar = "INSERT INTO artista \
            (nombre, genero, biografia, imagen, usuarioId) \
            VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(insertar, 
    (nombre, genero, biografia, imagen, usuarioId))
    bd.commit()

    if cursor.rowcount:
        return True
    else:
        return False

def get_artistas():
    query = "SELECT id, nombre, genero, imagen, biografia FROM artista"
    cursor.execute(query)
    artistas = []
    for row in cursor.fetchall():
        artista = {
            'id': row[0],
            'nombre': row[1],
            'genero': row[2],
            'imagen': row[3],
            'biografia': row[4]
        }
        artistas.append(artista)
    
    return artistas

def get_artista(id):
    query = "SELECT * FROM artista WHERE id = %s"
    cursor.execute(query, (id,))
    artista = {}
    row = cursor.fetchone()
    if row: # si row tiene info
        artista['id'] = row[0]
        artista['nombre'] = row[1]
        artista['genero'] = row[2]
        artista['biografia'] = row[3]
        artista['imagen'] = row[4]

    return artista

# def modificar_artista(id, columna, valor):
#     update = f"UPDATE artista SET {columna} = %s WHERE id = %s"
#     cursor.execute(update, (valor, id))
#     bd.commit()

#     if cursor.rowcount:
#         return True
#     else:
#         return False

# def eliminar_artista(id):
#     eliminar = "DELETE from artista WHERE id = %s"
#     cursor.execute(eliminar, (id,))
#     bd.commit()

#     if cursor.rowcount:
#         return True
#     else:
#         return False


#ALBUM***************************
def insertar_album(album):
    titulo = album['titulo']
    anio = album['anio']
    n_tracks = album['n_tracks']
    imagen = album['imagen']

    artistaId = album['artistaId']

    insertar = "INSERT INTO album \
            (titulo, anio, n_tracks, imagen, artistaId) \
            VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(insertar, 
    (titulo, anio, n_tracks, imagen, artistaId))
    bd.commit()

    if cursor.rowcount:
        return True
    else:
        return False

def get_albumess():
    query = "SELECT id, titulo, anio, n_tracks, imagen FROM album"
    cursor.execute(query)
    albumes = []
    for row in cursor.fetchall():
        album = {
            'id': row[0],
            'titulo': row[1],
            'anio': row[2],
            'n_tracks': row[3],
            'imagen': row[4]
        }
        albumes.append(album)
    
    return albumes

def get_albumes(artistaId):
    query = "SELECT * FROM album WHERE artistaId = %s"
    cursor.execute(query, (artistaId,))
    album = {}
    row = cursor.fetchone()
    if row: # si row tiene info
        album['id'] = row[0]
        album['titulo'] = row[1]
        album['anio'] = row[2]
        album['n_tracks'] = row[3]
        album['imagen'] = row[4]

    return album

def modificar_album(id, link):
    update = f"UPDATE album SET imagen = %s WHERE id = %s"
    cursor.execute(update, (link, id))
    bd.commit()

    if cursor.rowcount:
        return True
    else:
        return False

def eliminar_album(id):
    eliminar = "DELETE from album WHERE id = %s"
    cursor.execute(eliminar, (id,))
    bd.commit()

    if cursor.rowcount:
        return True
    else:
        return False

#TRACK***************************
def insertar_track(track):
    titulo = track['titulo']
    duracion = track['duracion']
    lyrics = track['lyrics']

    albumId = track['albumId']

    insertar = "INSERT INTO track \
            (titulo, duracion, lyrics, albumId) \
            VALUES (%s, %s, %s, %s)"
    cursor.execute(insertar, 
    (titulo, duracion, lyrics, albumId))
    bd.commit()

    if cursor.rowcount:
        return True
    else:
        return False

def get_trackss():
    query = "SELECT id, titulo, duracion, lyrics, albumId FROM track"
    cursor.execute(query)
    tracks = []
    for row in cursor.fetchall():
        track = {
            'id': row[0],
            'titulo': row[1],
            'duracion': row[2],
            'lyrics': row[3],
            'albumId': row[4]
        }
        tracks.append(track)
    
    return tracks

def get_tracks(albumId):
    query = "SELECT * FROM track WHERE albumId = %s"
    cursor.execute(query, (albumId,))
    track = {}
    row = cursor.fetchone()
    if row: # si row tiene info
        track['id'] = row[0]
        track['titulo'] = row[1]
        track['duracion'] = row[2]
        track['lyrics'] = row[3]
        track['albumId'] = row[4]

    return track

def modificar_track(titulo, columna, valor): 
    #formato
    # {
    #     "titulo": "blabla",
    #     "columna": "titulo",
    #     "valor": "blabla"
    # }
    update = f"UPDATE track SET {columna} = %s WHERE titulo = %s"
    cursor.execute(update, (valor, titulo))
    bd.commit()

    if cursor.rowcount:
        return True
    else:
        return False

def eliminar_track(albumId, titulo):
    # formato
    # {
    #     "titulo": "blabla"
    # }
    eliminar = "DELETE from track WHERE albumId = %s AND titulo = %s"
    cursor.execute(eliminar, (albumId, titulo))
    bd.commit()

    if cursor.rowcount:
        return True
    else:
        return False

# def get_peliculas_usuario(id):
#     query = "SELECT * FROM pelicula WHERE usuarioId = %s"
#     cursor.execute(query, (id,))
#     peliculas = []
#     for row in cursor.fetchall():
#         pelicula = {
#             'id': row[0],
#             'titulo': row[1],
#             'fecha_visto': row[2],
#             'imagen': row[3],
#             'director': row[4],
#             'anio': row[5],
#             'valoracion': row[6],
#             'favorito': row[7],
#             'resenia': row[8],
#             'compartido': row[9]
#         }
#         peliculas.append(pelicula)
#     return peliculas