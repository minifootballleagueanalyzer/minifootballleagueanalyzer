🇪🇸 [Español](README.md) | 🇬🇧 [English](README_EN.md)
---

# Mini Football League Analyzer - Frontend

This is the data visualization layer for the Mini Football League Analyzer.

## 🚀 Architecture: Astro + React (Islands Architecture)

The frontend uses a **Static Site Generation (SSG)** model with **Partial Hydration**. This architecture allows the page to load almost instantly while maintaining the complex interactivity required for statistical analysis.

### 🛠️ Core Technologies
- **Framework**: [Astro 5](https://astro.build/)
- **UI Library**: [React 19](https://react.dev/)
- **Animations**: [Framer Motion](https://www.framer.com/motion/)
- **Charts**: [Chart.js](https://www.chartjs.org/) with `react-chartjs-2`
- **Icons**: [Lucide React](https://lucide.dev/)

### 📐 Application Workflow

1. **Build Time Rendering (SSG)**:
   - During the build process (`npm run build`), Astro executes the code in `src/pages/index.astro`.
   - A `fetch` request retrieves the processed data from `elo_rankings.json` (hosted on GitHub).
   - A static HTML file is generated containing the pre-rendered ranking data, heavily improving SEO and eliminating "Loading" states.

2. **Islands Architecture**:
   - Highly interactive components (such as the H2H dashboard or the AI Chatbot) are loaded as isolated "island" components.
   - We use the `client:load` directive so Astro only downloads the essential React JavaScript for those specific components, keeping the rest of the page as lightweight HTML.

3. **Data Flow**:
   - **Backend (Python)**: Executes the nightly scraping and generates the rankings JSON.
   - **GitHub Actions**: Commits and pushes the JSON back to the repository.
   - **Vercel Build**: Detects the changes, triggers the Astro build, consumes the updated JSON, and deploys the new static version of the site.

## 📁 Project Structure

```text
frontend/
├── public/              # Static assets and backend-generated JSONs
├── src/
│   ├── components/      # React Islands (Home, Leaderboard, MatrixChart, etc.)
│   ├── layouts/         # Base layout templates (.astro)
│   ├── pages/           # Site routes (.astro)
│   └── assets/          # Vite-processed images and resources
├── astro.config.mjs     # Astro and React integration configuration
└── package.json         # Dependencies and NPM scripts
```

## 🛠️ Available Scripts

From the `frontend/` directory, you can run:

| Command | Description |
| :--- | :--- |
| `npm install` | Installs all project dependencies. |
| `npm run dev` | Starts the local development server (Astro). |
| `npm run build` | Builds the static production site into `dist/`. |
| `npm run preview` | Previews the production build locally. |

## 🌐 Deployment

The website is set up to deploy automatically on **Vercel** after every push to the main branch. Vercel reads the settings defined in the `vercel.json` file located at the repository's root to correctly orchestrate the build of the `frontend/` sub-folder.
