import json
from Main import limpiar_terminal, ingreso_texto, ingreso_entero


def mostrar_obras(archivo, mensaje="Presione ENTER para continuar", tipo=None):
    """Muestra las obras y opcionalmente devuelve un dato"""
    limpiar_terminal()
    try:
        with open(archivo, encoding="UTF-8") as datos:
            lista = json.load(datos)
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

            texto = None
            if tipo == str:
                texto = ingreso_texto(mensaje)
            elif tipo == int:
                texto = ingreso_entero(mensaje)
            elif tipo == None:
                input(mensaje)

            limpiar_terminal()
            return texto

    except (FileNotFoundError, OSError) as error:
        print(f"Error! {error}")


def agregar_obras(archivo):
    limpiar_terminal()
    try:
        with open(archivo, "r", encoding="UTF-8") as datos:
            obras = json.load(datos)

            if len(obras) == 0:  # Si no hay obras crea una obra con el ID 1
                nuevo_id = 1
            else:
                nuevo_id = max(obra["ID"] for obra in obras) + 1

            nombre = ingreso_texto(  # Ingreso Nombre
                "Nombre de la obra: ",
                "Ingreso Inválido: El nombre no puede estar vacío. Presione ENTER para reintentar.",
            ).capitalize()

            precio = ingreso_entero("Precio de la obra: ")  # Ingreso Precio

            categoria = ingreso_texto(  # Ingreso Categoría
                "Categoría de la obra: ",
                "Ingreso Inválido: La Categoría no puede estar vacío. Presione ENTER para reintentar.",
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

            with open(archivo, "w", encoding="UTF-8") as datos:
                json.dump(obras, datos, ensure_ascii=False)
            print(
                f"Obra agregada: | ID: {nuevo_id} | Nombre: {nombre} | Precio: ${precio} | Categoría: {categoria} | Duración: {duracion} min |"
            )
            input("Presione ENTER para continuar.")
            limpiar_terminal()

    except (FileNotFoundError, OSError) as error:
        print(f"Error! {error}")


def lista_IDs(lista_dict):
    IDs = []
    for i in lista_dict:
        IDs.append(i["ID"])
    return IDs


def modificar_obra(archivo):
    try:
        with open(archivo, "r", encoding="UTF-8") as datos:
            obras = json.load(datos)

        if len(obras) == 0:  # Chequear si hay alguna obra
            print("No hay obras para modificar.")
            input("Presione ENTER para continuar.")
            return

        while True:
            id_mod = mostrar_obras(  # Ingreso y busqueda del ID
                "archivos/obras.json", "Ingrese el ID de la obra a modificar: ", int
            )
            if id_mod != "":
                break
        IDs = lista_IDs(obras)
        if id_mod not in IDs:
            input(
                "No se encontró ninguna obra con el ID ingresado.\n\nPresione ENTER para continuar."
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

        with open(archivo, "w", encoding="UTF-8") as datos:
            json.dump(obras, datos, ensure_ascii=False, indent=4)

        print(f"Obra: '{obras[indice]['Nombre']}'")
        print(f"Precio: ${obras[indice]['Precio']}")
        print(f"Categoría: {obras[indice]['Categoria']}")
        print(f"Duración: {obras[indice]['Duracion']} min")
        input("Presione ENTER para continuar.")
        limpiar_terminal()

    except (FileNotFoundError, OSError) as error:
        print(f"Error! {error}")


def borrar_obra(archivo):
    limpiar_terminal()
    try:
        with open(archivo, "r", encoding="UTF-8") as datos:
            obras = json.load(datos)

        if len(obras) == 0:  # Chequear si hay alguna obra
            print("No hay obras para borrar.")
            input("Presione ENTER para continuar.")
            return

        id_borrar = mostrar_obras(  # Ingreso y busqueda del ID
            "archivos/obras.json", "Ingrese el ID de la obra a borrar: ", int
        )
        IDs = lista_IDs(obras)
        if id_borrar not in IDs:
            input(
                "No se encontró ninguna obra con el ID ingresado.\n\nPresione ENTER para continuar."
            )
            return

        indice = IDs.index(id_borrar)
        confirmacion = (
            input(f'¿Seguro que quiere borrar "{obras[indice]["Nombre"]}"? (s/n): ')
            .strip()
            .lower()
        )
        if confirmacion == "s":
            obras.pop(indice)
            print("Obra eliminada.")
        else:
            print("No se eliminó ninguna obra.")

        with open(archivo, "w", encoding="UTF-8") as datos:
            json.dump(obras, datos, ensure_ascii=False, indent=4)
        input("Presione ENTER para continuar.")
        limpiar_terminal()

    except (FileNotFoundError, OSError) as error:
        print(f"Error! {error}")


def estadisticas_precios_obras(archivo):
    limpiar_terminal()
    try:
        with open(archivo, "r", encoding="UTF-8") as datos:
            obras = json.load(datos)

        precios = []
        for obra in obras:
            precios.append(obra["Precio"])

        minimo = minimo_lista(precios)
        promedio = suma_lista(precios) // len(precios)
        maximo = max(precios)
        input(
            f"El precio mínimo es: ${minimo}\nEl precio promedio es: ${promedio}\nEl precio maximo es: ${maximo}\n\nPresione ENTER para continuar"
        )
        limpiar_terminal()

    except (FileNotFoundError, OSError) as error:
        print(f"Error! {error}")


def minimo_lista(lista):
    if len(lista) > 0:
        if len(lista) == 1:
            return lista[0]
        elif lista[0] <= minimo_lista(lista[1:]):
            return lista[0]
        else:
            return minimo_lista(lista[1:])


def suma_lista(lista):
    if len(lista) == 0:
        return 0
    else:
        return lista[0] + suma_lista(lista[1:])
