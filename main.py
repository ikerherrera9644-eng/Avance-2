"""
Sistema de Reservas de Hotel

Una ReservaHotel representa la estadía de un huésped (nombre, habitación,
noches, costo por noche y estado de pago). La subclase ReservaSuite modela
una reserva de suite con atributos propios (personas, desayuno incluido y
spa) y un cálculo de total diferente.
"""


# ==========================================
# Creación de la clase base
# ==========================================
class ReservaHotel:
    def __init__(self, huesped, numero_habitacion, noches, costo_por_noche):
        self.huesped = huesped
        self.numero_habitacion = numero_habitacion
        self.noches = noches
        # Aplicación de Encapsulamiento: se asigna mediante el setter (valida el valor)
        self.costo_por_noche = costo_por_noche
        # Atributo protegido: solo debe modificarse desde la clase o sus subclases
        self._pagado = False

    # ------------------------------------------
    # Aplicación de Encapsulamiento (atributo privado + @property)
    # ------------------------------------------
    @property
    def costo_por_noche(self):
        # Getter: consulta controlada del atributo privado
        return self.__costo_por_noche

    @costo_por_noche.setter
    def costo_por_noche(self, valor):
        # Setter: valida que el costo sea un número positivo
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError(f"Costo por noche inválido: {valor}. Debe ser un número mayor a 0.")
        self.__costo_por_noche = valor  # Atributo privado (name mangling)

    @property
    def pagado(self):
        # Solo lectura: el estado de pago se cambia únicamente con registrar_pago()
        return self._pagado

    # ------------------------------------------
    # Métodos operativos de la clase base
    # ------------------------------------------
    def extender_estadia(self, noches_extra):
        if noches_extra <= 0:
            print(f"No se puede extender la reserva de {self.huesped} con un valor inválido.")
        else:
            self.noches += noches_extra
            print(f"{self.huesped} extendió su estadía {noches_extra} noches. Total: {self.noches} noches.")

    def aplicar_descuento(self, porcentaje):
        # Se usa el setter, por lo que la validación también aplica aquí
        self.costo_por_noche = self.costo_por_noche * (1 - porcentaje / 100)
        print(f"Se aplicó {porcentaje}% de descuento a la reserva de {self.huesped}. "
              f"Nuevo costo por noche: ${self.costo_por_noche:.2f}.")

    def registrar_pago(self):
        if self._pagado:
            print(f"La reserva de {self.huesped} ya estaba pagada.")
        else:
            self._pagado = True
            print(f"Se registró el pago de {self.huesped} por ${self.calcular_total():.2f}.")

    def calcular_total(self):
        return self.noches * self.costo_por_noche

    def mostrar_resumen(self):
        estado_pago = "Pagada" if self._pagado else "Pendiente de pago"
        print(f"--- Reserva de {self.huesped} (Habitación {self.numero_habitacion}) ---")
        print(f"Noches: {self.noches} | Costo por noche: ${self.costo_por_noche:.2f} | "
              f"Total: ${self.calcular_total():.2f} | Estado: {estado_pago}")


# ==========================================
# Uso de super() y Herencia
# ==========================================
class ReservaSuite(ReservaHotel):
    COSTO_DESAYUNO = 150  # por persona, por noche
    COSTO_SPA = 500       # cargo único

    def __init__(self, huesped, numero_habitacion, noches, costo_por_noche,
                 personas, desayuno_incluido=False):
        # super() reutiliza los atributos de la superclase
        super().__init__(huesped, numero_habitacion, noches, costo_por_noche)
        # Atributos nuevos propios de la subclase
        self.personas = personas
        self.desayuno_incluido = desayuno_incluido
        self._spa_contratado = False  # Atributo protegido

    # Método propio de la subclase
    def contratar_spa(self):
        if self._spa_contratado:
            print(f"{self.huesped} ya tiene el spa contratado.")
        else:
            self._spa_contratado = True
            print(f"{self.huesped} contrató el spa (+${self.COSTO_SPA:.2f}).")

    # ------------------------------------------
    # Sobrescritura de métodos (Polimorfismo)
    # ------------------------------------------
    def calcular_total(self):
        total = super().calcular_total()  # reutiliza el cálculo de la base
        if self.desayuno_incluido:
            total += self.COSTO_DESAYUNO * self.personas * self.noches
        if self._spa_contratado:
            total += self.COSTO_SPA
        return total

    def mostrar_resumen(self):
        estado_pago = "Pagada" if self._pagado else "Pendiente de pago"
        desayuno = "Sí" if self.desayuno_incluido else "No"
        spa = "Sí" if self._spa_contratado else "No"
        print(f"=== SUITE de {self.huesped} (Habitación {self.numero_habitacion}) ===")
        print(f"Noches: {self.noches} | Personas: {self.personas} | "
              f"Costo por noche: ${self.costo_por_noche:.2f}")
        print(f"Desayuno: {desayuno} | Spa: {spa} | "
              f"Total: ${self.calcular_total():.2f} | Estado: {estado_pago}")


# ==========================================
# Instanciación y pruebas
# ==========================================
if __name__ == "__main__":
    # 1 objeto de la clase base y 2 de la subclase
    reserva1 = ReservaHotel("Sofía Ramírez", 204, 3, 800)
    suite1 = ReservaSuite("Diego Mendoza", 310, 2, 1800, personas=2, desayuno_incluido=True)
    suite2 = ReservaSuite("Laura Núñez", 501, 4, 2500, personas=3)

    print("\nResumen inicial (polimorfismo: cada objeto usa su propio mostrar_resumen):")
    for reserva in (reserva1, suite1, suite2):
        reserva.mostrar_resumen()

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
    suite1.extender_estadia(1)   # método heredado
    suite1.contratar_spa()       # método propio de la subclase
    suite1.aplicar_descuento(10) # método heredado
    suite1.registrar_pago()      # usa calcular_total() sobrescrito

    # Independencia de datos entre instancias (self)
    print("\nIndependencia de datos entre instancias:")
    reserva1.aplicar_descuento(15)
    suite2.registrar_pago()
    suite2.registrar_pago()

    print("\nResumen final:")
    for reserva in (reserva1, suite1, suite2):
        reserva.mostrar_resumen()