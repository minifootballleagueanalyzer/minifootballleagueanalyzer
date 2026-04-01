🇪🇸 [Español](README.md) | 🇬🇧 [English](README_EN.md)
---

# Mini Football League Analyzer - Frontend

Esta es la capa de visualización de datos de Mini Football League Analyzer.

## 🚀 Arquitectura: Astro + React (Islands Architecture)

El frontend utiliza un modelo de **Generación de Sitios Estáticos (SSG)** con **Hidratación Parcial**. Este enfoque permite que la página cargue de forma casi instantánea, a la vez que mantiene la interactividad compleja necesaria para los análisis estadísticos.

### 🛠️ Tecnologías Core
- **Framework**: [Astro 5](https://astro.build/)
- **UI Library**: [React 19](https://react.dev/)
- **Animaciones**: [Framer Motion](https://www.framer.com/motion/)
- **Gráficos**: [Chart.js](https://www.chartjs.org/) con `react-chartjs-2`
- **Iconos**: [Lucide React](https://lucide.dev/)

### 📐 Flujo de la Aplicación

1.  **Renderizado en Tiempo de Build (SSG)**:
    - Durante el proceso de construcción (`npm run build`), Astro ejecuta el código definido en `src/pages/index.astro`.
    - Se realiza un `fetch` a los datos procesados en `elo_rankings.json` (alojados en el propio repositorio).
    - Se genera un archivo HTML estático puro que ya contiene los datos del ranking impresos, mejorando drásticamente el SEO y eliminando los tiempos de carga (_Loading states_).

2.  **Arquitectura de Islas**:
    - Los componentes que requieren alta interactividad (como el Dashboard de comparativa H2H o el Chatbot IA) se cargan como "islas" independientes.
    - Utilizamos la directiva `client:load` para que Astro únicamente descargue e hidrate el JavaScript de React estrictamente necesario para dichos componentes, manteniendo el resto de la interfaz como un HTML ultra-ligero.

3.  **Flujo de Datos Automatizado**:
    - **Backend (Python)**: Realiza el scraping nocturno y genera el JSON actualizado de rankings.
    - **GitHub Actions**: Hace commit y push automático del JSON al repositorio.
    - **Vercel Build**: Detecta el nuevo commit en el repositorio, lanza el build de Astro (que consume los últimos datos JSON) y despliega la nueva versión completamente estática.

## 📁 Estructura del Proyecto

```text
frontend/
├── public/              # Assets estáticos y JSONs generados por el backend
├── src/
│   ├── components/      # Islas de React (Home, Leaderboard, MatrixChart, Chatbot)
│   ├── layouts/         # Plantillas base en formato .astro
│   ├── pages/           # Rutas del sitio web (.astro)
│   └── assets/          # Imágenes y recursos procesados optimizadamente por Vite
├── astro.config.mjs     # Configuración central de Astro e integraciones
└── package.json         # Dependencias y scripts del proyecto
```

## 🛠️ Scripts Disponibles

Ejecuta los siguientes comandos siempre desde el directorio `frontend/`:

| Comando | Descripción |
| :--- | :--- |
| `npm install` | Instala todas las dependencias necesarias. |
| `npm run dev` | Arranca el servidor de desarrollo local (Astro dev). |
| `npm run build` | Construye y compila la versión estática de producción en `dist/`. |
| `npm run preview` | Previsualiza localmente el build de producción generado. |

## 🌐 Despliegue

La plataforma está configurada para desplegarse automáticamente en **Vercel** tras cada integración en la rama principal (`main`). Para ello, Vercel lee las reglas definidas en el archivo `vercel.json` de la raíz del proyecto, orquestando el build específicamente para esta subcarpeta `frontend/`.
