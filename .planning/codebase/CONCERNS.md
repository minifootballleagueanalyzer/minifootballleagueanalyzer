# Known Concerns & Tech Debt - MiniFootballLeagueAnalyzer

## Scraper Fragility
- **Selenium Dependency**: Relying on specific CSS selectors from `minifootballleagues.com`. Any site redesign will break the scraper.
- **Headless Mode**: Chrome updates might occasionally require driver synchronization.

## Data Management
- **Local JSON Storage**: As the number of leagues and historical data grows, the repository size will increase significantly.
- **Syncing Assets**: Team logos are stored as URLs; if external links break, images will fail to load in the frontend.

## SSG Latency
- **Weekly Updates**: ELO rankings only update once a week. Live updates would require moving to SSR (Server-Side Rendering) or a real-time database trigger.

## Performance
- **Large JSON payloads**: `elo_rankings.json` could become very large, impacting initial load times. Need to consider splitting by league in the future.
