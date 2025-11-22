import re, os, json
from utilidades import *

ARCHIVO_RESERVAS = "archivos/reservas.txt"
ARCHIVO_TEMP = "archivos/reservas_temp.txt"

butacas_visuales = [
    [("A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8")],
    [("B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8")],
    [("C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8")],
    [("D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8")],
    [("E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8")],
    [("F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8")],
    [("G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8")],
    [("H1", "H2", "H3", "H4", "H5", "H6", "H7", "H8")],
]

butacas_estado = [["0"] * 8 for _ in range(8)]

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

def leer_reservas():
    reservas = []
    try:
        with open(ARCHIVO_RESERVAS, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if linea:
                    try:
                        partes = linea.split(";")
                        reserva = [
                            int(partes[0]), int(partes[1]), int(partes[2]),
                            int(partes[3]), partes[4], int(partes[5]), int(partes[6]),
                        ]
                        reservas.append(reserva)
                    except (ValueError, IndexError):
                        print(f"Error: Se omitió una línea mal formada en {ARCHIVO_RESERVAS}")
    except FileNotFoundError:
        print(f"Nota: No se encontró {ARCHIVO_RESERVAS}.")
    return reservas

def butaca_valida(b):
    return re.match(r"^[A-Ha-h][1-8]$", b.strip()) is not None

def buscar_pos(butaca):
    pos = None
    f = 0
    while f < len(butacas_visuales) and pos is None:
        fila_tupla = butacas_visuales[f][0]
        c = 0
        while c < len(fila_tupla) and pos is None:
            if fila_tupla[c] == butaca:
                pos = (f, c)
            c += 1
        f += 1
    return pos

def buscar_precio(id):
    # Lectura directa para evitar ciclos
    try:
        with open("archivos/obras.json", "r", encoding="UTF-8") as f:
            lista_obras = json.load(f)
        for o in lista_obras:
            if o.get("ID") == id:
                return o.get("Precio")
        return None
    except:
        return None

def mostrar_butacas():
    print("\n======================== BUTACAS ============================")
    print("    " + "".join([f"{n:>4}" for n in range(1, 9)])) # List comprehension pequeña
    f = 0
    while f < len(butacas_visuales):
        fila_letra = chr(ord("A") + f)
        fila_tupla = butacas_visuales[f][0]
        celdas = []
        c = 0
        while c < len(fila_tupla):
            if butacas_estado[f][c] == "X":
                celdas.append(f"{'[X]':>4}")
            else:
                celdas.append(f"{fila_tupla[c]:>4}")
            c += 1
        print(f"{fila_letra} | " + " ".join(celdas))
        f += 1

def mostrar_reservas(reservas_):
    encabezados = ["Usuario", "NR", "ID Obra", "Cant", "Butacas", "Precio", "Total"]
    mostrar_matriz(reservas_, encabezados)

def init_estado_desde_reservas():
    reservas = leer_reservas()
    # Resetear matriz
    for f in range(len(butacas_estado)):
        for c in range(len(butacas_estado[f])):
            butacas_estado[f][c] = "0"

    i = 0
    while i < len(reservas):
        butacas_str = reservas[i][4]
        partes = butacas_str.split(",")
        j = 0
        while j < len(partes):
            buscada = partes[j].strip().upper()
            pos = buscar_pos(buscada)
            if pos is not None:
                ff, cc = pos
                butacas_estado[ff][cc] = "X"
            j += 1
        i += 1

def _construir_ids_obras():
    try:
        with open("archivos/obras.json", "r", encoding="UTF-8") as f:
            lista_obras = json.load(f)
        # Uso de conjunto (Set) para ids unicos
        ids = {o.get("ID") for o in lista_obras}
        return list(ids)
    except:
        return []

def crear_reserva():
    # Aseguramos que la matriz esté actualizada con las 'X' antes de empezar
    init_estado_desde_reservas()
    
    usuario = ingreso_entero("Coloque el id de usuario: ")
    ultimo_nr = _obtener_ultimo_id(ARCHIVO_RESERVAS, id_columna=1)
    nr = ultimo_nr + 1

    ids_obras = _construir_ids_obras()
    if not ids_obras:
        print("Error: No se pudieron cargar las obras.")
        return

    id_obra_valido = 0
    ok = False
    while ok == False:
        id_obra_valido = ingreso_entero("Id de la obra: ")
        if id_obra_valido in ids_obras:
            ok = True
        else:
            print("ID inexistente.")

    cant = ingreso_entero("Cuántas entradas deseas reservar: ")
    while cant <= 0:
        cant = ingreso_entero("Debe ser positivo: ")

    # NUEVO: Mostramos las butacas con las ocupadas ya marcadas
    mostrar_butacas()
    
    butacas_elegidas = []
    i = 0
    while i < cant:
        valida = False
        while valida == False:
            butaca = input(f"Butaca que desea ({i+1}/{cant}): ").strip().upper()
            if not butaca_valida(butaca):
                print("Formato inválido (ej: C5).")
            else:
                if butaca in butacas_elegidas:
                    print("Ya elegiste esa butaca.")
                else:
                    pos = buscar_pos(butaca)
                    if pos is None:
                        print("Esa butaca no existe.")
                    else:
                        f, c = pos
                        if butacas_estado[f][c] == "X":
                            print("¡Esa butaca ya está ocupada! Elegí otra.")
                        else:
                            butacas_estado[f][c] = "X"
                            butacas_elegidas.append(butaca)
                            valida = True
        i += 1

    butacas_cadena = ",".join(butacas_elegidas)
    precio = buscar_precio(id_obra_valido)

    if precio is None:
        print("Error precio no encontrado.")
    else:
        total = precio * cant
        print(f"Precio unitario: ${precio}")
        print(f"Total a abonar: ${total}")
        
        reserva = [usuario, nr, id_obra_valido, cant, butacas_cadena, precio, total]
        linea = ";".join([str(item) for item in reserva]) + "\n"

        try:
            with open(ARCHIVO_RESERVAS, "a", encoding="utf-8") as f:
                f.write(linea)
            print(f"¡Reserva realizada! Número: {nr}")
        except OSError as e:
            print(f"Error al guardar: {e}")

    input("Presione ENTER para continuar.")

def modificar_reserva():
    # Lógica idéntica a tu original
    nr_modificar = ingreso_entero("Ingrese el número de reserva que desea modificar: ")
    encontrado = False
    try:
        with open(ARCHIVO_RESERVAS, "r", encoding="utf-8") as arch_orig, open(ARCHIVO_TEMP, "w", encoding="utf-8") as arch_temp:
            for linea in arch_orig:
                linea = linea.strip()
                if not linea: continue
                try:
                    partes = linea.split(";")
                    nr_actual = int(partes[1])
                    if nr_actual == nr_modificar:
                        encontrado = True
                        print(f"Encontrada: {linea}")
                        
                        id_usuario = partes[0]
                        id_obra = partes[2]
                        precio = int(partes[5])
                        cantidad = int(partes[3])

                        nuevo_usuario = input("Nuevo ID usuario (ENTER igual): ")
                        if nuevo_usuario.isdigit(): id_usuario = nuevo_usuario
                        
                        nuevo_obra = input("Nuevo ID obra (ENTER igual): ")
                        if nuevo_obra.isdigit():
                            id_obra = nuevo_obra
                            precio_nuevo = buscar_precio(int(id_obra))
                            if precio_nuevo: precio = precio_nuevo

                        total = precio * cantidad
                        nueva_linea = f"{id_usuario};{nr_actual};{id_obra};{cantidad};{partes[4]};{precio};{total}\n"
                        arch_temp.write(nueva_linea)
                    else:
                        arch_temp.write(linea + "\n")
                except:
                    arch_temp.write(linea + "\n")
    except: pass

    if encontrado:
        os.remove(ARCHIVO_RESERVAS)
        os.rename(ARCHIVO_TEMP, ARCHIVO_RESERVAS)
        print("Modificado.")
    else:
        os.remove(ARCHIVO_TEMP)
        print("No encontrado.")
    input("ENTER.")

def borrar_reserva():
    nr_borrar = ingreso_entero("Ingrese el número de reserva que desea borrar: ")
    encontrado = False
    linea_borrada = None

    try:
        with open(ARCHIVO_RESERVAS, "r", encoding="utf-8") as arch_orig, open(ARCHIVO_TEMP, "w", encoding="utf-8") as arch_temp:
            for linea in arch_orig:
                linea = linea.strip()
                if not linea: continue
                try:
                    partes = linea.split(";")
                    if int(partes[1]) == nr_borrar:
                        encontrado = True
                        linea_borrada = partes
                        print(f"Reserva {nr_borrar} eliminada.")
                    else:
                        arch_temp.write(linea + "\n")
                except:
                    arch_temp.write(linea + "\n")
    except: pass

    if encontrado:
        if linea_borrada:
            # Liberar butacas
            bs = linea_borrada[4].split(",")
            for b in bs:
                pos = buscar_pos(b.strip().upper())
                if pos: butacas_estado[pos[0]][pos[1]] = "0"
        os.remove(ARCHIVO_RESERVAS)
        os.rename(ARCHIVO_TEMP, ARCHIVO_RESERVAS)
    else:
        os.remove(ARCHIVO_TEMP)
        print("No encontrada.")
    input("ENTER.")
