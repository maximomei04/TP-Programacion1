import re
from funciones import leer_funciones
from reservas import leer_reservas
import Main
import os  # <--- IMPORTANTE

ARCHIVO_USUARIOS = "archivos/usuarios.txt"
ARCHIVO_TEMP = "archivos/usuarios_temp.txt"

patron_email = re.compile(r'^[\w\.-]+@[\w\.-]+\.\w+$')
patron_telefono = re.compile(r'^\d{8,12}$')


def _obtener_ultimo_id(archivo, id_columna=0):
    """
    Lee el archivo linea por linea para encontrar el ID más alto
    en la columna especificada, sin cargar todo a memoria.
    """
    ultimo_id = 0
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea:
                    try:
                        partes = linea.split(";")
                        id_actual = int(partes[id_columna])
                        if id_actual > ultimo_id:
                            ultimo_id = id_actual
                    except (ValueError, IndexError):
                        continue  # Ignorar lineas mal formadas
    except FileNotFoundError:
        pass  # Si no hay archivo, el ultimo ID es 0
    return ultimo_id


def leer_usuarios():
    """
    Se mantiene igual, se usa para 'Mostrar Usuarios' y reportes.
    """
    usuarios = []
    try:
        with open(ARCHIVO_USUARIOS, 'r', encoding='utf-8') as f:
            for linea in f:
                linea = linea.strip() 
                if linea: 
                    try:
                        partes = linea.split(';')

                        usuario = [
                            int(partes[0]),   
                            partes[1],        
                            partes[2],        
                            partes[3],        
                            int(partes[4])    
                        ]
                        usuarios.append(usuario)
                    except (ValueError, IndexError):
                        print(f"Error: Se omitió una línea mal formada en {ARCHIVO_USUARIOS}")
    except FileNotFoundError:
        print(f"Nota: No se encontró {ARCHIVO_USUARIOS}, se creará uno nuevo al guardar.")

    return usuarios


def guardar_usuarios(usuarios):
    """
    Se mantiene, pero ya no es usada por crear/modificar/borrar.
    """
    try:
        with open(ARCHIVO_USUARIOS, 'w', encoding='utf-8') as f:
            for usuario in usuarios:
                linea_items = [str(item) for item in usuario]
                linea = ";".join(linea_items)
                f.write(linea + "\n")
    except OSError as e:
        print(f"Error al guardar usuarios: {e}")


def crear_usuario():
    """
    (Refactorizado) Usa 'append' para agregar un nuevo usuario.
    """
    # 1. Obtener último ID eficientemente
    id_usuario = _obtener_ultimo_id(ARCHIVO_USUARIOS, id_columna=0) + 1
    
    # 2. Pedir datos
    nombre = input("Nombre del usuario: ")

    email = input("Email del usuario: ")
    while not patron_email.match(email):
        print("Email inválido. Ejemplo válido: usuario@dominio.com")
        email = input("Email del usuario: ")

    telefono = input("Teléfono del usuario (8 a 12 dígitos): ")
    while not patron_telefono.match(telefono):
        print("Teléfono inválido. Solo números (8-12 dígitos).")
        telefono = input("Teléfono del usuario: ")

    edad = Main.ingreso_entero("Edad del usuario: ")

    # 3. Guardar en modo 'append'
    try:
        with open(ARCHIVO_USUARIOS, "a", encoding="utf-8") as f:
            nueva_linea = f"{id_usuario};{nombre};{email};{telefono};{edad}\n"
            f.write(nueva_linea)
        print(f"Usuario {nombre} creado con éxito (ID: {id_usuario})")
    except OSError as e:
        print(f"Error al guardar el nuevo usuario: {e}")

    input("Presione ENTER para continuar.")


def modificar_usuario():
    """
    (Refactorizado) Usa archivo temporal para modificar.
    """
    id_modificar = Main.ingreso_entero("Ingrese el ID del usuario a modificar: ")
    encontrado = False
    
    try:
        with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as arch_orig, open(
            ARCHIVO_TEMP, "w", encoding="utf-8"
        ) as arch_temp:
            
            for linea in arch_orig:
                linea = linea.strip()
                if not linea:
                    continue
                
                try:
                    partes = linea.split(";")
                    id_actual = int(partes[0])

                    if id_actual == id_modificar:
                        encontrado = True
                        print(f"Usuario encontrado: {partes[1]}")
                        
                        nuevo_nombre = input("Nuevo nombre (enter para dejar igual): ")
                        nuevo_email = input("Nuevo email (enter para dejar igual): ")
                        nuevo_telefono = input("Nuevo teléfono (enter para dejar igual): ")
                        # Asumimos que la edad no se modifica
                        
                        nombre_final = nuevo_nombre if nuevo_nombre != "" else partes[1]
                        email_final = nuevo_email if nuevo_email != "" else partes[2]
                        telefono_final = nuevo_telefono if nuevo_telefono != "" else partes[3]
                        
                        nueva_linea = f"{id_actual};{nombre_final};{email_final};{telefono_final};{partes[4]}\n"
                        arch_temp.write(nueva_linea)
                        print("Usuario modificado con éxito.")
                    else:
                        arch_temp.write(linea + "\n")
                
                except (ValueError, IndexError):
                    arch_temp.write(linea + "\n")

    except FileNotFoundError:
        print(f"No se encontró el archivo {ARCHIVO_USUARIOS}.")
    except OSError as e:
        print(f"Error de E/S: {e}")

    # Reemplazar archivo
    if encontrado:
        try:
            os.remove(ARCHIVO_USUARIOS)
            os.rename(ARCHIVO_TEMP, ARCHIVO_USUARIOS)
        except OSError as e:
            print(f"Error al reemplazar el archivo: {e}")
    else:
        print("Usuario no encontrado.")
        os.remove(ARCHIVO_TEMP)
        
    input("Presione ENTER para continuar.")


def borrar_usuario():
    """
    (Refactorizado) Usa archivo temporal para borrar.
    """
    id_borrar = Main.ingreso_entero("Ingrese el ID del usuario a borrar: ")
    encontrado = False
    
    try:
        with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as arch_orig, open(
            ARCHIVO_TEMP, "w", encoding="utf-8"
        ) as arch_temp:
            
            for linea in arch_orig:
                linea = linea.strip()
                if not linea:
                    continue
                
                try:
                    partes = linea.split(";")
                    id_actual = int(partes[0])

                    if id_actual == id_borrar:
                        confirmacion = input(f"¿Seguro que quiere borrar a '{partes[1]}'? (s/n): ").strip().lower()
                        if confirmacion == 's':
                            encontrado = True
                            print(f"Usuario {partes[1]} fue eliminado.")
                            # No escribir la línea en el temporal
                        else:
                            print("Operación cancelada.")
                            arch_temp.write(linea + "\n")
                    else:
                        arch_temp.write(linea + "\n")
                
                except (ValueError, IndexError):
                    arch_temp.write(linea + "\n")

    except FileNotFoundError:
        print(f"No se encontró el archivo {ARCHIVO_USUARIOS}.")
    except OSError as e:
        print(f"Error de E/S: {e}")

    # Reemplazar archivo
    if encontrado:
        try:
            os.remove(ARCHIVO_USUARIOS)
            os.rename(ARCHIVO_TEMP, ARCHIVO_USUARIOS)
        except OSError as e:
            print(f"Error al reemplazar el archivo: {e}")
    else:
        if 'id_actual' in locals() and id_actual != id_borrar:
             print("Usuario no encontrado.")
        os.remove(ARCHIVO_TEMP)
        
    input("Presione ENTER para continuar.")


# --- Funciones de Reportes ---
# Estas funciones SÍ necesitan cargar los datos en memoria para procesarlos.

def usuarios_con_mas_reservas():
    # Esta función necesita leer ambos archivos
    usuarios = leer_usuarios()
    lista_de_reservas = leer_reservas() 
    
    conteo_reservas = {}
    for reserva in lista_de_reservas:
        id_usuario = reserva[0]
        conteo_reservas[id_usuario] = conteo_reservas.get(id_usuario, 0) + 1

    if not conteo_reservas:
        print("No hay reservas registradas.")
        input("Presione ENTER para continuar.")
        return

    max_reservas = max(conteo_reservas.values())
    usuarios_max = set()

    print(f"\nUsuarios con más reservas ({max_reservas} reserva/s):")
    for usuario in usuarios:
        if conteo_reservas.get(usuario[0], 0) == max_reservas:
            usuarios_max.add(usuario[1])

    if not usuarios_max:
        print("No se encontraron usuarios coincidentes.")
    else:
        for nombre in usuarios_max:
            print(f"- {nombre}")
            
    input("Presione ENTER para continuar.")


promedio = lambda lista: sum(lista) / len(lista)


def promedio_edad_por_funcion():
    # Esta función necesita leer los 3 archivos
    usuarios = leer_usuarios()
    lista_de_funciones = leer_funciones()
    lista_de_reservas = leer_reservas()

    if not usuarios:
        print("No hay usuarios registrados para calcular promedios.")
        input("Presione ENTER para continuar.")
        return
        
    print("\n--- Promedio de Edad por Función ---")
    for funcion in lista_de_funciones:
        id_funcion = funcion[0]     
        id_obra_funcion = funcion[1] 
        nombre_funcion = f"Función {id_funcion} (Obra ID: {id_obra_funcion}) - {funcion[2]}"

        edades = []
        
        for reserva in lista_de_reservas:
            id_obra_reserva = reserva[2] 
            
            if id_obra_reserva == id_obra_funcion:    
                id_usuario_reserva = reserva[0]
                
                for usuario in usuarios:
                    if usuario[0] == id_usuario_reserva:
                        edades.append(usuario[4]) 
                        break 
        try:
            prom = promedio(edades)
            print(f"{nombre_funcion}: promedio de edad = {prom:.2f} años (sobre {len(edades)} reservas)")
            
            primeras_edades = edades[:3] 
            print(f"Primeras 3 edades en reservar: {primeras_edades}")

        except ZeroDivisionError:
            print(f"{nombre_funcion}: no hay reservas registradas para esta función.")
            
    input("Presione ENTER para continuar.")


def topTresUsuariosMasJovenes():
    # Esta función SÍ carga todo en memoria a propósito
    usuarios = leer_usuarios()
    
    if not usuarios:
        print("No hay usuarios registrados")
        input("Preseione ENTER para continuar")
        return
    
    usuarios.sort(key=lambda usuario:usuario[4])
    top_3_jovenes = usuarios[:3]

    print("Top 3 usuarios más jovenes")
    Main.mostrar_matriz(top_3_jovenes,("ID Usuario", "Nombre", "Email", "Teléfono", "Edad"))