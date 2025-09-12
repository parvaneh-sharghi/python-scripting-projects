from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .db import init_db, get_session, Vulnerability

# Create FastAPI application
app = FastAPI(title="VulnLite API", version="0.1")

# Run database initialization on startup
@app.on_event("startup")
async def on_startup():
    await init_db()

# Simple health check endpoint
@app.get("/health")
def health():
    return {"ok": True}

# POST endpoint to create a new vulnerability
@app.post("/vulns")
async def create_vuln(
    vuln: Vulnerability,                      # Input body: matches ORM model
    session: AsyncSession = Depends(get_session),  # Inject DB session
):
    session.add(vuln)           # Mark object for INSERT
    await session.commit()      # Commit the transaction
    await session.refresh(vuln) # Refresh to get ID and DB-generated values
    return vuln                 # Return the object as JSON response
