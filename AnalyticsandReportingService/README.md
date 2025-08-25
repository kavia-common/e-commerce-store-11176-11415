# Analytics and Reporting Service

Provides analytics endpoints for dashboards and exports.

## Run
1. Copy `.env.example` to `.env` (optional).
2. Install deps:

   pip install -r requirements.txt

3. Start:

   uvicorn app.main:app --host 0.0.0.0 --port 8003 --reload

## Endpoints
- GET /health
- GET /api/v1/analytics/sales-summary?range=7d
- GET /api/v1/analytics/inventory-summary
