import os
from datetime import datetime, timezone
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/api/markets")
def market_snapshot():
    """Simple market snapshot for demo purposes.
    In a real setup, this would pull from a data provider and/or database.
    """
    now = datetime.now(timezone.utc).isoformat()
    data = [
        {
            "symbol": "CL",
            "name": "WTI Crude Oil",
            "price": 78.42,
            "change": -0.62,
            "changePct": -0.78,
            "currency": "USD/bbl",
            "updatedAt": now,
        },
        {
            "symbol": "XAU",
            "name": "Gold",
            "price": 2345.10,
            "change": 12.3,
            "changePct": 0.53,
            "currency": "USD/oz",
            "updatedAt": now,
        },
        {
            "symbol": "HG",
            "name": "Copper",
            "price": 4.12,
            "change": -0.03,
            "changePct": -0.72,
            "currency": "USD/lb",
            "updatedAt": now,
        },
        {
            "symbol": "ZW",
            "name": "Wheat",
            "price": 621.5,
            "change": 4.75,
            "changePct": 0.77,
            "currency": "cents/bu",
            "updatedAt": now,
        },
    ]
    return {"data": data}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
