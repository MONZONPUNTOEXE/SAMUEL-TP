from pickle import dumps, load
import re
from datetime import datetime


class Producto:
    def __init__(self, codigo, nombre, precio):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio

    def validar_codigo_unico_producto(self, codigo, lista):
        for item in lista:
            if item.codigo == codigo:
                return False
        return True

    def validar_string_nombre_producto(self, validacion):
        maximo_de_caracteres = 50
        return len(validacion) <= maximo_de_caracteres

    def validar_precio_en_dolares(self, precio):
        if precio > 0:
            return True
        else:
            print("El precio debe ser un número positivo mayor que 0.")
        return False

    def __repr__(self):
        return f"Producto: {self.nombre} (Código: {self.codigo}, Precio: {self.precio})"


class Cliente:
    def __init__(self, dni, nombre_y_apellido, fecha_de_nacimiento):
        self.dni = dni
        self.nombre_y_apellido = nombre_y_apellido
        self.fecha_de_nacimiento = fecha_de_nacimiento

    def validar_dni(self, dni, lista):
        if len(str(dni)) != 8 or not (0 < dni < 100000000):
            print("El DNI debe tener 8 dígitos y ser un número entero positivo.")
            return False

        for cliente in lista:
            if cliente.dni == dni:
                print("El DNI está registrado.")
                return False
        return True

    def validar_string_nombre_y_apellido(self, validar_nombres_y_apellidos):
        maximo_de_caracteres = 60
        return len(validar_nombres_y_apellidos) <= maximo_de_caracteres

    def validar_fecha_de_nacimiento(self, fecha):
        patron = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"
        if not re.match(patron, fecha):
            return False
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
            return True
        except ValueError:
            return False

    def __repr__(self):
        return f"Cliente: {self.nombre_y_apellido} (DNI: {self.dni})"


class Pedido:
    def __init__(
        self, codigo_de_pedido, productos, cliente, fecha_de_pedido, cargos_extras
    ):
        self.codigo_de_pedido = codigo_de_pedido
        self.productos = productos
        self.cliente = cliente
        self.fecha_de_pedido = fecha_de_pedido
        self.cargos_extras = cargos_extras

    def validar_codigo_de_pedidos(codigo, lista_pedidos):
        if codigo <= 0:
            print("El código de pedido debe ser un número entero positivo.")
            return False
        # Verificar que el código sea único (no repetido)
        for pedido in lista_pedidos:
            if pedido.codigo_de_pedido == codigo:
                print("El código de pedido ya está registrado.")
                return False
        return True

    def validar_productos_existentes(productos_del_pedido, lista_productos_existentes):
        for producto in productos_del_pedido:
            encontrado = False
            for producto_existente in lista_productos_existentes:
                if producto_existente.codigo == producto.codigo:
                    encontrado = True
                    break
            if not encontrado:
                print(f"El producto con el código {
                      producto.codigo} no está registrado.")
                return False
        return True

    def validar_fecha_de_pedido(self, fecha):
        patron = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"
        if not re.match(patron, fecha):
            print("El formato de la fecha debe ser DD/MM/AAAA.")
            return False
        return True

    def validar_fecha_de_pedido(fecha):
        patron = r"^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}$"
        if not re.match(patron, fecha):
            print("El formato de la fecha debe ser DD/MM/AAAA.")
        return False

    def calcular_total(self):
        total_productos = 0
        for producto in self.productos:
            total_productos += producto.precio
        return total_productos + self.cargos_extras


# Funciones de persistencia
def cargar_datos(nombre_archivo):
    with open(nombre_archivo, "rb") as bin_file:
        datos = load(bin_file)
        print(f"Datos cargados desde {nombre_archivo} correctamente.")
        return datos


def guardar_datos(nombre_archivo, datos):
    with open(nombre_archivo, "wb") as bin_file:
        bin_file.write(dumps(datos))
    print(f"Datos guardados en {nombre_archivo} correctamente.")


# Funci gestión
def crear_producto(lista):
    codigo = int(input("Ingrese el código producto: "))
    nombre = input("Ingrese el nombre del producto: ")
    precio = float(input("Ingrese el precio del producto en dólares: "))
    producto = Producto(codigo, nombre, precio)
    lista.append(producto)
    print(f"Producto {nombre} agregado exitosamente.")


def mostrar_productos(lista):
    if lista:
        for producto in lista:
            print(producto)
    else:
        print("No hay productos para mostrar.")


# crear cliente
def crear_cliente(lista_clientes):
    try:
        dni = int(input("Ingrese el DNI del cliente: "))
        nombre = input("Ingrese el nombre completo del cliente: ")
        fecha_nac = input("Ingrese la fecha de nacimiento (dd/mm/aaaa): ")
        cliente = Cliente(dni, nombre, fecha_nac)
        lista_clientes.append(cliente)
        print("Cliente agregado correctamente.")
    except ValueError:
        print("Entrada inválida. Intente nuevamente.")


def mostrar_clientes(lista):
    if lista:
        for cliente in lista:
            print(cliente)
    else:
        print("No hay clientes para mostrar.")


def crear_pedido(lista_pedidos, lista_productos, lista_clientes):
    codigo = int(input("Ingrese el código del pedido: "))

    # Verificar si el código es válido y no está en uso
    codigo_duplicado = False
    for pedido in lista_pedidos:
        if pedido.codigo_de_pedido == codigo:
            codigo_duplicado = True
            break

    if codigo <= 0 or codigo_duplicado:
        print("El código de pedido ya está en uso.")
        return

    dni_cliente = int(input("Ingrese el DNI del cliente: "))
    cliente = None
    for c in lista_clientes:
        if c.dni == dni_cliente:
            cliente = c
            break

    if not cliente:
        print("Cliente no encontrado.")
        return

    fecha = input("Ingrese fecha del pedido (dd/mm/aaaa): ")
    cargos_extras = float(input("Ingrese los cargos extras: "))

    print("Seleccione los productos del pedido (ingrese '0' para finalizar):")
    productos_seleccionados = []
    while True:
        mostrar_productos(lista_productos)
        codigo_producto = int(input("Ingrese el código del producto: "))
        if codigo_producto == 0:
            break

        producto = None
        for p in lista_productos:
            if p.codigo == codigo_producto:
                producto = p
                break

        if producto:
            productos_seleccionados.append(producto)
        else:
            print("Producto no encontrado.")

    pedido = Pedido(codigo, productos_seleccionados, cliente, fecha, cargos_extras)
    lista_pedidos.append(pedido)
    print("Pedido agregado correctamente.")


def mostrar_pedidos(lista):
    if lista:
        for pedido in lista:
            total = pedido.calcular_total()
            print(f"Código de Pedido: {pedido.codigo_de_pedido}, Cliente: {
                  pedido.cliente.nombre_y_apellido}, Total: ${total:.2f}")
    else:
        print("No hay pedidos para mostrar.")


def actualizar_producto(lista):
    codigo = int(input("Ingrese el códig de producto a actuazilar: "))
    for producto in lista:
        if producto.codigo == codigo:
            producto.nombre = input(
                "Ingrese el nuevo nombre del producto qeu desea actualizar: "
            )
            producto.precio = float(
                input("Ingrese el nuevo precio del producto que desea actualizar: ")
            )
            print("Producto actualizado.")
            return
    print("El producto no ha encontrado.")


def eliminar_producto(lista):
    codigo = int(input("Ingrese el código del producto a eliminar: "))
    for producto in lista:
        if producto.codigo == codigo:
            lista.remove(producto)
            print("Producto eliminado.")
            return
    print("Eñ producto no se ha encontrado.")


# Funciones de ordenamiento
def mezclar_con_mersort_de_total(lista, inicio, medio, fin):
    izquierda = lista[inicio : medio + 1]
    derecha = lista[medio + 1 : fin + 1]
    i = j = 0
    k = inicio

    while i < len(izquierda) and j < len(derecha):
        if izquierda[i].calcular_total() <= derecha[j].calcular_total():
            lista[k] = izquierda[i]
            i += 1
        else:
            lista[k] = derecha[j]
            j += 1
        k += 1

    while i < len(izquierda):
        lista[k] = izquierda[i]
        i += 1
        k += 1

    while j < len(derecha):
        lista[k] = derecha[j]
        j += 1
        k += 1


def merge_sort_por_importe_total(lista, inicio, fin):
    if inicio < fin:
        medio = (inicio + fin) // 2
        merge_sort_por_importe_total(lista, inicio, medio)
        merge_sort_por_importe_total(lista, medio + 1, fin)

        mezclar_con_mersort_de_total(lista, inicio, medio, fin)


# Menú principal
#


def menu():
    productos = cargar_datos("productos.bin")
    clientes = cargar_datos("clientes.bin")
    pedidos = cargar_datos("pedidos.bin")

    while True:
        print("\n1. Gestión de productos")
        print("2. Gestión de clientes")
        print("3. Gestión de pedidos")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            while True:
                print("\n--- Gestión de Productos ---")
                print("1. Crear producto")
                print("2. Mostrar productos")
                print("3. Actualizar producto")
                print("4. Eliminar producto")
                print("5. Volver al menú principal")

                opcion_producto = input("Seleccione una opción: ")

                if opcion_producto == "1":
                    crear_producto(productos)
                    guardar_datos("productos.bin", productos)
                elif opcion_producto == "2":
                    mostrar_productos(productos)
                elif opcion_producto == "3":
                    actualizar_producto(productos)
                    guardar_datos("productos.bin", productos)
                elif opcion_producto == "4":
                    eliminar_producto(productos)
                    guardar_datos("productos.bin", productos)
                elif opcion_producto == "5":
                    break
                else:
                    print("Opción no válida.")

        elif opcion == "4":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu()
