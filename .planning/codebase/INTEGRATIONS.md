# External Integrations - MiniFootballLeagueAnalyzer

## 1. Supabase
- **Purpose**: User authentication and management of favorite teams/leagues.
- **Integration**: `@supabase/supabase-js` client in the frontend.

## 2. Google Gemini (AI)
- **Purpose**: Interactive chatbot to answer questions about league statistics and ELO rankings.
- **Integration**: `@google/generative-ai` SDK using a server-side proxy or direct client initialization.

## 3. Mapbox
- **Purpose**: Render an interactive map showing the locations of football venues.
- **Integration**: `mapbox-gl` and `react-map-gl`.

## 4. Vercel
- **Purpose**: Hosting, automated deployments, and performance monitoring.
- **Integration**: `@vercel/analytics`, `@vercel/speed-insights`.

## 5. GitHub Actions
- **Purpose**: Automate the weekly scraping and data refresh cycle (Wed 02:00 UTC).
- **Integration**: GitHub Secrets for `GH_PAT` to trigger Vercel rebuilds.
