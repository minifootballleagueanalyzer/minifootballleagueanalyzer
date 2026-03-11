
import json
import numpy as np
import time

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