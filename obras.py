import json

from utilidades import *


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
    for clave in lista[0].keys():
        if clave == "Duracion":
            print(f"{clave}", end="")
        else:
            print(f"{clave:<30}", end=" | ")
    print(f'\n{"-" * 150}')
    for diccionario in lista:
        for dato in diccionario:
            if dato == "Precio":
                print(f"${diccionario[dato]:<29}", end=" | ")
            elif dato == "Duracion":
                print(f"{diccionario[dato]} min", end="")
            else:
                print(f"{diccionario[dato]:<30}", end=" | ")
        print()
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

    if not obras:  # Si no hay obras crea una obra con el ID 1
        nuevo_id = 1
    else:
        nuevo_id = max(obra["ID"] for obra in obras) + 1

    nombre = ingreso_texto(  # Ingreso Nombre
        "Nombre de la obra: ",
        "Ingreso Inválido: El nombre no puede estar vacío.\nPresione ENTER para reintentar.",
    ).capitalize()

    precio = ingreso_entero("Precio de la obra: ")  # Ingreso Precio

    categoria = ingreso_texto(  # Ingreso Categoría
        "Categoría de la obra: ",
        "Ingreso Inválido: La Categoría no puede estar vacío.\nPresione ENTER para reintentar.",
    ).capitalize()

    duracion = ingreso_entero(
        "Ingrese la Duración de la obra (minutos): "
    )  # Ingreso Duración

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
    """Crea una lista de enteros desde una lista de diccionarios"""
    IDs = []
    for i in lista_dict:
        IDs.append(i["ID"])
    return IDs


# def cambiar_mantener(dato_cambiar, mensaje):

#     return


def modificar_obra(ruta):
    obras = cargar_json(ruta)
    limpiar_terminal()

    if not obras:  # Chequear si hay alguna obra
        input("No hay obras para modificar. Presione ENTER para continuar.")
        return

    while True:  # Ingreso y busqueda del ID
        id_mod = mostrar_obras(
            "archivos/obras.json", "Ingrese el ID de la obra a modificar: ", int
        )
        if id_mod != "":
            break
    IDs = lista_IDs(obras)
    if id_mod not in IDs:
        input(
            "No se encontró ninguna obra con el ID ingresado.\n"
            "Presione ENTER para continuar."
        )
        return
    indice = IDs.index(id_mod)

    nuevo_nombre = ingreso_texto(  # Nombre
        f"Nuevo Nombre (ENTER para dejar '{obras[indice]['Nombre']}'): ", vacio=True
    )
    if nuevo_nombre == "":
        print("Se mantiene el Nombre actual")
    else:
        obras[indice]["Nombre"] = nuevo_nombre

    nuevo_precio = ingreso_entero(  # Precio
        f"Desea modificar el Precio? (ENTER para dejar ${obras[indice]['Precio']}): "
    )
    if nuevo_precio == "":
        print("Se mantiene el Precio actual.")
    else:
        obras[indice]["Precio"] = nuevo_precio

    nueva_categoria = ingreso_texto(  # Categoria
        f"Nueva Categoría (ENTER para dejar '{obras[indice]['Categoria']}'): ",
        vacio=True,
    )
    if nueva_categoria == "":
        print("Se mantiene la Categoria actual")
    else:
        obras[indice]["Categoria"] = nueva_categoria

    nueva_duracion = ingreso_entero(  # Duracion
        f"Desea modificar la Duracion? (ENTER para dejar ${obras[indice]['Duracion']}): "
    )
    if nueva_duracion == "":
        print("Se mantiene la Duracion actual.")
    else:
        obras[indice]["Duracion"] = nueva_duracion

    modificar_json(ruta, obras)

    print(
        f"Obra: '{obras[indice]['Nombre']}'"
        f"Precio: ${obras[indice]['Precio']}"
        f"Categoría: {obras[indice]['Categoria']}"
        f"Duración: {obras[indice]['Duracion']} min"
    )
    mostrar_obras("archivos/obras.json")
    limpiar_terminal()


def borrar_obra(ruta):
    obras = cargar_json(ruta)
    limpiar_terminal()

    if not obras:  # Chequear si hay alguna obra
        input("No hay obras para borrar. Presione ENTER para continuar.")
        return

    id_borrar = mostrar_obras(  # Ingreso y busqueda del ID
        "archivos/obras.json", "Ingrese el ID de la obra a borrar: ", int
    )
    IDs = lista_IDs(obras)
    if id_borrar not in IDs:
        input(
            "No se encontró ninguna obra con el ID ingresado.\n"
            "Presione ENTER para continuar."
        )
        return

    indice = IDs.index(id_borrar)

    if confirmacion(f'¿Seguro que quiere borrar "{obras[indice]["Nombre"]}"? (S/n): '):
        obras.pop(indice)
        print("Obra eliminada.")
    else:
        print("No se eliminó ninguna obra.")

    modificar_json(ruta, obras)

    input("Presione ENTER para continuar.")
    limpiar_terminal()


def estadisticas_precios_obras(ruta):
    obras = cargar_json(ruta)
    limpiar_terminal()

    if not obras:
        input("No hay obras existentes. Presione ENTER para continuar")
        return

    precios = []
    for obra in obras:
        precios.append(obra["Precio"])

    minimo = minimo_lista(precios)
    promedio = suma_lista(precios) // len(precios)
    maximo = max(precios)
    input(
        f"Precio Mínimo: ${minimo}\n"
        f"Precio Promedio: ${promedio}\n"
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
