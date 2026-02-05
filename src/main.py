"""
B2B E-Commerce Shipping Charge Estimator

FastAPI application entry point.
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.api import warehouse_router, shipping_router
from src.core.exceptions import ShippingError, NotFoundError, ValidationError


# Create FastAPI application
app = FastAPI(
    title="B2B Shipping Charge Estimator",
    description="""
    A production-ready API for calculating shipping charges in a B2B e-commerce 
    marketplace for Kirana stores.
    
    ## Features
    
    - **Nearest Warehouse Lookup**: Find the closest warehouse to a seller
    - **Shipping Cost Calculation**: Calculate costs based on distance and weight
    - **Multiple Transport Modes**: Mini Van, Truck, Aeroplane based on distance
    - **Delivery Speed Options**: Standard and Express delivery
    
    ## Shipping Rules
    
    | Distance | Mode | Rate |
    |----------|------|------|
    | 0-100 km | Mini Van | 3 INR/km/kg |
    | 100-500 km | Truck | 2 INR/km/kg |
    | 500+ km | Aeroplane | 1 INR/km/kg |
    
    **Delivery Speed:**
    - Standard: 10 INR base charge
    - Express: 10 INR base + 1.2 INR/kg extra
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========== EXCEPTION HANDLERS ==========

@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    """Handle 404 Not Found errors."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "NotFoundError",
            "message": exc.message,
            "statusCode": 404
        }
    )


@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    """Handle 400 Validation errors."""
    return JSONResponse(
        status_code=400,
        content={
            "error": "ValidationError",
            "message": exc.message,
            "statusCode": 400
        }
    )


@app.exception_handler(ShippingError)
async def shipping_error_handler(request: Request, exc: ShippingError):
    """Handle generic shipping errors."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "ShippingError",
            "message": exc.message,
            "statusCode": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred",
            "statusCode": 500
        }
    )


# ========== INCLUDE ROUTERS ==========

app.include_router(warehouse_router, prefix="/api/v1")
app.include_router(shipping_router, prefix="/api/v1")


# ========== ROOT ENDPOINT ==========

@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "B2B Shipping Charge Estimator",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "service": "shipping-charge-estimator",
        "version": "1.0.0"
    }
