# Project Structure - MiniFootballLeagueAnalyzer

## Root Directory
- `league_scraping.py`: Scraper orchestration logic.
- `elo_system.py`: Implementation of the ELO ranking algorithm.
- `simulacion_final.py`: Main data processing and export script.
- `jsons/`: Storage for raw match data and classifications.
- `.github/workflows/`: GitHub Actions for automated scraping.

## Frontend Directory (`/frontend`)
- `src/pages/`: Astro routes and page layouts.
- `src/components/`: React islands and UI components.
- `src/styles/`: Global and component-level CSS.
- `public/`: Static assets, including `elo_rankings.json` and team logos.
- `vitest.config.ts`: Configuration for frontend testing.

## Data Schema
- **Raw JSON**: `[{"jornada": 1, "equipo_local": "...", "goles_local": 2, ...}]`
- **Processed ELO**: `{ "league_id": [{ "posicion": 1, "equipo": "...", "puntos": 1550, "evolucion": [...] }] }`
