# AGENTS.md — MiniFootballLeagueAnalyzer

## Project overview

MiniFootballLeagueAnalyzer is a two-layer project:

| Layer | Tech | Root |
|-------|------|------|
| **Backend** | Python 3.10 | `/` (repo root) |
| **Frontend** | Astro 5 + React 19 | `/frontend/` |

The backend scrapes match data from [minifootballleagues.com](https://minifootballleagues.com/), calculates ELO rankings, and writes JSON files that the frontend consumes via SSG (Static Site Generation). GitHub Actions keeps everything in sync automatically every night.

---

## Dev environment tips

### Python backend

- Always work from the **repo root** when running Python scripts.
- Install Python dependencies once into a virtual environment:
  ```bash
  python -m venv .venv
  source .venv/Scripts/activate   
  # Windows: .venv\Scripts\activate
  pip install -r requirements.txt
  ```
- The scraping step requires **Google Chrome** installed locally (Selenium uses it via ChromeDriver).
- Data files live in `jsons/`; ELO output files are written to `frontend/public/` so the Astro build can consume them.

### Frontend

- All `npm` commands must be run from the `frontend/` directory:
  ```bash
  cd frontend
  npm install      # first time only
  npm run dev      # start local dev server (Astro)
  ```
- The frontend fetches JSON data at build-time from GitHub for SSG; however, for local development, it uses the files in `frontend/public/`.
- The Astro config (`frontend/astro.config.mjs`) manages the React integration and base paths.

---

## Repository structure

```
MiniFootballLeagueAnalyzer/
├── .github/
│   └── workflows/
│       └── scraping.yml    # Runs scraping + ELO analysis daily at 02:00 UTC
├── jsons/                  # Raw match/standings data (one JSON per competition)
│   ├── classification/     # Scraped real points for rank comparison
│   ├── prim_div_mur.json
│   ├── seg_div_murA.json
│   ├── seg_div_murB.json
│   ├── ter_div_murA.json
│   ├── ter_div_murB.json
│   └── cuar_div_mur.json
├── frontend/               # Astro + React (Islands Architecture)
│   ├── public/             # Static assets + generated JSON consumed during build
│   ├── src/
│   │   ├── assets/         # Processed images and logos
│   │   ├── components/     # Interactive React components (islands)
│   │   │   └── Home/
│   │   │       ├── Home.jsx
│   │   │       └── Home.css
│   │   ├── layouts/        # Astro layouts
│   │   │   └── Layout.astro
│   │   └── pages/          # Astro pages (routes)
│   │       └── index.astro
│   ├── package.json
│   ├── astro.config.mjs
│   └── tsconfig.json       # Astro/React TS config
├── vercel.json             # Vercel deployment configuration
├── league_scraping.py      # Selenium + BeautifulSoup scraper
├── elo_system.py           # ELO calculation logic
├── simulacion_final.py     # Runs ELO pipeline, writes output JSONs
├── requirements.txt        # Python dependencies
└── README.md
```

---

## Running the data pipeline locally

```bash
# 1. Scrape fresh data from the web
python league_scraping.py

# 2. Compute ELO rankings and write output JSONs to frontend/public/
python simulacion_final.py
```

Run these in order from the repo root. After step 2 the frontend has up-to-date data for the next build.

---

## Frontend scripts

Run all of the following from the `frontend/` directory:

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start local Astro dev server |
| `npm run build` | Build static production site to `frontend/dist/` |
| `npm run preview` | Preview the production build locally |
| `npm run lint` | Run ESLint |

---

## CI / GitHub Actions / Vercel

| Tool | Trigger | What it does |
|----------|---------|--------------|
| **GitHub Actions** | Daily at 02:00 UTC | Scrapes data, runs ELO, and commits JSONs back to `main`. |
| **Vercel** | Push to `main` | Detects changes, runs `npm run build` in `frontend/`, and deploys the static site. |


---
