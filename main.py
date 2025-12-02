import os  # Importamos 'os' para poder crear carpetas y verificar si existen archivos
from datetime import datetime # Importamos 'datetime' para poner fecha y hora a las boletas

# =============================================================================
# 1. CONFIGURACIÓN INICIAL (Variables Globales)
# Definimos las rutas aquí al inicio para tener orden.
# =============================================================================

CARPETA_DATOS = 'datos'           # Nombre de la carpeta donde guardaremos el CSV
NOMBRE_ARCHIVO = 'productos.csv'  # Nombre del archivo físico

# os.path.join une la carpeta y el archivo usando la barra correcta (\ o /)
# Esto crea la ruta: "datos/productos.csv"
ARCHIVO_INVENTARIO = os.path.join(CARPETA_DATOS, NOMBRE_ARCHIVO)


# =============================================================================
# 2. CAPA DE DATOS (Lectura y Escritura)
# Primero cargamos la información, porque sin datos no hay programa.
# =============================================================================

def cargar_inventario():
    # Función que lee el archivo CSV y carga los datos en una MATRIZ (Lista de Listas).
    # Si el archivo no existe, devuelve None para avisar que hay un error crítico.
    
    inventario = [] # Lista vacía donde iremos guardando cada fila del excel/csv
    
    # Validamos: ¿Existe el archivo en la computadora?
    if os.path.exists(ARCHIVO_INVENTARIO):
        
        # Abrimos el archivo en modo LECTURA ('r' = read)
        # encoding='utf-8' sirve para que lea bien las tildes y la letra 'ñ'
        archivo = open(ARCHIVO_INVENTARIO, 'r', encoding='utf-8')
        
        # Recorremos el archivo línea por línea (como leer un libro)
        for linea in archivo:
            linea = linea.strip() # Limpieza: Quitamos espacios y saltos de línea (\n)
            
            # Solo procesamos la línea si tiene texto (len > 0)
            if len(linea) > 0:
                datos = linea.split(',') # Separamos el texto por las comas
                
                # --- CASTEO DE DATOS ---
                # Todo lo que viene del archivo es Texto (String).
                # Debemos convertirlo a números para poder operar (restar stock, multiplicar precio).
                id_producto = int(datos[0])    # Convertimos ID a Entero
                nombre = datos[1]              # El nombre se queda como Texto
                precio = float(datos[2])       # Convertimos Precio a Decimal
                stock = int(datos[3])          # Convertimos Stock a Entero
                
                # Creamos el arreglo del producto: [101, "Paracetamol", 2.5, 100]
                fila = [id_producto, nombre, precio, stock]
                
                # Agregamos esa fila a nuestra matriz principal 'inventario'
                inventario.append(fila)
        
        archivo.close() # ¡Muy importante! Cerramos el archivo al terminar.
        return inventario
    
    else:
        # Si no existe el archivo, imprimimos error y devolvemos None.
        print("\n[ERROR CRÍTICO] No se encontró la base de datos.")
        print("Por favor verifica que exista la carpeta 'datos' y el archivo 'productos.csv'")
        return None 

def guardar_cambios(inventario):
    # Esta función toma la matriz de la memoria RAM y la guarda en el Disco Duro.
    # Se usa al salir del programa para no perder los cambios.
    
    # Seguridad: Si borraron la carpeta 'datos' por error, la creamos de nuevo.
    if not os.path.exists(CARPETA_DATOS):
        os.makedirs(CARPETA_DATOS)

    # Abrimos en modo ESCRITURA ('w' = write).
    # OJO: Esto borra el archivo anterior y crea uno nuevo con los datos actualizados.
    archivo = open(ARCHIVO_INVENTARIO, 'w', encoding='utf-8')
    
    for producto in inventario:
        # Reconstruimos la línea de texto para el CSV: "101,Nombre,2.5,100"
        # Usamos str() para convertir los números a texto y poder unirlos con '+'
        linea = str(producto[0]) + "," + producto[1] + "," + str(producto[2]) + "," + str(producto[3]) + "\n"
        archivo.write(linea)
            
    archivo.close()
    print(">> Base de datos actualizada correctamente.")


# =============================================================================
# 3. CAPA DE INTERFAZ (Menús y Visualización)
# Aquí definimos cómo se ve el programa para el usuario.
# =============================================================================

def mostrar_menu():
    # Un print simple para mostrar las opciones disponibles
    print("\n" + "="*40)
    print("     SISTEMA DE GESTIÓN DE MEDIFARM")
    print("="*40)
    print("[1] Ver Inventario")
    print("[2] Realizar Venta")
    print("[3] Ingresar Stock")
    print("[4] Guardar y Salir")
    print("-" * 40)

def ver_inventario(inventario):
    """
    Recorre la matriz y muestra los datos ordenados como una tabla.
    """
    print("\n--- REPORTE DE INVENTARIO ---")
    print("ID    | PRODUCTO                  | PRECIO     | STOCK")
    print("-" * 60)
    
    for prod in inventario:
        # Formateo visual: .ljust(x) rellena con espacios a la derecha hasta llegar a x caracteres.
        # Esto hace que las columnas queden derechitas.
        columna_id = str(prod[0]).ljust(5)
        columna_nom = prod[1].ljust(25)
        columna_pre = ("S/" + str(prod[2])).ljust(10)
        columna_stk = str(prod[3])
        
        fila = columna_id + " | " + columna_nom + " | " + columna_pre + " | " + columna_stk
        print(fila)


# =============================================================================
# 4. CAPA DE LÓGICA DE NEGOCIO (Operaciones)
# Aquí programamos qué hace realmente cada opción del menú.
# =============================================================================

def realizar_venta(inventario):
    print("\n--- MÓDULO DE VENTA ---")
    
    # 1. Pedimos datos y validamos que sean números
    entrada = input("Ingrese el ID del producto: ")
    if entrada.isdigit(): 
        id_buscado = int(entrada)
    else:
        print("Error: El ID debe ser un número.")
        return [] # Retornamos lista vacía indicando que falló

    # 2. Búsqueda Secuencial: Buscamos el ID en la matriz
    producto_encontrado = [] 
    
    for producto in inventario:
        if producto[0] == id_buscado:
            producto_encontrado = producto # ¡Lo encontramos! Guardamos la referencia.
            break # Dejamos de buscar para ahorrar tiempo
    
    # 3. Verificamos si encontramos algo
    if len(producto_encontrado) > 0:
        # Mostramos info al usuario
        print(">> Producto: " + producto_encontrado[1])
        print(">> Stock:    " + str(producto_encontrado[3]))
        print(">> Precio:   S/ " + str(producto_encontrado[2]))
        
        entrada_cant = input("Ingrese cantidad a vender: ")
        
        if entrada_cant.isdigit():
            cantidad = int(entrada_cant)
            
            # 4. Validaciones de Negocio (Reglas de la farmacia)
            if cantidad <= 0:
                print("Error: La cantidad debe ser mayor a 0.")
                return []
            elif cantidad > producto_encontrado[3]:
                print("Error: Stock insuficiente.")
                return []
            else:
                # --- ACTUALIZACIÓN DE STOCK (En Memoria) ---
                # Restamos la cantidad al stock actual (índice 3)
                producto_encontrado[3] = producto_encontrado[3] - cantidad
                total = cantidad * producto_encontrado[2]
                
                print("\n VENTA EXITOSA")
                print("Total a cobrar: S/ " + str(total))
                print("Nuevo Stock:    " + str(producto_encontrado[3]))
                
                # Preparamos una lista con el resumen para poder imprimir la boleta luego
                # Estructura: [Nombre, Cantidad, Total]
                datos_venta = [producto_encontrado[1], cantidad, total]
                return datos_venta 
        else:
            print("Error: Cantidad inválida.")
            return []
    else:
        print("Error: Producto no encontrado.")
        return []

def agregar_stock(inventario):
    print("\n--- REABASTECIMIENTO ---")
    
    entrada = input("Ingrese el ID del producto: ")
    if entrada.isdigit():
        id_buscado = int(entrada)
    else:
        print("Error: ID inválido.")
        return

    # Reutilizamos la lógica de búsqueda
    producto_encontrado = []
    for producto in inventario:
        if producto[0] == id_buscado:
            producto_encontrado = producto
            break
            
    if len(producto_encontrado) > 0:
        print(">> Producto: " + producto_encontrado[1])
        print(">> Stock actual: " + str(producto_encontrado[3]))
        
        entrada_cant = input("Ingrese cantidad a sumar: ")
        if entrada_cant.isdigit():
            cantidad_nueva = int(entrada_cant)
            
            if cantidad_nueva > 0:
                # Sumamos la nueva cantidad al stock existente
                producto_encontrado[3] = producto_encontrado[3] + cantidad_nueva
                print("\n STOCK ACTUALIZADO")
                print("Nuevo Stock: " + str(producto_encontrado[3]))
            else:
                print("Error: La cantidad debe ser positiva.")
        else:
            print("Error: Cantidad inválida.")
    else:
        print("Error: Producto no encontrado.")


# =============================================================================
# 5. CAPA DE REPORTES (Boletas TXT)
# =============================================================================

def generar_boleta_txt(datos_venta):
    """
    Genera un archivo de texto con la boleta.
    Usa la fecha y hora para que el nombre del archivo nunca se repita.
    Recibe: [Nombre, Cantidad, Total]
    """
    print("\n--- GENERANDO COMPROBANTE ---")
    cliente = input("Nombre del Cliente: ")
    ruc = input("RUC o DNI: ")
    
    # Obtenemos fecha y hora exacta
    ahora = datetime.now()
    # Formato para el nombre del archivo (ej: 20231201_143000)
    marca_tiempo = ahora.strftime("%Y%m%d%H%M%S")
    # Formato para escribir dentro de la boleta (ej: 01/12/2023 14:30:00)
    fecha_impresion = ahora.strftime("%d/%m/%Y %H:%M:%S")

    # Creamos la carpeta 'boletas' si no existe
    carpeta = "boletas"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    
    # Nombre único del archivo
    nombre_archivo = "boleta_" + ruc + "_" + marca_tiempo + ".txt"
    ruta_final = os.path.join(carpeta, nombre_archivo)
    
    # Escribimos el contenido
    archivo = open(ruta_final, 'w', encoding='utf-8')
    
    archivo.write("==========================================\n")
    archivo.write("              'FARMACIA MEDIFARM'         \n")
    archivo.write("==========================================\n")
    archivo.write("Fecha:   " + fecha_impresion + "\n")
    archivo.write("Cliente: " + cliente + "\n")
    archivo.write("DOC:     " + ruc + "\n")
    archivo.write("------------------------------------------\n")
    archivo.write("Producto: " + datos_venta[0] + "\n")
    archivo.write("Cantidad: " + str(datos_venta[1]) + "\n")
    archivo.write("TOTAL:    S/ " + str(datos_venta[2]) + "\n")
    archivo.write("==========================================\n")
    
    archivo.close()
    print(">> Archivo guardado en: " + ruta_final)


# =============================================================================
# 6. FLUJO PRINCIPAL (MAIN)
# Aquí unimos todo: Carga -> Bucle -> Menú -> Funciones
# =============================================================================

def main():
    # 1. Intentamos cargar los datos del archivo a la memoria
    mis_productos = cargar_inventario()
    
    # Validación de Seguridad: Si la carga falló (devuelve None), cerramos el programa.
    if mis_productos == None:
        return # 'return' en el main finaliza el script

    print(">> Sistema iniciado. " + str(len(mis_productos)) + " productos cargados.")
    
    continuar = True # Variable bandera para controlar el bucle
    
    # 2. Bucle infinito (El programa corre hasta que el usuario diga basta)
    while continuar:
        mostrar_menu() # Mostramos las opciones
        opcion = input("Ingrese una opción: ")
        
        # 3. Decidimos qué función llamar según la opción
        if opcion == "1":
            ver_inventario(mis_productos)
            input("\nEnter para continuar...") # Pausa para que el usuario lea
            
        elif opcion == "2":
            resultado = realizar_venta(mis_productos)
            # Si 'resultado' tiene datos, significa que la venta se hizo.
            if len(resultado) > 0:
                if input("¿Generar boleta? (s/n): ") == "s":
                    generar_boleta_txt(resultado)
            input("\nEnter para continuar...")
            
        elif opcion == "3":
            agregar_stock(mis_productos)
            input("\nEnter para continuar...")
            
        elif opcion == "4":
            print("Guardando cambios...")
            guardar_cambios(mis_productos) # Guardamos en CSV antes de salir
            continuar = False # Cambiamos la bandera a False para romper el while
            print("¡Hasta luego!")
            
        else:
            print("Opción no válida.")

# Punto de entrada estándar de Python.
main()