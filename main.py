from modelos import Habitacion, ReservaHotel, ReservaSuite

# Instanciación: 3 habitaciones (componentes), 1 reserva base y 2 suites
hab1 = Habitacion(204, "Estándar")
hab2 = Habitacion(310, "Suite")
hab3 = Habitacion(501, "Suite")

reserva1 = ReservaHotel("Sofía Ramírez", hab1, 3, 800)
suite1 = ReservaSuite("Diego Mendoza", hab2, 2, 1800, personas=2, desayuno_incluido=True)
suite2 = ReservaSuite("Laura Núñez", hab3, 4, 2500, personas=3)

print("\nResumen inicial (polimorfismo: cada objeto usa su propio mostrar_resumen):")
for reserva in (reserva1, suite1, suite2):
    reserva.mostrar_resumen()

# Pruebas de composición
print("\nPruebas de composición:")
print(f"Método del objeto contenido, vía la reserva: {suite1.habitacion.descripcion()}")

# Pruebas de encapsulamiento
print("\nPruebas de encapsulamiento:")
print(f"Costo por noche consultado con el getter: ${reserva1.costo_por_noche:.2f}")
reserva1.costo_por_noche = 900  # setter con valor válido
print(f"Costo actualizado con el setter: ${reserva1.costo_por_noche:.2f}")
try:
    reserva1.costo_por_noche = -50  # el setter rechaza valores negativos
except ValueError as error:
    print(f"Restricción activa -> {error}")
try:
    reserva1.pagado = True  # propiedad de solo lectura
except AttributeError:
    print("No se puede modificar 'pagado' directamente; usa registrar_pago().")

# Pruebas de herencia y sobrescritura
print("\nPruebas de herencia y método sobrescrito:")
suite1.extender_estadia(1)    # método heredado
suite1.contratar_spa()        # método propio de la subclase
suite1.aplicar_descuento(10)  # método heredado
suite1.registrar_pago()       # usa calcular_total() sobrescrito
