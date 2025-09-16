from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi import HTTPException
from fastapi import Body
from .schemas import VulnCreate, VulnRead
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

# Update (partial) a vulnerability by ID
@app.patch("/vulns/{vuln_id}")
async def update_vuln(
    vuln_id: int,
    data: dict = Body(...),                           # JSON body with any fields to update
    session: AsyncSession = Depends(get_session),
):
    # 1) fetch the row
    result = await session.execute(select(Vulnerability).where(Vulnerability.id == vuln_id))
    vuln = result.scalars().first()
    if not vuln:
        raise HTTPException(status_code=404, detail="Vulnerability not found")

    # 2) apply only allowed fields
    allowed = {"title", "severity", "status", "notes", "archived"}
    for k, v in data.items():
        if k in allowed:
            setattr(vuln, k, v)

    # 3) save and return
    await session.commit()
    await session.refresh(vuln)
    return vuln


# Delete (soft by default). Use ?hard=true for hard delete.
@app.delete("/vulns/{vuln_id}")
async def delete_vuln(
    vuln_id: int,
    hard: bool = False,                                # /vulns/1?hard=true
    session: AsyncSession = Depends(get_session),
):
    # 1) fetch the row
    result = await session.execute(select(Vulnerability).where(Vulnerability.id == vuln_id))
    vuln = result.scalars().first()
    if not vuln:
        raise HTTPException(status_code=404, detail="Vulnerability not found")

    # 2) soft or hard delete
    if hard:
        await session.delete(vuln)                     # hard delete
        await session.commit()
        return {"ok": True, "deleted": "hard"}
    else:
        vuln.archived = True                           # soft delete (archive)
        await session.commit()
        await session.refresh(vuln)
        return {"ok": True, "deleted": "soft", "item": vuln}