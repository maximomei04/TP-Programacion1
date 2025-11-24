import json

from utilidades import *
from funciones import *


def cargar_json(ruta):
    try:
        with open(ruta, "r", encoding="UTF-8") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, OSError) as error:
        print(f"Error: {error}")
    except Exception as e:
        print(f"Error: {e}")


def modificar_json(ruta, cambios):
    try:
        with open(ruta, "w", encoding="UTF-8") as archivo:
            json.dump(cambios, archivo, ensure_ascii=False, indent=4)
    except (FileNotFoundError, OSError) as error:
        print(f"Error: {error}")
    except Exception as e:
        print(f"Error: {e}")


def mostrar_obras(ruta, mensaje="Presione ENTER para continuar", tipo=None):
    """Muestra las obras y opcionalmente devuelve un entero o cadena"""
    lista = cargar_json(ruta)
    limpiar_terminal()

    if not lista:
        input("No hay obras a mostrar. Presione ENTER para continuar")
        return

    print()
    titulo = "OBRAS"
    print(titulo.center(150, "-"))

    print(  # Cabecera manual
        f"{'ID':<5} | {'Nombre':<30} | {'Precio':<10} | {'Categoría':<30} | {'Duración':<10}"
    )
    print(f'\n{"-" * 150}')

    for diccionario in lista:
        print(f"{diccionario['ID']:<5}", end=" | ")
        print(f"{diccionario['Nombre']:<30}", end=" | ")
        print(f"${diccionario['Precio']:<9}", end=" | ")
        print(f"{cat_mostrar:<30}", end=" | ")
        print(f"{diccionario['Duracion']} min")
    print()

    texto = ""  # Ingreso de dato opcional
    if tipo is None:
        input(mensaje)
        limpiar_terminal()
        return None
    elif tipo == str:
        texto = ingreso_texto(mensaje)
    elif tipo == int:
        texto = ingreso_entero(mensaje)
    else:
        print("Error: Tipo de dato no soportado")

    limpiar_terminal()
    return texto


def agregar_obras(ruta):
    obras = cargar_json(ruta)
    limpiar_terminal()

    if not obras:
        nuevo_id = 1
    else:
        nuevo_id = max(obra["ID"] for obra in obras) + 1

    nombre = ingreso_texto("Nombre de la obra: ").capitalize()
    precio = ingreso_entero("Precio de la obra: ")
    categoria = ingreso_texto("Categoría de la obra: ").capitalize()
    duracion = ingreso_entero("Ingrese la Duración de la obra (minutos): ")

    nueva_obra = {
        "ID": nuevo_id,
        "Nombre": nombre,
        "Precio": precio,
        "Categoria": categoria,
        "Duracion": duracion,
    }
    obras.append(nueva_obra)

    modificar_json(ruta, obras)

    print(
        "\nObra agregada:\n"
        f"  - ID: {nuevo_id}\n"
        f"  - Nombre: {nombre}\n"
        f"  - Precio: ${precio}\n"
        f"  - Categoría: {categoria}\n"
        f"  - Duración: {duracion} min\n"
    )
    input("Presione ENTER para continuar.")
    limpiar_terminal()


def lista_IDs(lista_dict):
    IDs = []
    for i in lista_dict:
        IDs.append(i["ID"])
    return IDs


def modificar_campo(obras, indice, campo, mensaje, funcion_ingreso):
    valor_actual = obras[indice][campo]
    nuevo_valor = funcion_ingreso(mensaje + f"{valor_actual}'): ", vacio=True)
    if nuevo_valor == "":
        print(f"Se mantiene: {obras[indice][campo]}")
    else:
        obras[indice][campo] = nuevo_valor


def modificar_obra(ruta):
    obras = cargar_json(ruta)
    limpiar_terminal()

    if not obras:
        input("No hay obras para modificar. Presione ENTER para continuar.")
        return

    while True:
        id_mod = mostrar_obras(
            "archivos/obras.json", "Ingrese el ID de la obra a modificar: ", int
        )
        if id_mod != "":
            break

    IDs = lista_IDs(obras)

    if id_mod not in IDs:
        input(
            "No se encontró ninguna obra con el ID ingresado.\nPresione ENTER para continuar."
        )
        return

    indice = IDs.index(id_mod)
    modificar_campo(
        obras, indice, "Nombre", "Nuevo Nombre (ENTER para dejar '", ingreso_texto
    )
    modificar_campo(
        obras, indice, "Precio", "Nuevo Precio (ENTER para dejar '", ingreso_texto
    )
    modificar_campo(
        obras, indice, "Categoria", "Nueva Categoria (ENTER para dejar '", ingreso_texto
    )
    modificar_campo(
        obras, indice, "Duracion", "Nueva Duracion (ENTER para dejar '", ingreso_texto
    )

    modificar_json(ruta, obras)
    mostrar_obras("archivos/obras.json")
    limpiar_terminal()


def borrar_obra(ruta):
    obras = cargar_json(ruta)
    limpiar_terminal()

    if not obras:
        input("No hay obras para borrar. Presione ENTER para continuar.")
        return

    id_borrar = mostrar_obras(
        "archivos/obras.json", "Ingrese el ID de la obra a borrar: ", int
    )
    IDs = lista_IDs(obras)

    if id_borrar not in IDs:
        input(
            "No se encontró ninguna obra con el ID ingresado.\nPresione ENTER para continuar."
        )
        return

    indice = IDs.index(id_borrar)

    if confirmacion(
        f'¿Seguro que quiere borrar "{obras[indice]["Nombre"]}" y sus FUNCIONES asociadas? (S/n): '
    ):
        obras.pop(indice)
        modificar_json(ruta, obras)

        # Eliminar Funciones Asociadas a la Obra a Eliminar
        eliminar_funciones_por_obra(id_borrar)

        print("Obra y sus funciones asociadas eliminadas.")
    else:
        print("No se eliminó ninguna obra.")

    input("Presione ENTER para continuar.")
    limpiar_terminal()


def estadisticas_precios_obras(ruta):
    obras = cargar_json(ruta)
    limpiar_terminal()

    if not obras:
        input("No hay obras existentes. Presione ENTER para continuar")
        return

    # Lista por comprensión para extraer precios
    precios = [obra["Precio"] for obra in obras]

    minimo = minimo_lista(precios)
    promedio_val = suma_lista(precios) // len(precios)
    maximo = max(precios)

    input(
        f"Precio Mínimo: ${minimo}\n"
        f"Precio Promedio: ${promedio_val}\n"
        f"Precio Máximo: ${maximo}\n"
        "\nPresione ENTER para continuar"
    )
    limpiar_terminal()


def minimo_lista(lista):
    try:
        if len(lista) > 0:
            if len(lista) == 1:
                return lista[0]
            elif lista[0] <= minimo_lista(lista[1:]):
                return lista[0]
            else:
                return minimo_lista(lista[1:])
    except Exception as e:
        print(f"Error: {e}")


def suma_lista(lista):
    try:
        if len(lista) == 0:
            return 0
        else:
            return lista[0] + suma_lista(lista[1:])
    except Exception as e:
        print(f"Error: {e}")
