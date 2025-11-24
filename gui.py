import json

from tkinter import *
from tkinter import messagebox, simpledialog

from obras import cargar_json, modificar_json
from utilidades import *
from funciones import *


def mostrar_obras():
    lista = cargar_json("archivos/obras.json")
    if not lista:
        messagebox.showinfo("No hay obras", "No hay obras para mostrar.")
        return

    mensaje = "\n".join(
        [
            f"{obra['ID']} - {obra['Nombre']} - ${obra['Precio']} - {obra['Categoria']} - {obra['Duracion']} min"
            for obra in lista
        ]
    )
    messagebox.showinfo("Obras", mensaje)


def agregar_obras():
    obras = cargar_json("archivos/obras.json")

    if not obras:
        nuevo_id = 1
    else:
        nuevo_id = max(obra["ID"] for obra in obras) + 1

    nombre = simple_input("Nombre de la obra: ")
    precio = int(simple_input("Precio de la obra: "))
    categoria = simple_input("Categoría de la obra: ")
    duracion = int(simple_input("Duración de la obra (minutos): "))

    nueva_obra = {
        "ID": nuevo_id,
        "Nombre": nombre,
        "Precio": precio,
        "Categoria": categoria,
        "Duracion": duracion,
    }

    obras.append(nueva_obra)
    modificar_json("archivos/obras.json", obras)
    messagebox.showinfo("Obra agregada", f"Obra '{nombre}' agregada con éxito.")


def modificar_obra():
    obras = cargar_json("archivos/obras.json")

    if not obras:
        messagebox.showinfo("No hay obras", "No hay obras para modificar.")
        return

    id_mod = int(simple_input("Ingrese el ID de la obra a modificar: "))
    obra = next((o for o in obras if o["ID"] == id_mod), None)

    if not obra:
        messagebox.showerror(
            "Obra no encontrada", "No se encontró ninguna obra con ese ID."
        )
        return

    nombre = simple_input(
        f"Nuevo nombre (actual: {obra['Nombre']}): ", default=obra["Nombre"]
    )
    precio = int(
        simple_input(
            f"Nuevo precio (actual: {obra['Precio']}): ", default=obra["Precio"]
        )
    )
    categoria = simple_input(
        f"Nueva categoría (actual: {obra['Categoria']}): ", default=obra["Categoria"]
    )
    duracion = int(
        simple_input(
            f"Nueva duración (actual: {obra['Duracion']}): ", default=obra["Duracion"]
        )
    )

    obra["Nombre"] = nombre
    obra["Precio"] = precio
    obra["Categoria"] = categoria
    obra["Duracion"] = duracion

    modificar_json("archivos/obras.json", obras)
    messagebox.showinfo("Obra modificada", f"Obra '{nombre}' modificada con éxito.")


def borrar_obra():
    obras = cargar_json("archivos/obras.json")

    if not obras:
        messagebox.showinfo("No hay obras", "No hay obras para borrar.")
        return

    id_borrar = int(simple_input("Ingrese el ID de la obra a borrar: "))
    obra = next((o for o in obras if o["ID"] == id_borrar), None)

    if not obra:
        messagebox.showerror(
            "Obra no encontrada", "No se encontró ninguna obra con ese ID."
        )
        return

    respuesta = messagebox.askyesno(
        "Confirmación", f"¿Está seguro de que desea borrar '{obra['Nombre']}'?"
    )
    if respuesta:
        obras.remove(obra)
        modificar_json("archivos/obras.json", obras)
        messagebox.showinfo(
            "Obra eliminada", f"Obra '{obra['Nombre']}' eliminada con éxito."
        )
    else:
        messagebox.showinfo("Operación cancelada", "No se eliminó ninguna obra.")


def simple_input(prompt, default=None):
    """Función para obtener entradas simples, con valor por defecto"""
    value = simpledialog.askstring("Input", prompt, initialvalue=default)
    return value if value is not None else ""


# Menu Obras
def crear_menu():
    ventana = Tk()
    ventana.title("CRUD de Obras")

    def on_mostrar():
        mostrar_obras()

    def on_agregar():
        agregar_obras()

    def on_modificar():
        modificar_obra()

    def on_borrar():
        borrar_obra()

    # Botones
    btn_mostrar = Button(ventana, text="Mostrar Obras", command=on_mostrar, width=30)
    btn_mostrar.pack(pady=10)

    btn_agregar = Button(ventana, text="Agregar Obra", command=on_agregar, width=30)
    btn_agregar.pack(pady=10)

    btn_modificar = Button(
        ventana, text="Modificar Obra", command=on_modificar, width=30
    )
    btn_modificar.pack(pady=10)

    btn_borrar = Button(ventana, text="Borrar Obra", command=on_borrar, width=30)
    btn_borrar.pack(pady=10)

    btn_salir = Button(ventana, text="Salir", command=ventana.quit, width=30)
    btn_salir.pack(pady=10)

    ventana.mainloop()


# Ejecutar el menú
if __name__ == "__main__":
    crear_menu()
