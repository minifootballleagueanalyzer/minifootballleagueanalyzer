# Architecture - MiniFootballLeagueAnalyzer

## Overview
The project follows a **decoupled architecture** where a Python backend prepares data for a static-site-generated (SSG) frontend.

## Data Pipeline
1. **Scraping Phase**: `league_scraping.py` uses Selenium and BeautifulSoup to extract match results and team logos from minifootballleagues.com. Output: `jsons/*.json`.
2. **Processing Phase**: `simulacion_final.py` consumes the raw JSONs and uses the algorithm in `elo_system.py` to calculate Power Rankings (ELO) with time-decay and goal-margin multipliers.
3. **Export Phase**: Processed data is written to `frontend/public/elo_rankings.json`.

## Frontend Architecture (Astro Islands)
- **Astro**: Orchestrates the static site generation.
- **React Islands**: Used for interactive components that require state or dynamic rendering:
    - **H2H Comparison**: Comparing two teams' ELO history.
    - **Leaderboards**: Filterable and searchable league tables.
    - **Chatbot**: Real-time AI interaction.
- **Nanostores**: Lightweight state management for sharing data (e.g., selected league) between React islands without a heavy context provider.

## Design Patterns
- **Time-Decay ELO**: Recent matches carry more weight in the ranking calculation.
- **SSG (Static Site Generation)**: High performance and SEO by pre-rendering pages at build time.
