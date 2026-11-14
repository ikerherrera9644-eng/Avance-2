"""
Sistema de Reservas de Hotel - Módulo de modelos

Contiene la clase auxiliar Habitacion (composición), la clase base
ReservaHotel y la subclase ReservaSuite.
"""


# ==========================================
# Clase auxiliar para Composición
# ==========================================
class Habitacion:
    def __init__(self, numero, tipo):
        self.numero = numero
        self.tipo = tipo

    def descripcion(self):
        return f"Habitación {self.numero} ({self.tipo})"


# ==========================================
# Creación de la clase base
# ==========================================
class ReservaHotel:
    def __init__(self, huesped, habitacion, noches, costo_por_noche):
        self.huesped = huesped
        # Composición: una ReservaHotel "tiene-una" Habitacion
        self.habitacion = habitacion
        self.noches = noches
        # Aplicación de Encapsulamiento: se asigna mediante el setter (valida el valor)
        self.costo_por_noche = costo_por_noche
        # Atributo protegido: solo debe modificarse desde la clase o sus subclases
        self._pagado = False

    # ------------------------------------------
    # Aplicación de Encapsulamiento
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
        # Delegación: se invoca el método del objeto Habitacion contenido
        print(f"--- Reserva de {self.huesped} ({self.habitacion.descripcion()}) ---")
        print(f"Noches: {self.noches} | Costo por noche: ${self.costo_por_noche:.2f} | "
              f"Total: ${self.calcular_total():.2f} | Estado: {estado_pago}")


# ==========================================
# Uso de super() y Herencia
# ==========================================
class ReservaSuite(ReservaHotel):
    COSTO_DESAYUNO = 150  # por persona, por noche
    COSTO_SPA = 500       # cargo único

    def __init__(self, huesped, habitacion, noches, costo_por_noche,
                 personas, desayuno_incluido=False):
        # super() reutiliza los atributos de la superclase
        super().__init__(huesped, habitacion, noches, costo_por_noche)
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
        print(f"=== SUITE de {self.huesped} ({self.habitacion.descripcion()}) ===")
        print(f"Noches: {self.noches} | Personas: {self.personas} | "
              f"Costo por noche: ${self.costo_por_noche:.2f}")
        print(f"Desayuno: {desayuno} | Spa: {spa} | "
              f"Total: ${self.calcular_total():.2f} | Estado: {estado_pago}")
