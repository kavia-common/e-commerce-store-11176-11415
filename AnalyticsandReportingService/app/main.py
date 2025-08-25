import os
from typing import Dict, Any, List
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# PUBLIC_INTERFACE
def get_settings() -> Dict[str, Any]:
    """Load settings from environment variables."""
    return {
        "SERVICE_NAME": os.getenv("ANALYTICS_SERVICE_NAME", "Analytics and Reporting Service"),
        "ENV": os.getenv("ENV", "development"),
        "ALLOWED_ORIGINS": os.getenv("ALLOWED_ORIGINS", "*"),
        # Database envs for future persistence
        "POSTGRES_URL": os.getenv("ANALYTICS_DB_URL"),
        "POSTGRES_USER": os.getenv("ANALYTICS_DB_USER"),
        "POSTGRES_PASSWORD": os.getenv("ANALYTICS_DB_PASSWORD"),
        "POSTGRES_DB": os.getenv("ANALYTICS_DB_NAME"),
    }

settings = get_settings()

app = FastAPI(
    title="Analytics and Reporting Service",
    description="Aggregates sales, inventory, and customer data. Provides dashboards and exports.",
    version="1.0.0",
    openapi_tags=[
        {"name": "health", "description": "Health checks"},
        {"name": "analytics", "description": "Analytics endpoints"},
    ],
)

allow_origins = [o.strip() for o in settings["ALLOWED_ORIGINS"].split(",")] if settings["ALLOWED_ORIGINS"] else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SalesSummary(BaseModel):
    range: str = Field(..., description="Range descriptor")
    total_orders: int = Field(..., description="Total orders")
    total_revenue: float = Field(..., description="Total revenue")
    top_products: List[str] = Field(..., description="Top product ids")

class InventorySummary(BaseModel):
    total_skus: int = Field(..., description="Total SKUs")
    low_stock_skus: List[str] = Field(..., description="Low stock product ids")


@app.get("/health", tags=["health"], summary="Liveness", description="Return liveness info.")
async def health():
    return {"status": "ok", "service": settings["SERVICE_NAME"], "env": settings["ENV"]}


# PUBLIC_INTERFACE
@app.get("/api/v1/analytics/sales-summary", tags=["analytics"], summary="Sales summary", response_model=SalesSummary)
async def sales_summary(range: str = Query("7d", description="Time range like '24h', '7d', '30d'")):
    # Demo response; replace with DB/reporting queries
    data = SalesSummary(
        range=range,
        total_orders=123,
        total_revenue=45678.9,
        top_products=["SKU-1", "SKU-2", "SKU-3"],
    )
    return data


# PUBLIC_INTERFACE
@app.get("/api/v1/analytics/inventory-summary", tags=["analytics"], summary="Inventory summary", response_model=InventorySummary)
async def inventory_summary():
    # Demo response; replace with DB/reporting queries
    data = InventorySummary(
        total_skus=250,
        low_stock_skus=["SKU-99", "SKU-150", "SKU-200"],
    )
    return data
