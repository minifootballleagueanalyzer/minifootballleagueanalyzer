# elo_system.py

# --- EL SISTEMA ELO CENTRALIZADO ---
class SistemaElo:
    def __init__(self, k_factor=32):
        self.k_factor = k_factor
        self.ratings = {}

    def obtener_elo(self, equipo):
        return self.ratings.get(equipo, 1500)  # Todos empiezan con 1500 puntos

    # Calcula la probabilidad estadística (entre 0.0 y 1.0) de que A le gane a B basándose en sus puntos actuales (ra y rb)
    def probabilidad_esperada(self, rating_a, rating_b):
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400)) # fórmula matemática ELO

    # Esta función se ejecuta después de que el partido ha terminado.
    # Su trabajo es comparar lo que se esperaba que pasara con lo que realmente pasó, y repartir o quitar puntos en consecuencia.
    def actualizar_ratings(self, equipo_local, equipo_visitante, goles_local, goles_visitante, jornada):

        total_jornadas = 8

        ra = self.obtener_elo(equipo_local)
        rb = self.obtener_elo(equipo_visitante)

        ea = self.probabilidad_esperada(ra, rb)
        eb = self.probabilidad_esperada(rb, ra)

        # 1. Determinar quién gana (sa, sb) y calcular la Diferencia de Goles absoluta
        diferencia_goles = abs(goles_local - goles_visitante)

        if goles_local > goles_visitante:
            sa, sb = 1, 0
        elif goles_local == goles_visitante:
            sa, sb = 0.5, 0.5
            diferencia_goles = 0  # En empate no hay margen
        else:
            sa, sb = 0, 1

        # 2. Multiplicador K por Margen de Victoria (Goleada)
        if diferencia_goles == 0:
            k_goles = 1.0
        else:
            k_goles = 1 + 0.5 * (diferencia_goles ** 0.5)

        # 3. Multiplicador K por Degradación Temporal (Time-Decay)
        k_tiempo = 0.5 + (jornada / total_jornadas) * 0.5

        # 4. Calculamos la K final del partido combinando todo
        k_partido = self.k_factor * k_goles * k_tiempo

        # 5. Actualizamos puntuaciones (Usando la k_partido adaptada)
        self.ratings[equipo_local] = ra + k_partido * (sa - ea)
        self.ratings[equipo_visitante] = rb + k_partido * (sb - eb)
