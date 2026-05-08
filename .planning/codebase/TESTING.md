# Testing Strategy - MiniFootballLeagueAnalyzer

## Backend Testing
- **Framework**: `pytest`
- **Scope**:
    - **ELO Algorithm**: Validating point calculations across different scorelines.
    - **Data Integrity**: Ensuring scraped JSONs match expected schemas.
    - **Scraper Logic**: Verifying URL generation and element selection.

## Frontend Testing
- **Framework**: `vitest`
- **Library**: `React Testing Library`, `jsdom`
- **Scope**:
    - **Unit Tests**: Individual React components (e.g., `LeagueTable`, `TeamCard`).
    - **Integration Tests**: Verifying Nanostore state updates across islands.
    - **Snapshot Testing**: Ensuring UI stability for critical data views.

## CI Verification
- Automated tests run via GitHub Actions on every pull request to ensure no regressions in the ELO calculation or frontend build.
