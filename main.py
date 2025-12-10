# =============================================================================
# 1. CONFIGURACIÓN INICIAL (Variables Globales)
# Importamos las librerías a utilizar y definimos las rutas de los datos.
# =============================================================================

import os  # Importamos 'os' para manejar rutas de carpetas y archivos (Windows/Linux)
from datetime import datetime # Importamos 'datetime' para poner fecha y hora exacta a las boletas

CARPETA_DATOS = 'datos'           # Nombre de la carpeta donde vive la base de datos
NOMBRE_ARCHIVO = 'productos.csv'  # Nombre del archivo físico
# os.path.join crea la ruta correcta sin importar el sistema operativo: "datos/productos.csv"
ARCHIVO_INVENTARIO = os.path.join(CARPETA_DATOS, NOMBRE_ARCHIVO)


# =============================================================================
# 2. CARGA DE DATOS A MEMORIA 
# La memoria es mucho más rápida que el disco
# =============================================================================

def cargar_inventario():
    # Lee el archivo CSV y carga los datos en una MATRIZ (Lista de Listas).
    # Si el archivo no existe, devuelve None para detener el programa.
    
    inventario = [] # Lista vacía que llenaremos con cada fila del csv
    
    # Validamos: ¿Existe el archivo en la computadora?
    if os.path.exists(ARCHIVO_INVENTARIO):
        
        # Abrimos el archivo en modo LECTURA ('r' = read)
        # encoding='utf-8' sirve para que lea bien las tildes y la letra 'ñ'
        archivo = open(ARCHIVO_INVENTARIO, 'r', encoding='utf-8')
        
        # Recorremos el archivo línea por línea
        for linea in archivo:
            linea = linea.strip() # Limpieza: Quitamos espacios y saltos de línea (\n)
            
            # Solo procesamos si la línea tiene información (evitamos líneas vacías)
            if len(linea) > 0:
                datos = linea.split(',') # Convertimos el texto en lista separando por comas
                
                # --- CASTEO DE DATOS (Conversión de Tipos) ---
                # El archivo nos da texto (String), debemos convertirlo a números.
                id_producto = int(datos[0])    # ID -> Entero
                nombre = datos[1]              # Nombre -> Texto
                precio = float(datos[2])       # Precio -> Decimal
                stock = int(datos[3])          # Stock -> Entero
                
                # Creamos el arreglo del producto: [101, "Paracetamol", 2.5, 100]
                fila = [id_producto, nombre, precio, stock]
                
                # Agregamos esa fila a nuestra matriz principal
                inventario.append(fila)
        
        archivo.close() # ¡Importante! Siempre cerrar el archivo.
        return inventario
    
    else:
        # Si no existe el archivo, imprimimos error y devolvemos None.
        print("\n[ERROR CRÍTICO] No se encontró la base de datos.")
        print("Ubicación esperada: " + ARCHIVO_INVENTARIO)
        return None 

def guardar_cambios(inventario):
    # Vuelca la matriz de la memoria RAM al disco duro (CSV).
    # Se ejecuta al salir para guardar todas las ventas realizadas.
    
    # Seguridad: Si borraron la carpeta 'datos' por error, la creamos.
    if not os.path.exists(CARPETA_DATOS):
        os.makedirs(CARPETA_DATOS)

    # Abrimos en modo ESCRITURA ('w' = write).
    # OJO: Esto borra el contenido anterior y escribe lo nuevo.
    archivo = open(ARCHIVO_INVENTARIO, 'w', encoding='utf-8')
    
    for producto in inventario:
        # Reconstruimos la línea de texto CSV: "101,Nombre,2.5,100\n"
        # Usamos str() para convertir números a texto y concatenar con '+'
        linea = str(producto[0]) + "," + producto[1] + "," + str(producto[2]) + "," + str(producto[3]) + "\n"
        archivo.write(linea)
            
    archivo.close()
    print(">> Base de datos actualizada correctamente.")


# =============================================================================
# 3. CAPA DE INTERFAZ (Menús y Visualización)
# "La cara del programa": Lo que el usuario ve.
# =============================================================================

def mostrar_menu():
    print("\n" + "="*40)
    print("      SISTEMA DE GESTIÓN DE FARMACIA")
    print("="*40)
    print("[1] Ver Inventario")
    print("[2] Realizar Venta")
    print("[3] Ingresar Stock")
    print("[4] Guardar y Salir")
    print("-" * 40)

def ver_inventario(inventario):
    # Recorre la matriz y muestra los datos ordenados como tabla.
    # AJUSTE: Se amplió el ancho de columna a 40 para nombres largos.
    
    print("\n--- REPORTE DE INVENTARIO ---")
    print("ID    | PRODUCTO                                 | PRECIO       | STOCK")
    print("-" * 78)
    
    for prod in inventario:
        # Formateo: .ljust(x) rellena con espacios a la derecha hasta llegar a x caracteres.
        # Esto alinea las columnas perfectamente sin usar librerías externas.
        columna_id = str(prod[0]).ljust(5)
        columna_nom = prod[1].ljust(40)
        columna_pre = ("S/" + str(prod[2])).ljust(12)
        columna_stk = str(prod[3])
        
        # Imprimimos la fila formateada
        print(columna_id + " | " + columna_nom + " | " + columna_pre + " | " + columna_stk)


# =============================================================================
# 4. CAPA DE LÓGICA DE NEGOCIO (Operaciones con Carrito)
# "El cerebro": Validaciones, cálculos y reglas del negocio.
# =============================================================================

def realizar_venta(inventario):
    # Función de venta MEJORADA CON CARRITO.
    # Permite agregar múltiples productos antes de finalizar la venta.
    # Retorna: La lista 'carrito' y el 'gran_total'.
    
    print("\n--- MÓDULO DE VENTA (CARRITO) ---")
    
    carrito = []      # Lista temporal para guardar los productos seleccionados
    gran_total = 0.0  # Acumulador para el monto total a pagar
    
    comprando = True  # Bandera para controlar el bucle de compra
    
    while comprando:
        # 1. Entrada Flexible: El usuario puede escribir "101" o "paracetamol"
        entrada = input("\nIngrese el ID o el Nombre del producto (o '0' para finalizar): ")
        
        # Salida rápida del bucle si el usuario ingresa '0'
        if entrada == "0":
            break
        
        id_buscado = 0 # Variable para guardar el ID final seleccionado
        
        # --- ESCENARIO A: BÚSQUEDA POR ID (Si escribió solo números) ---
        if entrada.isdigit():
            id_buscado = int(entrada)
            
        # --- ESCENARIO B: BÚSQUEDA POR NOMBRE (Si escribió letras) ---
        else:
            print(">> Buscando coincidencias con: '" + entrada + "'...")
            texto_busqueda = entrada.lower() # Convertimos a minúsculas para comparar
            
            coincidencias = [] # Lista temporal para guardar resultados
            
            # Recorremos el inventario buscando similitudes
            for producto in inventario:
                nombre_producto = producto[1].lower() 
                # Operador 'in': Verifica si el texto buscado está DENTRO del nombre
                if texto_busqueda in nombre_producto:
                    coincidencias.append(producto)
            
            # Si encontramos algo, mostramos la lista para que el usuario elija
            if len(coincidencias) > 0:
                print("\n>> Se encontraron productos similares:")
                for p in coincidencias:
                    # Mostramos ID, Nombre y Stock para ayudar a decidir
                    print(str(p[0]).ljust(5) + " | " + p[1].ljust(30) + " | Stock: " + str(p[3]))
                
                # Pedimos el ID exacto tras ver la lista
                seleccion = input("Ingrese el ID exacto del producto a vender: ")
                if seleccion.isdigit():
                    id_buscado = int(seleccion)
                else:
                    print("Error: Debe ingresar un ID numérico.")
                    continue # Regresamos al inicio del bucle while
            else:
                print(">> No se encontraron productos con ese nombre.")
                continue # Regresamos al inicio del bucle while

        # --- PROCESO DE SELECCIÓN Y VALIDACIÓN ---
        producto_encontrado = [] 
        
        # Buscamos el producto específico en la matriz principal
        for producto in inventario:
            if producto[0] == id_buscado:
                producto_encontrado = producto # Referencia a la lista original
                break
        
        # Si el producto existe...
        if len(producto_encontrado) > 0:
            print(f">> Seleccionado: {producto_encontrado[1]} (Stock: {producto_encontrado[3]})")
            
            entrada_cant = input("Ingrese cantidad a vender: ")
            
            if entrada_cant.isdigit(): 
                cantidad = int(entrada_cant)
                
                # Validaciones de Negocio
                if cantidad <= 0:
                    print("Error: La cantidad debe ser mayor a 0.")
                elif cantidad > producto_encontrado[3]:
                    print("Error: Stock insuficiente.")
                else:
                    # --- ÉXITO: AGREGAR AL CARRITO ---
                    
                    # 1. ACTUALIZACIÓN DE STOCK (En Memoria)
                    # Restamos stock inmediatamente para reservar el producto
                    producto_encontrado[3] = producto_encontrado[3] - cantidad
                    
                    # 2. Calculamos subtotal
                    subtotal = cantidad * producto_encontrado[2]
                    gran_total += subtotal # Sumamos al total general de la compra
                    
                    # 3. Guardamos en el carrito: [Nombre, Cantidad, PrecioUnit, Subtotal]
                    item_carrito = [producto_encontrado[1], cantidad, producto_encontrado[2], subtotal]
                    carrito.append(item_carrito)
                    
                    print(f"✅ Agregado: {cantidad} x {producto_encontrado[1]}")
                    print(f"   Subtotal parcial: S/ {subtotal}")
            else:
                print("Error: Cantidad inválida.")
        else:
            print("Error: Producto no encontrado con ID " + str(id_buscado))

        # --- PREGUNTA DE CONTINUACIÓN ---
        respuesta = input("\n¿Desea agregar otro producto? (s/n): ").lower()
        if respuesta != "s":
            comprando = False # Cambiamos la bandera para salir del while

    # --- FIN DEL BUCLE DE VENTA ---
    # Verificamos si el carrito tiene productos
    if len(carrito) > 0:
        print("\n" + "="*30)
        print("VENTA FINALIZADA")
        print(f"Items en carrito: {len(carrito)}")
        print(f"TOTAL A PAGAR:    S/ {gran_total}")
        print("="*30)
        return carrito, gran_total # Devolvemos la lista de compras y el total
    else:
        print("\n>> Operación cancelada o carrito vacío.")
        return [], 0.0

def agregar_stock(inventario):
    # Busca un producto y aumenta su stock.
    
    print("\n--- REABASTECIMIENTO ---")
    
    entrada = input("Ingrese el ID del producto: ")
    if entrada.isdigit():
        id_buscado = int(entrada)
    else:
        print("Error: ID inválido.")
        return

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
                # Sumamos la cantidad nueva al stock existente
                producto_encontrado[3] = producto_encontrado[3] + cantidad_nueva
                print("\n✅ STOCK ACTUALIZADO ✅")
                print("Nuevo Stock: " + str(producto_encontrado[3]))
            else:
                print("Error: Cantidad debe ser positiva.")
        else:
            print("Error: Cantidad inválida.")
    else:
        print("Error: Producto no encontrado.")


# =============================================================================
# 5. CAPA DE REPORTES (Generación de Archivos)
# =============================================================================

def generar_boleta_txt(carrito, gran_total):
    # Genera un TXT único con el detalle de TODOS los productos del carrito.
    # Recibe: La lista 'carrito' y el 'gran_total'.
    
    print("\n--- GENERANDO COMPROBANTE ---")
    cliente = input("Nombre del Cliente: ")
    ruc = input("RUC o DNI: ")
    
    # Obtenemos fecha y hora exacta
    ahora = datetime.now()
    # Timestamp para el nombre del archivo
    marca_tiempo = ahora.strftime("%Y%m%d_%H%M%S")
    # Fecha legible para imprimir DENTRO del ticket
    fecha_impresion = ahora.strftime("%d/%m/%Y %H:%M:%S")

    # Creamos carpeta 'boletas' si no existe
    carpeta = "boletas"
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)
    
    # Nombre único del archivo
    nombre_archivo = "boleta_" + ruc + "_" + marca_tiempo + ".txt"
    ruta_final = os.path.join(carpeta, nombre_archivo)
    
    # Escritura del archivo
    archivo = open(ruta_final, 'w', encoding='utf-8')
    
    archivo.write("==============================================\n")
    archivo.write("           FARMACIA 'MEDIFARMA'               \n")
    archivo.write("==============================================\n")
    archivo.write("Fecha:   " + fecha_impresion + "\n")
    archivo.write("Cliente: " + cliente + "\n")
    archivo.write("DOC:     " + ruc + "\n")
    archivo.write("----------------------------------------------\n")
    archivo.write("DESCRIPCION                   CANT    TOTAL   \n")
    archivo.write("----------------------------------------------\n")
    
    # Bucle para imprimir cada producto del carrito
    for item in carrito:
        # item tiene la estructura: [Nombre, Cantidad, PrecioUnit, Subtotal]
        # Cortamos el nombre a 28 caracteres y rellenamos espacios
        nombre = item[0][:28].ljust(28) 
        cant = str(item[1]).center(6)
        subt = str(item[3]).rjust(8)
        
        archivo.write(f"{nombre}{cant} S/{subt}\n")
        
    archivo.write("==============================================\n")
    archivo.write(f"TOTAL A PAGAR:                S/ {gran_total}\n")
    archivo.write("==============================================\n")
    
    archivo.close()
    print(">> Archivo guardado en: " + ruta_final)


# =============================================================================
# 6. FLUJO PRINCIPAL (MAIN)
# Orquestador de todo el sistema.
# =============================================================================

def main():
    # 1. Carga Inicial de Datos
    mis_productos = cargar_inventario()
    
    # Validación Crítica: Si la carga falló, cerramos el programa.
    if mis_productos == None:
        return 

    print(">> Sistema iniciado. " + str(len(mis_productos)) + " productos cargados.")
    
    continuar = True
    
    # 2. Bucle Principal (While Infinito)
    while continuar:
        mostrar_menu()
        opcion = input("Ingrese una opción: ")
        
        # --- DERIVACIÓN A LOS MÓDULOS ---
        
        if opcion == "1":
            ver_inventario(mis_productos)
            input("\nEnter para continuar...")
            
        elif opcion == "2":
            # Recibimos DOS valores: el carrito (lista) y el total (numero)
            carrito_compras, total_pagar = realizar_venta(mis_productos)
            
            # Si el carrito tiene productos, la venta fue exitosa
            if len(carrito_compras) > 0:
                if input("¿Generar boleta? (s/n): ").lower() == "s":
                    generar_boleta_txt(carrito_compras, total_pagar)
            input("\nEnter para continuar...")
            
        elif opcion == "3":
            agregar_stock(mis_productos)
            input("\nEnter para continuar...")
            
        elif opcion == "4":
            print("Guardando cambios...")
            guardar_cambios(mis_productos) # Persistencia de datos
            continuar = False # Rompemos el ciclo
            print("¡Hasta luego!")
            
        else:
            print("Opción no válida.")


# Llamada del prorgrama
main()