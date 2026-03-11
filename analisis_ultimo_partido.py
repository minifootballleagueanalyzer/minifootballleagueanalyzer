import json
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# --- 1. MOTOR ELO (Reutilizado y optimizado) ---
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
            sa, sb = 0.5, 0.5; diferencia_goles = 0
        else:
            sa, sb = 0, 1

        k_goles = 1.0 if diferencia_goles == 0 else 1 + 0.5 * (diferencia_goles ** 0.5)
        k_tiempo = 0.5 + (jornada / 8) * 0.5
        k_partido = self.k_factor * k_goles * k_tiempo

        self.ratings[equipo_local] = ra + k_partido * (sa - ea)
        self.ratings[equipo_visitante] = rb + k_partido * (sb - eb)


# --- 2. CARGA DE DATOS Y CÁLCULO DE xG ---
print("Cargando datos y calculando métricas ELO...")
elo_liga = SistemaElo()

try:
    with open('resultados_liga.json', 'r', encoding='utf-8') as f:
        partidos = json.load(f)
        for partido in partidos:
            elo_liga.actualizar_ratings(partido['equipo_local'], partido['equipo_visitante'],
                                        partido['goles_local'], partido['goles_visitante'], partido['jornada'])
except FileNotFoundError:
    print("Error: No se encuentra 'resultados_liga.json'.")
    exit()

# Definimos el partido
equipo_home = "C.D Tocapelotas"
equipo_away = "Los Gallos Fc"

elo_home = elo_liga.obtener_elo(equipo_home)
elo_away = elo_liga.obtener_elo(equipo_away)
prob_base_home = elo_liga.probabilidad_esperada(elo_home, elo_away)
prob_base_away = elo_liga.probabilidad_esperada(elo_away, elo_home)

goles_esperados_total = 5.0
xg_home = goles_esperados_total * prob_base_home
xg_away = goles_esperados_total * prob_base_away

# --- 3. CÁLCULO DE LA MATRIZ DE POISSON ---
max_goles = 7  # Calculamos hasta el 6-6
resultados = []
prob_total_home = 0
prob_total_draw = 0
prob_total_away = 0

for h in range(max_goles):
    for a in range(max_goles):
        prob_h = (math.exp(-xg_home) * (xg_home ** h)) / math.factorial(h)
        prob_a = (math.exp(-xg_away) * (xg_away ** a)) / math.factorial(a)
        prob_conjunta = prob_h * prob_a * 100  # En porcentaje

        # Clasificamos el resultado
        if h > a:
            prob_total_home += prob_conjunta
        elif h == a:
            prob_total_draw += prob_conjunta
        else:
            prob_total_away += prob_conjunta

        resultados.append({'h': h, 'a': a, 'prob': prob_conjunta})

# --- 4. DIBUJO DEL GRÁFICO (Estilo Dark UI) ---
print("Generando el panel de cuotas visual...")
# Colores estilo casa de apuestas oscura
bg_color = '#121212'
text_color = '#FFFFFF'
home_color = '#1B5E20'  # Verde oscuro
draw_color = '#424242'  # Gris oscuro
away_color = '#01579B'  # Azul oscuro
box_border = '#333333'

fig, ax = plt.subplots(figsize=(12, 9), facecolor=bg_color)
ax.set_facecolor(bg_color)

# Dibujamos las cajas de resultados
box_size = 0.85
for res in resultados:
    h, a, prob = res['h'], res['a'], res['prob']

    # Ignorar probabilidades ínfimas (<0.1%) para limpiar el gráfico
    if prob < 0.1 and h > 3 and a > 3: continue

    # Lógica Geométrica para la "Escalera"
    if h > a:
        y = h - a
        x = a
        color_caja = home_color
    elif h == a:
        y = 0
        x = h
        color_caja = draw_color
    else:
        y = h - a  # Será negativo
        x = h
        color_caja = away_color

    # Definimos colores de texto por defecto
    color_texto_marcador = text_color
    color_texto_prob = '#B0BEC5'

    # --- NUEVO: DESTACAR EL 3-2 EN DORADO ---
    if h == 3 and a == 2:
        color_caja = '#FFD700'  # Fondo dorado vibrante
        color_texto_marcador = '#000000'  # Texto en negro para que lea bien
        color_texto_prob = '#333333'  # Gris oscuro para el porcentaje

    # Dibujar el rectángulo
    # (Le subimos un poco el 'alpha' de 0.8 a 0.9 para que el dorado sea más sólido)
    rect = patches.Rectangle((x - box_size / 2, y - box_size / 2), box_size, box_size,
                             linewidth=1, edgecolor=box_border, facecolor=color_caja, alpha=0.9)
    ax.add_patch(rect)

    # Texto: Marcador
    ax.text(x, y + 0.15, f"{h}-{a}", color=color_texto_marcador, ha='center', va='center', fontsize=11,
            fontweight='bold')

    # Texto: Probabilidad
    prob_text = f"<0.1%" if prob < 0.1 else f"{prob:.1f}%"
    ax.text(x, y - 0.2, prob_text, color=color_texto_prob, ha='center', va='center', fontsize=9)

# --- PANEL LATERAL DERECHO (Resumen de Probabilidades) ---
panel_x = 7
ancho_panel = 3.5


# Función para dibujar paneles resumen
def dibujar_panel_resumen(y_pos, titulo, prob, color, xg_val=None, equipo=None):
    rect = patches.Rectangle((panel_x, y_pos), ancho_panel, 1.8,
                             linewidth=2, edgecolor=color, facecolor=bg_color, alpha=0.9, zorder=3)
    ax.add_patch(rect)
    ax.text(panel_x + ancho_panel / 2, y_pos + 1.3, f"{prob:.1f}%", color=color, ha='center', va='center', fontsize=18,
            fontweight='bold')
    ax.text(panel_x + ancho_panel / 2, y_pos + 0.9, titulo, color=text_color, ha='center', va='center', fontsize=10)

    if equipo:
        ax.text(panel_x + ancho_panel / 2, y_pos + 0.5, equipo, color='#B0BEC5', ha='center', va='center', fontsize=11,
                fontweight='bold')
    if xg_val is not None:
        ax.text(panel_x + ancho_panel / 2, y_pos + 0.2, f"{xg_val:.2f} xG", color='#4CAF50', ha='center', va='center',
                fontsize=10)


# Dibujamos los 3 paneles
dibujar_panel_resumen(2.5, "PROBABILIDAD DE VICTORIA", prob_total_home, '#4CAF50', xg_home, equipo_home)
dibujar_panel_resumen(0, "EMPATE", prob_total_draw, '#9E9E9E')
dibujar_panel_resumen(-2.5, "PROBABILIDAD DE VICTORIA", prob_total_away, '#29B6F6', xg_away, equipo_away)

# Títulos generales
ax.text(0, 6.5, "RESULTADOS POSIBLES", color=text_color, fontsize=16, fontweight='bold', ha='left')
ax.text(2.5, 5.5, "PROBABILIDAD DE CADA RESULTADO EXACTO", color='#B0BEC5', fontsize=11, ha='center')

# Ajustes de la ventana
ax.set_xlim(-1, 11)
ax.set_ylim(-6.5, 7.5)
ax.set_aspect('equal')  # Mantiene los cuadrados perfectos
ax.axis('off')  # Ocultar ejes

plt.tight_layout()
plt.savefig('matriz_cuotas.png', dpi=300, bbox_inches='tight', facecolor=bg_color)
print("¡Listo! Revisa la imagen 'matriz_cuotas.png' en tu carpeta.")