import json
import numpy as np
import time

# --- 1. EL SISTEMA ELO ---
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
    # Añadimos 'jornada' como parámetro
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


# --- 2. CARGAR DATOS Y CALCULAR EL RANKING ELO ---
print("Cargando resultados y calculando el Power Ranking (Elo)...")
elo_liga = SistemaElo()

try:
    with open('resultados_liga.json', 'r', encoding='utf-8') as f:
        partidos = json.load(f)

        for partido in partidos:
            elo_liga.actualizar_ratings(
                partido['equipo_local'],
                partido['equipo_visitante'],
                partido['goles_local'],
                partido['goles_visitante'],
                partido['jornada']  # <-- ¡AÑADIDO!
            )

except FileNotFoundError:
    print("Error: No se encuentra 'resultados_liga.json'. Asegúrate de que está en la misma carpeta.")
    exit()



print("\n--- RANKING ELO (Tras 8 Jornadas) ---")
ranking_ordenado = sorted(elo_liga.ratings.items(), key=lambda x: x[1], reverse=True)
for i, (equipo, rating) in enumerate(ranking_ordenado):
    print(f"{i + 1}. {equipo}: {rating:.0f} pts")
print("-------------------------------------\n")

# --- 3. SIMULACIÓN DE LA ÚLTIMA JORNADA ---
rival_de_toca = "Los Gallos Fc"
rival_de_afed = "Ud Las Piscinas"

print(f"Preparando simulación basada en sistema ELO...")

def simular_goles_por_elo(equipo_a, equipo_b):

    """Calcula los goles esperados basándose en la diferencia de Elo"""
    elo_a = elo_liga.obtener_elo(equipo_a)
    elo_b = elo_liga.obtener_elo(equipo_b)

    # Probabilidad base del Elo
    prob_a = elo_liga.probabilidad_esperada(elo_a, elo_b)
    prob_b = elo_liga.probabilidad_esperada(elo_b, elo_a)

    # Asumimos una media de 5 goles por partido en total en esta liga (basado en la tabla)
    goles_esperados_total = 5.0

    # Distribuimos los goles esperados según su probabilidad de victoria
    lambda_a = goles_esperados_total * prob_a
    lambda_b = goles_esperados_total * prob_b

    return np.random.poisson(lambda_a), np.random.poisson(lambda_b)


def calcular_xG(equipo_a, equipo_b):
    """Calcula los Expected Goals (xG) teóricos basados en Elo"""
    elo_a = elo_liga.obtener_elo(equipo_a)
    elo_b = elo_liga.obtener_elo(equipo_b)

    prob_a = elo_liga.probabilidad_esperada(elo_a, elo_b)
    prob_b = elo_liga.probabilidad_esperada(elo_b, elo_a)

    # Asumimos una media de 5 goles por partido en total en esta liga
    goles_esperados_total = 5.0

    xg_a = goles_esperados_total * prob_a
    xg_b = goles_esperados_total * prob_b
    return xg_a, xg_b


# Calculamos e imprimimos los xG antes de simular
xg_toca, xg_rival_toca = calcular_xG("C.D Tocapelotas", rival_de_toca)
xg_afed, xg_rival_afed = calcular_xG("Afed Fc", rival_de_afed)

print("\n--- EXPECTED GOALS (xG) PARA LA ÚLTIMA JORNADA ---")
print(f"C.D Tocapelotas {xg_toca:.2f} - {xg_rival_toca:.2f} {rival_de_toca}")
print(f"Afed Fc         {xg_afed:.2f} - {xg_rival_afed:.2f} {rival_de_afed}")


"""
# --- PREDICCIÓN DE MARCADORES EXACTOS (POISSON) ---
print("\n--- PREDICCIÓN DE MARCADORES EXACTOS (C.D Tocapelotas) ---")

def probabilidad_marcador(xg_local, xg_visitante, max_goles=10):
    probabilidades = []
    # Calculamos una matriz de resultados posibles desde el 0-0 hasta el 9-9
    for goles_loc in range(max_goles):
        for goles_vis in range(max_goles):
            # Fórmula de Poisson: P(k) = (e^(-λ) * λ^k) / k!
            prob_loc = (math.exp(-xg_local) * (xg_local ** goles_loc)) / math.factorial(goles_loc)
            prob_vis = (math.exp(-xg_visitante) * (xg_visitante ** goles_vis)) / math.factorial(goles_vis)

            # La probabilidad conjunta es la multiplicación de ambas
            prob_conjunta = prob_loc * prob_vis

            probabilidades.append({
                "marcador": f"{goles_loc}-{goles_vis}",
                "probabilidad": prob_conjunta * 100  # Lo pasamos a porcentaje
            })
    return probabilidades


# Calculamos las probabilidades para el partido de Tocapelotas
probs_toca = probabilidad_marcador(xg_toca, xg_rival_toca)

# Ordenamos la lista de resultados de mayor a menor probabilidad
probs_toca_ordenadas = sorted(probs_toca, key=lambda x: x['probabilidad'], reverse=True)

# Imprimimos el Top 3
print(
    f"Resultado más probable para Tocapelotas: {probs_toca_ordenadas[0]['marcador']} ({probs_toca_ordenadas[0]['probabilidad']:.2f}% de probabilidad)")
print(
    f"Segundo más probable: {probs_toca_ordenadas[1]['marcador']} ({probs_toca_ordenadas[1]['probabilidad']:.2f}% de probabilidad)")
print(
    f"Tercer más probable: {probs_toca_ordenadas[2]['marcador']} ({probs_toca_ordenadas[2]['probabilidad']:.2f}% de probabilidad)")
"""

# --- 4. SIMULACIÓN MONTE CARLO ---
num_simulaciones = 1000000
veces_toca_campeon = 0
veces_afed_campeon = 0

print(f"\nIniciando {num_simulaciones} (1 millón) de simulaciones...")

# ¡ENCENDEMOS EL CRONÓMETRO!
inicio_simulacion = time.time()

for _ in range(num_simulaciones):

    # Puntos base (antes de la última jornada)
    # Ya no necesitamos las variables dg_toca y dg_afed (Diferencia de Goles)
    pts_toca = 19
    pts_afed = 19

    # Simulamos el partido de Tocapelotas
    goles_toca, goles_rival_toca = simular_goles_por_elo("C.D Tocapelotas", rival_de_toca)
    if goles_toca > goles_rival_toca:
        pts_toca += 3
    elif goles_toca == goles_rival_toca:
        pts_toca += 1

    # Simulamos el partido de Afed FC
    goles_afed, goles_rival_afed = simular_goles_por_elo("Afed Fc", rival_de_afed)
    if goles_afed > goles_rival_afed:
        pts_afed += 3
    elif goles_afed == goles_rival_afed:
        pts_afed += 1

    # --- NUEVA LÓGICA DE DESEMPATE (ENFRENTAMIENTO DIRECTO) ---
    if pts_toca > pts_afed:
        veces_toca_campeon += 1
    elif pts_afed > pts_toca:
        veces_afed_campeon += 1
    else:
        # EMPATE A PUNTOS: Gana siempre Tocapelotas por el enfrentamiento directo
        veces_toca_campeon += 1

# ¡APAGAMOS EL CRONÓMETRO!
fin_simulacion = time.time()

# Calculamos minutos y segundos
tiempo_total = fin_simulacion - inicio_simulacion
minutos = int(tiempo_total // 60)
segundos = tiempo_total % 60

print(f"Ran for {segundos:.2f} seconds")

# --- 4. RESULTADOS FINALES ---
prob_toca = (veces_toca_campeon / num_simulaciones) * 100
prob_afed = (veces_afed_campeon / num_simulaciones) * 100

print(f"\n--- RESULTADOS DE LA SIMULACIÓN ---")
print(f"Probabilidad de que C.D Tocapelotas gane la liga: {prob_toca:.2f}%")
print(f"Probabilidad de que Afed Fc gane la liga:         {prob_afed:.2f}%")