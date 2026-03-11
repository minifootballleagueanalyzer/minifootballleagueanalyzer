Proyecto que aplica análisis de datos de fútbol de MiniFootballLeague España (https://minifootballleagues.com/). 
Extráe información de las competiciones mediante scraping web y muestra infografías útiles que permiten a los equipos estudiar a sus rivales.

Las infografías se actualizan diariamente.

La web muestra un menú desplegable permitiendo escoger la competición. Cada competición incluye:
- Clasificación ELO de los equipos -> Clasifican por estado de forma en el que llegan, no por puntos
- Tabla de cuotas de los encuentros de la próxima jornada 

Se incluyen las siguientes competiciones de F7:
- Primera División Murcia (prim_div_mur.json)
- Segunda División A Murcia (seg_div_murA.json)
- Segunda División B Murcia (seg_div_murB.json)
- Tercera División A Murcia (ter_div_murA.json)
- Tercera División B Murcia (ter_div_murB.json)
- Cuarta División Murcia (cuar_div_mur.json)

La web también muestra un menú desplegable permitiendo escoger dos equipo dentro de cada competición. Para cada pareja de equipos se incluirá:
- Tabla de cuotas (resultados más probables, porcentajes y xG)
- Evolución de ELO desde el comienzo de la liga de ambos equipos
- Gráfico de radar con:
  -   Poder Ofensivo -> Capacidad bruta de anotación.
  - Solidez Defensiva	-> Capacidad para evitar goles.
  - Fair Play	-> Nivel de disciplina (puntuas más si tienes menos tarjetas).
  - Reparto del Gol	100% ->	Si el valor es alto, el equipo no depende de un solo hombre.
  - Diferencia de Gol -> El balance general de competitividad.
