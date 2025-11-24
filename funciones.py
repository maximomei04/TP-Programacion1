import re, os
import json
from functools import reduce
from datetime import datetime

from utilidades import *

ARCHIVO_FUNCIONES = "archivos/funciones.txt"
ARCHIVO_TEMP = "archivos/funciones_temp.txt"


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


def _procesar_linea_recursiva(archivo, lista_funciones):
    linea = archivo.readline()
    if not linea:
        return

    linea = linea.strip()
    if linea:
        try:
            partes = linea.split(";")
            funcion = [int(partes[0]), int(partes[1]), partes[2]]
            lista_funciones.append(funcion)
        except (ValueError, IndexError):
            print(
                f"Advertencia: Se omitió una línea mal formada en {ARCHIVO_FUNCIONES}"
            )

    _procesar_linea_recursiva(archivo, lista_funciones)


def leer_funciones():
    funciones = []
    try:
        with open(ARCHIVO_FUNCIONES, "r", encoding="utf-8") as f:
            _procesar_linea_recursiva(f, funciones)
    except FileNotFoundError:
        print(
            f"Nota: No se encontró {ARCHIVO_FUNCIONES}, se creará uno nuevo al guardar."
        )
    return funciones


def guardar_funciones(funciones):
    try:
        with open(ARCHIVO_FUNCIONES, "w", encoding="utf-8") as f:
            for funcion in funciones:
                linea_items = [str(item) for item in funcion]
                linea = ";".join(linea_items)
                f.write(linea + "\n")
    except OSError as e:
        print(f"Error fatal al guardar funciones: {e}")


# NUEVO: Función para eliminar en cascada desde obras
def eliminar_funciones_por_obra(id_obra_borrar):
    funciones = leer_funciones()
    # Usamos Filter lambda para conservar solo las que NO son de esa obra
    funciones_conservadas = list(filter(lambda f: f[1] != id_obra_borrar, funciones))

    if len(funciones) != len(funciones_conservadas):
        guardar_funciones(funciones_conservadas)


# NUEVO: Mostrar funciones con el nombre de la obra
def mostrar_funciones_con_nombres():
    lista_funciones = leer_funciones()
    if not lista_funciones:
        print("No hay funciones cargadas.")
        input("Presione ENTER.")
        return

    # Leemos obras manualmente para evitar import circular con obras.py
    try:
        with open("archivos/obras.json", "r", encoding="UTF-8") as f:
            lista_obras = json.load(f)
    except:
        lista_obras = []

    # Creamos un diccionario ID->Nombre para acceso rápido
    mapa_obras = {o["ID"]: o["Nombre"] for o in lista_obras}

    # Construimos matriz visual
    matriz_visual = []
    for f in lista_funciones:
        nombre_obra = mapa_obras.get(f[1], "Obra Eliminada")
        # ID Func, ID Obra, Nombre Obra, Fecha
        matriz_visual.append([f[0], f[1], nombre_obra, f[2]])

    mostrar_matriz(matriz_visual, ("ID Func", "ID Obra", "Nombre Obra", "Fecha"))


def crear_funcion():
    ultimo_id = _obtener_ultimo_id(ARCHIVO_FUNCIONES, id_columna=0)
    id_funcion = ultimo_id + 1

    # Mostrar obras disponibles (lectura directa para evitar import)
    try:
        with open("archivos/obras.json", "r", encoding="UTF-8") as f:
            obs = json.load(f)
            print("\n--- Obras Disponibles ---")
            for o in obs:
                print(f"ID: {o['ID']} | {o['Nombre']}")
            print("-------------------------")
    except:
        pass

    id_obra = ingreso_entero("Ingrese el ID de la obra: ")

    fecha_valida = False
    fecha = ""
    while fecha_valida == False:
        fecha = input("Ingrese la fecha (YYYY-MM-DD): ").strip()
        if re.match(r"^\d{4}-\d{2}-\d{2}$", fecha):
            # Slicing de Cadenas
            mes = int(fecha[5:7])
            dia = int(fecha[8:])
            if (1 <= mes <= 12) and (1 <= dia <= 31):
                fecha_valida = True
            else:
                print("Mes o Día Inválido")
        else:
            print("Formato inválido. Use YYYY-MM-DD (ejemplo: 2025-09-18).")

    try:
        with open(ARCHIVO_FUNCIONES, "a", encoding="utf-8") as f:
            nueva_linea = f"{id_funcion};{id_obra};{fecha}\n"
            f.write(nueva_linea)
        print(f"Función creada con éxito (ID: {id_funcion}).")
    except OSError as e:
        print(f"Error al guardar la nueva función: {e}")

    input("Presione ENTER para continuar.")


def modificar_funcion():
    mostrar_funciones_con_nombres()  # Usamos la nueva visualización
    id_modificar = ingreso_entero("Ingrese el ID de la funcion a modificar: ")
    encontrada = False

    try:
        with open(ARCHIVO_FUNCIONES, "r", encoding="utf-8") as arch_orig, open(
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
                        encontrada = True
                        print(
                            f"Función encontrada: Obra {partes[1]}, Fecha {partes[2]}"
                        )
                        nuevaFecha = input(
                            "Ingrese la fecha nueva (enter para dejar igual): "
                        ).strip()
                        nuevaObra = input(
                            "Ingrese nuevo ID de obra (enter para dejar igual): "
                        ).strip()

                        fecha_final = nuevaFecha if nuevaFecha != "" else partes[2]
                        obra_final = partes[1]

                        if nuevaObra != "":
                            try:
                                obra_final = int(nuevaObra)
                            except ValueError:
                                print(
                                    "ID de obra inválido, se mantendrá el ID original."
                                )
                                obra_final = partes[1]

                        arch_temp.write(f"{id_actual};{obra_final};{fecha_final}\n")
                        print("Función modificada con éxito.")
                    else:
                        arch_temp.write(linea + "\n")

                except (ValueError, IndexError):
                    arch_temp.write(linea + "\n")

    except FileNotFoundError:
        print(f"No se encontró el archivo {ARCHIVO_FUNCIONES}.")
        return
    except OSError as e:
        print(f"Error de E/S: {e}")
        return

    if encontrada:
        try:
            os.remove(ARCHIVO_FUNCIONES)
            os.rename(ARCHIVO_TEMP, ARCHIVO_FUNCIONES)
        except OSError as e:
            print(f"Error al reemplazar el archivo: {e}")
    else:
        print("Función no encontrada.")
        os.remove(ARCHIVO_TEMP)

    input("Presione ENTER para continuar.")


def borrar_funcion():
    mostrar_funciones_con_nombres()
    id_borrar = ingreso_entero("Ingrese el ID de la funcion a borrar: ")
    encontrado = False

    try:
        with open(ARCHIVO_FUNCIONES, "r", encoding="utf-8") as arch_orig, open(
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
                        if confirmacion(
                            f"¿Seguro que quiere borrar la función {partes[0]}? (s/n): "
                        ):
                            encontrado = True
                            print(f"La funcion {id_actual} fue eliminada.")
                        else:
                            arch_temp.write(linea + "\n")
                    else:
                        arch_temp.write(linea + "\n")

                except (ValueError, IndexError):
                    arch_temp.write(linea + "\n")

    except FileNotFoundError:
        print(f"No se encontró el archivo {ARCHIVO_FUNCIONES}.")
        return
    except OSError as e:
        print(f"Error de E/S: {e}")
        return

    if encontrado:
        try:
            os.remove(ARCHIVO_FUNCIONES)
            os.rename(ARCHIVO_TEMP, ARCHIVO_FUNCIONES)
        except OSError as e:
            print(f"Error al reemplazar el archivo: {e}")
    else:
        print("No se borró nada.")
        os.remove(ARCHIVO_TEMP)

    input("Presione ENTER para continuar.")


# --- LAMBDAS ORIGINALES (MANTENIDAS) ---
def encontrar_funciones_por_obra(id_obra_buscada, funciones):
    funciones_filtradas = list(filter(lambda f: f[1] == id_obra_buscada, funciones))
    print(
        f"\n--- Funciones encontradas para la Obra ID {id_obra_buscada} (usando FILTER) ---"
    )
    if not funciones_filtradas:
        print("No se encontraron funciones para esa obra.")
    else:
        mostrar_matriz(funciones_filtradas, ("ID Función", "ID Obra", "Fecha"))
    return funciones_filtradas


def obtener_fechas_como_objetos(lista_funciones):
    print(f"\n--- Fechas convertidas a objetos datetime (usando MAP) ---")
    if not lista_funciones:
        print("No hay fechas para convertir.")
        return
    try:
        fechas_objetos = list(
            map(lambda f: datetime.strptime(f[2], "%Y-%m-%d"), lista_funciones)
        )
        for fecha in fechas_objetos:
            print(f"Día: {fecha.day}, Mes: {fecha.month}, Año: {fecha.year}")
    except ValueError as e:
        print(
            f"Error al convertir fechas: {e}. Asegúrese que el formato sea YYYY-MM-DD."
        )


def encontrar_ultima_funcion(funciones):
    if not funciones:
        print("\nNo hay funciones para comparar.")
        return
    ultima = reduce(lambda f1, f2: f1 if f1[2] > f2[2] else f2, funciones)
    print(f"\n--- Última función programada (usando REDUCE) ---")
    print(f"ID Función: {ultima[0]}, Obra: {ultima[1]}, Fecha: {ultima[2]}")


def reportes_con_lambdas():
    funciones = leer_funciones()
    print("=============================================")
    print(" EJECUTANDO REPORTES CON FUNCIONES LAMBDA ")
    print("=============================================")
    id_obra = ingreso_entero("Ingrese ID de obra para FILTRAR (ej: 1): ")
    funciones_filtradas = encontrar_funciones_por_obra(id_obra, funciones)
    obtener_fechas_como_objetos(funciones_filtradas)
    encontrar_ultima_funcion(funciones)
    input("\nPresione ENTER para continuar.")
