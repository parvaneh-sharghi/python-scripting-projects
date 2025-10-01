from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .db import Vulnerability
from .schemas import VulnCreate

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("vulnlite")

async def create_vuln_db(payload: VulnCreate, session: AsyncSession):
    v = Vulnerability(title=payload.title, severity=payload.severity, notes=payload.notes)
    session.add(v)
    await session.commit()
    await session.refresh(v)
    logger.info(f"Created vuln with id={v.id}")
    return v

async def get_vulns_db(session: AsyncSession):
    result= await session.execute(select(Vulnerability))
    vulns=result.scalars().all()
    return vulns
