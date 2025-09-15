from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi import HTTPException


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


@app.get("/vulns")
async def list_vulns(session: AsyncSession = Depends(get_session)):
    # run a SELECT query to fetch all rows
    result = await session.execute(select(Vulnerability))
    items = result.scalars().all()  # convert result to list of ORM objects
    return items                    # FastAPI will return JSON

# Get a single vulnerability by ID
@app.get("/vulns/{vuln_id}")
async def get_vuln(vuln_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Vulnerability).where(Vulnerability.id == vuln_id)
    )
    vuln = result.scalars().first()
    if not vuln:
        # return 404 if not found
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    return vuln