import re, os
import json

# Importaciones locales se harán dentro de funciones donde haga falta para evitar circularidad
from utilidades import *

# Importamos funciones y reservas solo para lectura si es necesario, pero cuidado con circulares
# Mejor leer archivos raw o import local

ARCHIVO_USUARIOS = "archivos/usuarios.txt"
ARCHIVO_TEMP = "archivos/usuarios_temp.txt"

patron_email = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
patron_telefono = re.compile(r"^\d{8,12}$")


def _obtener_ultimo_id(archivo, id_columna=0):
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
                        continue
    except FileNotFoundError:
        pass
    return ultimo_id


def leer_usuarios():
    usuarios = []
    try:
        with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea:
                    try:
                        partes = linea.split(";")
                        usuario = [
                            int(partes[0]),
                            partes[1],
                            partes[2],
                            partes[3],
                            int(partes[4]),
                        ]
                        usuarios.append(usuario)
                    except (ValueError, IndexError):
                        pass
    except FileNotFoundError:
        pass
    return usuarios


def crear_usuario():
    id_usuario = _obtener_ultimo_id(ARCHIVO_USUARIOS, id_columna=0) + 1
    nombre = input("Nombre del usuario: ")

    email = input("Email del usuario: ")
    while not patron_email.match(email):
        print("Email inválido.")
        email = input("Email del usuario: ")

    telefono = input("Teléfono (8-12 digitos): ")
    while not patron_telefono.match(telefono):
        print("Teléfono inválido.")
        telefono = input("Teléfono: ")

    edad = ingreso_entero("Edad del usuario: ")

    try:
        with open(ARCHIVO_USUARIOS, "a", encoding="utf-8") as f:
            nueva_linea = f"{id_usuario};{nombre};{email};{telefono};{edad}\n"
            f.write(nueva_linea)
        print(f"Usuario {nombre} creado (ID: {id_usuario})")
    except OSError as e:
        print(f"Error: {e}")
    input("Presione ENTER.")


def modificar_usuario():
    # (Código original mantenido resumido por espacio, funcionalmente igual)
    id_mod = ingreso_entero("ID usuario a modificar: ")
    encontrado = False
    try:
        with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as orig, open(
            ARCHIVO_TEMP, "w", encoding="utf-8"
        ) as temp:
            for linea in orig:
                if not linea.strip():
                    continue
                p = linea.strip().split(";")
                if int(p[0]) == id_mod:
                    encontrado = True
                    print(f"Usuario: {p[1]}")
                    nn = input("Nuevo nombre: ")
                    nm = input("Nuevo mail: ")
                    nt = input("Nuevo tel: ")

                    nf = nn if nn else p[1]
                    mf = nm if nm else p[2]
                    tf = nt if nt else p[3]
                    temp.write(f"{id_mod};{nf};{mf};{tf};{p[4]}\n")
                else:
                    temp.write(linea)
    except:
        pass

    if encontrado:
        os.remove(ARCHIVO_USUARIOS)
        os.rename(ARCHIVO_TEMP, ARCHIVO_USUARIOS)
        print("Modificado.")
    else:
        os.remove(ARCHIVO_TEMP)
        print("No encontrado.")
    input("ENTER.")


def borrar_usuario():
    id_borrar = ingreso_entero("ID borrar: ")
    encontrado = False
    try:
        with open(ARCHIVO_USUARIOS, "r", encoding="utf-8") as orig, open(
            ARCHIVO_TEMP, "w", encoding="utf-8"
        ) as temp:
            for linea in orig:
                if not linea.strip():
                    continue
                p = linea.strip().split(";")
                if int(p[0]) == id_borrar:
                    if input("Seguro? (s/n): ") == "s":
                        encontrado = True
                    else:
                        temp.write(linea)
                else:
                    temp.write(linea)
    except:
        pass

    if encontrado:
        os.remove(ARCHIVO_USUARIOS)
        os.rename(ARCHIVO_TEMP, ARCHIVO_USUARIOS)
        print("Borrado.")
    else:
        os.remove(ARCHIVO_TEMP)
    input("ENTER.")


# --- REPORTES CON CONJUNTOS (MANTENIDOS) ---
def usuarios_con_mas_reservas():
    # Import local para romper ciclo
    from reservas import leer_reservas

    usuarios = leer_usuarios()
    reservas = leer_reservas()

    conteo = {}
    for r in reservas:
        uid = r[0]
        conteo[uid] = conteo.get(uid, 0) + 1

    if not conteo:
        print("Sin reservas.")
        input("ENTER.")
        return

    max_res = max(conteo.values())
    # CONJUNTO
    usuarios_max = set()

    for u in usuarios:
        if conteo.get(u[0], 0) == max_res:
            usuarios_max.add(u[1])

    print(f"Usuarios con más reservas ({max_res}):")
    for n in usuarios_max:
        print(f"- {n}")
    input("ENTER.")


promedio = lambda lista: sum(lista) / len(lista) if len(lista) > 0 else 0


def promedio_edad_por_funcion():
    # Imports locales
    from reservas import leer_reservas
    from funciones import leer_funciones

    us = leer_usuarios()
    fs = leer_funciones()
    rs = leer_reservas()

    print("\n--- Promedio edad por función ---")
    for f in fs:
        id_f, id_obra_f = f[0], f[1]
        # Filtramos reservas para esa obra (asumiendo logica original del TP)
        # NOTA: La logica original ligaba usuario->reserva->obra, no directamente a función específica fecha.
        # Mantengo la logica original.

        edades = []
        for r in rs:
            if r[2] == id_obra_f:  # Misma obra
                uid = r[0]
                for u in us:
                    if u[0] == uid:
                        edades.append(u[4])
                        break

        if edades:
            print(
                f"Func {id_f} (Obra {id_obra_f}): Promedio {promedio(edades):.1f} años."
            )
        else:
            print(f"Func {id_f}: Sin datos.")
    input("ENTER.")


def topTresUsuariosMasJovenes():
    us = leer_usuarios()
    if not us:
        return
    us.sort(key=lambda u: u[4])
    print("Top 3 Jóvenes:")
    mostrar_matriz(us[:3], ("ID", "Nombre", "Email", "Tel", "Edad"))


# -----------------------------------------------------------------------
# NUEVO: REPORTE CRUZADO (CONSULTA CRUZADA)
# -----------------------------------------------------------------------
def reporte_cruzado_usuarios_obras():
    """
    Muestra qué usuarios han reservado qué obras y viceversa.
    Usa Listas por Comprensión.
    """
    from reservas import leer_reservas

    limpiar_terminal()
    print("=========================================")
    print("   REPORTE CRUZADO: USUARIOS <-> OBRAS   ")
    print("=========================================")

    users = leer_usuarios()
    res = leer_reservas()

    # Cargamos obras a mano para diccionarios
    try:
        with open("archivos/obras.json", "r", encoding="utf-8") as f:
            obras_data = json.load(f)
    except:
        obras_data = []

    # Diccionario por comprensión: {id_obra: nombre_obra}
    dict_obras = {o["ID"]: o["Nombre"] for o in obras_data}

    if not users:
        print("No hay usuarios.")
        input("ENTER.")
        return

    for u in users:
        u_id = u[0]
        u_nom = u[1]

        # NUEVO: Lista por comprensión con lógica cruzada
        # Obtenemos los nombres de las obras que este usuario reservó
        obras_reservadas = [
            dict_obras.get(r[2], "Desconocida") for r in res if r[0] == u_id
        ]

        # Usamos set para quitar duplicados si vio la misma obra 2 veces
        obras_unicas = set(obras_reservadas)

        if obras_unicas:
            print(f"[Usuario] {u_nom} (ID: {u_id}) vió:")
            for obra in obras_unicas:
                print(f"   -> {obra}")
        else:
            print(f"[Usuario] {u_nom} (ID: {u_id}) no tiene reservas.")

    print("\n-----------------------------------------")
    input("Presione ENTER para volver.")
