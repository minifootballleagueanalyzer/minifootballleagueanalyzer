import json
import matplotlib.pyplot as plt


# --- 1. EL SISTEMA ELO (Idéntico a tu motor principal) ---
class SistemaElo:
    def __init__(self, k_factor=32):
        self.k_factor = k_factor
        self.ratings = {}

    def obtener_elo(self, equipo):
        return self.ratings.get(equipo, 1500)

    def probabilidad_esperada(self, rating_a, rating_b):
        return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

    def actualizar_ratings(self, equipo_local, equipo_visitante, goles_local, goles_visitante, jornada):
        ra = self.obtener_elo(equipo_local)
        rb = self.obtener_elo(equipo_visitante)

        ea = self.probabilidad_esperada(ra, rb)
        eb = self.probabilidad_esperada(rb, ra)

        diferencia_goles = abs(goles_local - goles_visitante)

        if goles_local > goles_visitante:
            sa, sb = 1, 0
        elif goles_local == goles_visitante:
            sa, sb = 0.5, 0.5
            diferencia_goles = 0
        else:
            sa, sb = 0, 1

        if diferencia_goles == 0:
            k_goles = 1.0
        else:
            k_goles = 1 + 0.5 * (diferencia_goles ** 0.5)

        k_tiempo = 0.5 + (jornada / 8) * 0.5
        k_partido = self.k_factor * k_goles * k_tiempo

        self.ratings[equipo_local] = ra + k_partido * (sa - ea)
        self.ratings[equipo_visitante] = rb + k_partido * (sb - eb)


# --- 2. CARGAR DATOS Y RECOPILAR HISTORIAL ---
print("Cargando JSON y calculando la evolución histórica...")
try:
    with open('resultados_liga.json', 'r', encoding='utf-8') as f:
        partidos = json.load(f)
except FileNotFoundError:
    print("Error: No se encuentra 'resultados_liga.json'.")
    exit()

elo_liga = SistemaElo()

# Listas para guardar el historial. Empiezan en 1500 (Jornada 0)
historial_toca = [1500]
historial_afed = [1500]
historial_riomar = [1500]  # NUEVO
historial_gallos = [1500]  # NUEVO

# Procesamos los partidos agrupándolos jornada a jornada (del 1 al 8)
for j in range(1, 9):
    partidos_jornada = [p for p in partidos if p.get('jornada') == j]

    for partido in partidos_jornada:
        elo_liga.actualizar_ratings(
            partido['equipo_local'],
            partido['equipo_visitante'],
            partido['goles_local'],
            partido['goles_visitante'],
            partido['jornada']
        )

    # Al terminar la jornada, "tomamos una foto" del Elo del Top 4
    historial_toca.append(elo_liga.obtener_elo("C.D Tocapelotas"))
    historial_afed.append(elo_liga.obtener_elo("Afed Fc"))
    historial_riomar.append(elo_liga.obtener_elo("Riomar Fc"))  # NUEVO
    historial_gallos.append(elo_liga.obtener_elo("Los Gallos Fc"))  # NUEVO

# --- 3. CREAR EL GRÁFICO VISUAL ---
print("Generando gráfico...")
jornadas_x = list(range(0, 9))

# Configuramos el lienzo un poco más ancho
plt.figure(figsize=(11, 7))

# Dibujamos las líneas de los líderes (Gruesas y zorder alto para que salgan por encima)
plt.plot(jornadas_x, historial_toca, marker='o', linewidth=3.0, label='1º C.D Tocapelotas', color='#D62828', zorder=5)
plt.plot(jornadas_x, historial_afed, marker='s', linewidth=3.0, label='2º Afed Fc', color='#003049', zorder=5)

# Dibujamos las líneas de los perseguidores (Más finas, colores distintos y algo de transparencia)
plt.plot(jornadas_x, historial_riomar, marker='^', linewidth=2.0, label='3º Riomar Fc', color='#4CAF50', alpha=0.8,
         zorder=4)
plt.plot(jornadas_x, historial_gallos, marker='D', linewidth=2.0, label='4º Los Gallos Fc', color='#FF9800', alpha=0.8,
         zorder=4)

# Detalles estéticos
plt.title('Evolución del Estado de Forma (Elo) - Top 4 de la Liga', fontsize=14, fontweight='bold')
plt.xlabel('Jornada Disputada', fontsize=12)
plt.ylabel('Puntuación Elo', fontsize=12)
plt.xticks(jornadas_x)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=11, loc='upper left')

# Añadimos los puntos exactos al final de cada línea (ajustados a la derecha para que no se pisen)
plt.annotate(f"{historial_toca[-1]:.0f}", (8, historial_toca[-1]), textcoords="offset points", xytext=(8, 0), ha='left',
             va='center', color='#D62828', fontweight='bold')
plt.annotate(f"{historial_afed[-1]:.0f}", (8, historial_afed[-1]), textcoords="offset points", xytext=(8, 0), ha='left',
             va='center', color='#003049', fontweight='bold')
plt.annotate(f"{historial_riomar[-1]:.0f}", (8, historial_riomar[-1]), textcoords="offset points", xytext=(8, 0),
             ha='left', va='center', color='#4CAF50', fontweight='bold')
plt.annotate(f"{historial_gallos[-1]:.0f}", (8, historial_gallos[-1]), textcoords="offset points", xytext=(8, 0),
             ha='left', va='center', color='#FF9800', fontweight='bold')

plt.tight_layout()

# Ajustamos los márgenes para que los números finales no se salgan del gráfico
plt.subplots_adjust(right=0.92)

plt.show()