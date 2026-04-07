# School District Evaluator

## Project Overview
A simple React web app that helps parents and educators evaluate school districts
across the US using the SchoolDigger API.

## Tech Stack
- React + Vite
- Vitest + React Testing Library for unit tests
- CSS Modules or plain CSS (keep it simple)
- Deploy to Vercel

## API
- SchoolDigger API v2.3: https://api.schooldigger.com
- App ID: 32e0c2e9
- App Key: fe67cad95da74a892758f35ecdaa46ae
- Auth: pass `appID` and `appKey` as query params
- Key endpoints:
  - GET /v2.3/districts?st={state} — search districts by state
  - GET /v2.3/districts/{id} — district detail
  - GET /v2.3/rankings/districts/{st} — district rankings by state
  - GET /v2.3/schools?st={state}&districtID={id} — schools in a district

## Features (keep it minimal)
1. Select a state → see ranked school districts
2. Click a district → see details and schools within it
3. Simple, clean UI — nothing fancy

## Testing
- 100% code coverage required
- Use Vitest + React Testing Library
- Mock all API calls in tests

## Commands
- `npm run dev` — start dev server
- `npm run build` — production build
- `npm test` — run tests
- `npm run coverage` — run tests with coverage
