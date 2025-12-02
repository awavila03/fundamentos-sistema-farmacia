import os

# Nombre de nuestra "Base de Datos" en texto plano
ARCHIVO_INVENTARIO = 'productos.csv'

def cargar_inventario():
    """
    Lee el archivo CSV y devuelve una Matriz (Lista de Listas).
    Sin usar librerías externas.
    """
    lista_productos = []
    
    # Validamos que el archivo exista para que no explote el programa
    if not os.path.exists(ARCHIVO_INVENTARIO):
        print(f"Error: No se encontró {ARCHIVO_INVENTARIO}. Iniciando vacío.")
        return []

    try:
        # 'utf-8' es importante para que lea tildes y ñ sin problemas
        with open(ARCHIVO_INVENTARIO, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                linea = linea.strip() # Limpiamos espacios y 'enters' al inicio/final
                
                # Ignorar líneas vacías
                if not linea:
                    continue
                
                # --- AQUÍ ESTÁ LA MAGIA ---
                # Convertimos "101,Paracetamol,2.5,100" en ["101", "Paracetamol", "2.5", "100"]
                datos = linea.split(',') 
                
                # Casteo de datos (Convertir texto a números)
                try:
                    id_prod = int(datos[0])
                    nombre = datos[1]
                    precio = float(datos[2])
                    stock = int(datos[3])
                    
                    # Guardamos como lista: [ID, Nombre, Precio, Stock]
                    lista_productos.append([id_prod, nombre, precio, stock])
                except ValueError:
                    print(f"Advertencia: Datos corruptos en la línea: {linea}")
                    continue

        return lista_productos

    except Exception as e:
        print(f"Error crítico leyendo el archivo: {e}")
        return []

# --- ZONA DE PRUEBAS ---
# Esto solo se ejecuta si corres este archivo directamente
if __name__ == "__main__":
    print("Cargando sistema...")
    inventario = cargar_inventario()
    
    print(f"\nSe cargaron {len(inventario)} productos correctamente:")
    for producto in inventario:
        print(producto)
    