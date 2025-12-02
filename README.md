# Sistema de Gestión de MEDIFARM 💊

Proyecto final para el curso de **Fundamentos de Programación I**.
Este es un sistema de consola desarrollado en Python que permite administrar el inventario, las ventas y el reabastecimiento de una farmacia de manera eficiente y ordenada.

## 📋 Descripción

El programa simula el flujo de trabajo real de una farmacia. Utiliza una base de datos en archivo plano (CSV) para la persistencia de datos y genera comprobantes de venta en archivos de texto (TXT) organizados por carpetas.

El código ha sido estructurado siguiendo un diseño modular (Top-Down):
1.  **Capa de Datos:** Lectura/Escritura de archivos.
2.  **Capa de Interfaz:** Menús visuales.
3.  **Capa de Lógica:** Validaciones y operaciones matemáticas.

## 🚀 Funcionalidades Principales

* **Carga de Datos:** Lectura automática del inventario desde `datos/productos.csv`.
* **Visualización:** Tabla de productos formateada y alineada.
* **Ventas:**
    * Búsqueda de productos por ID.
    * Validación de stock disponible.
    * Cálculo automático de totales.
    * Actualización inmediata del stock en memoria.
* **Reportes:** Generación de **Boletas de Venta** únicas (usando fecha y hora) en la carpeta `boletas/`.
* **Reabastecimiento:** Opción para ingresar nueva mercadería.
* **Persistencia:** Guardado seguro de cambios al cerrar el sistema.

## 🛠️ Tecnologías y Conceptos Aplicados

Este proyecto fue desarrollado **sin librerías externas** para la gestión de datos, demostrando el dominio de los fundamentos del lenguaje:

* **Lenguaje:** Python 3.
* **Estructuras de Datos:** Listas (Arreglos) y Matrices (Listas de listas).
* **Control de Flujo:** Bucles `while`, `for` y condicionales `if/elif/else`.
* **Manejo de Archivos:** Uso de `open()`, `write()`, `close()` y manipulación de cadenas (`split`, `strip`).
* **Librerías Estándar:** `os` (gestión de rutas) y `datetime` (timestamps para boletas).

## 📂 Estructura del Proyecto

```text
sistema-farmacia/
│
├── datos/
│   └── productos.csv    # Base de datos (Inventario inicial)
│
├── boletas/             # Carpeta generada automáticamente
│   └── boleta_RUC_...   # Comprobantes de pago generados
│
├── main.py              # Código fuente principal
└── README.md            # Documentación del proyecto
```

## 👤 Autores

* **Avila Arauco, Angel** (u202523590)
* **Bellido Apolo, Mathías** (u202522188)
* **Garcia Jimenez, Brian** (u202524706)
* **Huiza Bejar, Carlos** (u202522413)