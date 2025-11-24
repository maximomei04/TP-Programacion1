import os, time


def mostrar_matriz(matriz, encabezados):
    print()
    for titulo in encabezados:
        print(f"{titulo:<30}", end="")
    print()
    print("-" * (30 * len(encabezados)))
    for fila in matriz:
        for dato in fila:
            print(f"{str(dato):<30}", end="")
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


def ingreso_texto(mensaje="Ingrese un texto: ", vacio=False):
    while True:
        texto = input(mensaje).strip()
        if texto == "" and vacio is False:
            print("No puede estar vacío.")
        else:
            return texto


def confirmacion(mensaje="Seguro? [Y/n]: "):
    respuesta = input(mensaje).strip().lower()
    return respuesta in ("", "s")
