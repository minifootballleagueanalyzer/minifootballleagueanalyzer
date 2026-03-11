
import json
import numpy as np
import time

# --- 3. SIMULACIÓN DE JORNADA ---
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
