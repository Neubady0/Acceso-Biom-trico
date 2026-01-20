
import psycopg2
from src.conexion_db import DBConnection

class UsuarioDAO:
    
    @staticmethod
    def registrar_usuario(nombre, foto_bytes):
        conn = DBConnection.get_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    query = "INSERT INTO usuarios (nombre, foto) VALUES (%s, %s)"
                    cursor.execute(query, (nombre, psycopg2.Binary(foto_bytes)))
                conn.commit()
                return True
            except Exception as e:
                print(f"Error registering user: {e}")
                conn.rollback()
                return False
        return False

    @staticmethod
    def obtener_todos():
        conn = DBConnection.get_connection()
        usuarios = []
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT id, nombre, foto FROM usuarios")
                    results = cursor.fetchall()
                    for row in results:
                        # row[2] comes as bytes/memoryview
                        usuarios.append({'id': row[0], 'nombre': row[1], 'foto': bytes(row[2])})
            except Exception as e:
                print(f"Error fetching users: {e}")
        return usuarios
