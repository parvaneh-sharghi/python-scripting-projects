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

async def get_vuln_db(vuln_id:int,session:AsyncSession):
    result=await session.execute(select(Vulnerability).where(Vulnerability.id== vuln_id))
    vuln=result.scalars().one_or_none()
    if vuln:
        logger.debug(f"[DB] Retrieved vuln id={vuln.id}")
    else:
        logger.warning(f"[DB] Vuln id={vuln_id} not found")
    return vuln