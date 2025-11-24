from obras import *
from funciones import *
from reservas import *
from usuarios import *
from utilidades import *
import time

# ----------------------------------------------------------------------------------------------
# NUEVO: LOGIN
# ----------------------------------------------------------------------------------------------
def login():
    limpiar_terminal()
    print("========================================")
    print("      SISTEMA DE GESTIÓN DE TEATRO      ")
    print("========================================")
    
    intentos = 3
    while intentos > 0:
        user = input("Usuario: ").strip()
        password = input("Contraseña: ").strip()

        # Credenciales hardcodeadas
        if user == "admin" and password == "1234":
            print("\n¡Bienvenido al sistema!")
            time.sleep(1)
            return True
        else:
            intentos -= 1
            print(f"Credenciales incorrectas. Intentos restantes: {intentos}")
    
    print("Se han agotado los intentos. Cerrando sistema.")
    return False

# ----------------------------------------------------------------------------------------------
# CUERPO PRINCIPAL
# ----------------------------------------------------------------------------------------------
def main():
    # Ejecutar Login antes de iniciar
    if not login():
        return

    # -------------------------------------------------
    # Inicialización de variables
    # -------------------------------------------------
    limpiar_terminal()
    

    # -------------------------------------------------
    # Bloque de menú
    # -------------------------------------------------
    while True:
        while True:
            opciones = 4
            print()
            print("-" * 20)
            print("MENÚ PRINCIPAL")
            print("-" * 20)
            print("[1] Gestión de Obras")
            print("[2] Gestión de Funciones")
            print("[3] Gestión de Reservas")
            print("[4] Gestión de Usuarios")
            print("-" * 20)
            print("[0] Salir del programa")
            print("-" * 20)
            print()

            opcion = input("Seleccione una opción: ")
            if opcion in [str(i) for i in range(0, opciones + 1)]:
                break
            else:
                input("Opción inválida. Presione ENTER para volver a seleccionar.")
        print()

        if opcion == "0":
            print("Gracias por usar el sistema")
            limpiar_terminal(2)
            exit()

        elif opcion == "1":  # MENÚ OBRAS
            limpiar_terminal()
            while True:
                while True:
                    opciones = 5
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > MENÚ OBRAS")
                    print("---------------------------")
                    print("[1] Mostrar obras")
                    print("[2] Agregar obra")
                    print("[3] Modificar obra")
                    print("[4] Eliminar obra (Borra funciones asociadas)")
                    print("[5] Estadistica precios")
                    print("---------------------------")
                    print("[0] Volver al menú anterior")
                    print("---------------------------")
                    print()

                    opcion = input("Seleccione una opción: ")
                    if opcion in [str(i) for i in range(0, opciones + 1)]:
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if opcion == "0":
                    limpiar_terminal()
                    break

                elif opcion == "1":
                    mostrar_obras("archivos/obras.json")
                elif opcion == "2":
                    agregar_obras("archivos/obras.json")
                elif opcion == "3":
                    modificar_obra("archivos/obras.json")
                elif opcion == "4":
                    borrar_obra("archivos/obras.json")
                elif opcion == "5":
                    estadisticas_precios_obras("archivos/obras.json")

        elif opcion == "2":  # MENÚ FUNCIONES
            limpiar_terminal()
            while True:
                while True:
                    opciones = 5
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > MENÚ FUNCIONES")
                    print("---------------------------")
                    print("[1] Mostrar funciones")
                    print("[2] Agregar función")
                    print("[3] Modificar función")
                    print("[4] Borrar función")
                    print("[5] Reportes con Lambdas (map, filter, reduce)")
                    print("---------------------------")
                    print("[0] Volver al menú anterior")
                    print("---------------------------")
                    print()

                    opcion = input("Seleccione una opción: ")
                    if opcion in [str(i) for i in range(0, opciones + 1)]:
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if opcion == "0":
                    break
                elif opcion == "1":
                    # NUEVO: Llamamos a la función que muestra nombres de obras
                    mostrar_funciones_con_nombres()
                elif opcion == "2":
                    crear_funcion()
                elif opcion == "3":
                    modificar_funcion()
                elif opcion == "4":
                    borrar_funcion()
                elif opcion == "5":
                    reportes_con_lambdas()

        elif opcion == "3":  # MENÚ RESERVAS
            limpiar_terminal()
            while True:
                while True:
                    opciones = 4
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > MENÚ RESERVAS")
                    print("---------------------------")
                    print("[1] Mostrar reservas")
                    print("[2] Agregar reserva")
                    print("[3] Modificar reserva")
                    print("[4] Borrar reserva")
                    print("---------------------------")
                    print("[0] Volver al menú anterior")
                    print("---------------------------")
                    print()

                    opcion = input("Seleccione una opción: ")
                    if opcion in [str(i) for i in range(0, opciones + 1)]:
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if opcion == "0":
                    break
                elif opcion == "1":
                    lista_de_reservas = leer_reservas()
                    mostrar_reservas(lista_de_reservas)
                elif opcion == "2":
                    crear_reserva()
                elif opcion == "3":
                    modificar_reserva()
                elif opcion == "4":
                    borrar_reserva()

        elif opcion == "4":  # MENÚ USUARIOS
            limpiar_terminal()
            while True:
                while True:
                    opciones = 8
                    print()
                    print("---------------------------")
                    print("MENÚ PRINCIPAL > MENÚ USUARIOS")
                    print("---------------------------")
                    print("[1] Mostrar Usuarios")
                    print("[2] Agregar Usuario")
                    print("[3] Modificar Usuario")
                    print("[4] Borrar Usuario")
                    print("[5] Mostrar promedio de edad de Usuarios en la funcion")
                    print("[6] Usuarios con mas Reservas")
                    print("[7] Top tres usuarios mas jovenes")
                    print("[8] Reporte Cruzado (Usuarios y sus Obras)") # NUEVO
                    print("---------------------------")
                    print("[0] Volver al menú anterior")
                    print("---------------------------")
                    print()

                    opcion = input("Seleccione una opción: ")
                    if opcion in [str(i) for i in range(0, opciones + 1)]:
                        break
                    else:
                        input("Opción inválida. Presione ENTER para volver a seleccionar.")
                print()

                if opcion == "0":
                    break
                elif opcion == "1":
                    lista_de_usuarios = leer_usuarios()
                    mostrar_matriz(lista_de_usuarios, ("ID Usuario", "Nombre", "Email", "Teléfono", "Edad"))
                elif opcion == "2":
                    crear_usuario()
                elif opcion == "3":
                    modificar_usuario()
                elif opcion == "4":
                    borrar_usuario()
                elif opcion == "5":
                    promedio_edad_por_funcion()
                elif opcion == "6":
                    usuarios_con_mas_reservas()
                elif opcion == "7":
                    topTresUsuariosMasJovenes()
                elif opcion == "8":
                    reporte_cruzado_usuarios_obras() # NUEVO

        print("\n\n")

if __name__ == "__main__":
    main()
