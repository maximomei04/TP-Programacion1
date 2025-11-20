import os, time


def mostrar_matriz(matriz, encabezados="-" * 20):
    print()
    for titulo in encabezados:
        print(f"{titulo:<25}", end="")
    print()
    for fila in matriz:
        for dato in fila:
            print(f"{dato:<25}", end="")
        print()
    print()
    input("Presione ENTER para continuar")


def limpiar_terminal(segundos=0):
    time.sleep(segundos)
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def ingreso_entero(mensaje="Ingrese un número entero: ", vacio=False):
    """Solamente permite ingresar enteros positivos. Devuelve un int."""
    while True:
        valor_ingresado = input(mensaje).strip()

        if valor_ingresado == "" and vacio is True:
            return ""

        try:
            valor_entero = int(valor_ingresado)

            if valor_entero <= 0:
                raise ValueError

            return valor_entero

        except ValueError:
            print(
                "Error: Ingreso inválido, solamente ingresar numeros enteros positivos"
            )
        except:
            print("Error inesperado")


def ingreso_texto(
    mensaje="Ingrese un texto: ",
    error="Ingreso inválido: No puede quedar vacío. Presione ENTER para reintentar",
    vacio=False,
):
    """Opcionalmente permite ingresar strings vacíos"""
    texto = ""
    while True:
        texto = input(mensaje).strip()
        if texto == "" and vacio is False:
            input(error)
        else:
            break
    return texto


def confirmacion(mensaje="Seguro? [Y/n]: "):
    """Solicita confirmación, devuelve un True o False"""
    respuesta = input(mensaje).strip().lower()
    return respuesta in ("", "s")
