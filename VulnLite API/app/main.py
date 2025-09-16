from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi import HTTPException
from fastapi import Body



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