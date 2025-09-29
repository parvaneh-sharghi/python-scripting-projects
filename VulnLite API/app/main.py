from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi import HTTPException
from fastapi import Body
from .schemas import VulnCreate, VulnRead, VulnUpdate
from .db import init_db, get_session, Vulnerability
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI application
app = FastAPI(title="VulnLite API", version="0.1")

# Run database initialization on startup
@app.on_event("startup")
async def on_startup():
    await init_db()


# CORS (for frontend/Postman consumption)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple health check endpoint
@app.get("/health")
def health():
    return {"Hello": True}

# POST endpoint to create a new vulnerability
@app.post("/vulns", response_model=VulnRead, status_code=201)
async def create_vuln(payload: VulnCreate, session: AsyncSession = Depends(get_session)):
    v = Vulnerability(title=payload.title, severity=payload.severity, notes=payload.notes)
    session.add(v)
    await session.commit()
    await session.refresh(v)
    return v               # Return the object as JSON response


@app.get("/vulns", response_model=list[VulnRead])
async def list_vulns(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Vulnerability).where(Vulnerability.archived == False))
    return result.scalars().all()                   # FastAPI will return JSON



# Get a single vulnerability by ID
@app.get("/vulns/{vuln_id}", response_model=VulnRead)
async def get_vuln(
    vuln_id: int,
    session: AsyncSession = Depends(get_session)
):
    # get by Id 
    db_vuln = await session.get(Vulnerability, vuln_id)
    if not db_vuln:
        raise HTTPException(status_code=404, detail="Vulnerability not found")

    # returning JSON
    return db_vuln

# Update (partial) a vulnerability by ID
@app.patch("/vulns/{vuln_id}", response_model=VulnRead)
async def update_vuln(
    vuln_id: int,                                 # The ID of the record to update
    vuln_data: VulnUpdate,                        # Request body with optional fields
    session: AsyncSession = Depends(get_session)  # Database session
):
    # 1. Find the record by ID
    db_vuln = await session.get(Vulnerability, vuln_id)
    if not db_vuln:
        raise HTTPException(status_code=404, detail="Vulnerability not found")

    # 2. Update only the fields provided in vuln_data
    update_data = vuln_data.dict(exclude_unset=True)  # ignore missing fields
    for key, value in update_data.items():
        setattr(db_vuln, key, value)


    # 3. Save changes
    await session.commit()
    await session.refresh(db_vuln)

    # 4. Return updated record as JSON
    return db_vuln


# Delete (soft by default). Use ?hard=true for hard delete.
@app.delete("/vulns/{vuln_id}", response_model=VulnRead)
async def delete_vuln(
    vuln_id: int,
    hard: bool = False,
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(select(Vulnerability).where(Vulnerability.id == vuln_id))
    vuln = result.scalars().first()
    if not vuln:
        raise HTTPException(status_code=404, detail="Vulnerability not found")

    if hard:
        await session.delete(vuln)
        await session.commit()
        return {"ok": True, "deleted": "hard", "item": None}
    else:
        vuln.archived = True
        await session.commit()
        await session.refresh(vuln)
        return {"ok": True, "deleted": "soft", "item": vuln}