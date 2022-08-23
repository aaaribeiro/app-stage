from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from crud.organization import Organization as CRUD
from domain.organization import Organization as Domain

from database.handlers import get_db

# authentication
# from auth import auth

# constants
TAGS = ["organizations",]

router = APIRouter()

@router.get(
    "/organizations",
    tags=TAGS,
    response_model=List[Domain],
    # dependencies=[Depends(auth.api_token)],
)
async def read_organizations(skip: int = 0, limit: int = 100,
                            db: Session = Depends(get_db)):
    dbOrganizations = CRUD.readOrganizations(db, skip, limit)
    return dbOrganizations



@router.post(
    "/organizations",
    tags=TAGS,
    status_code=status.HTTP_201_CREATED, 
    # dependencies=[Depends(auth.api_token)],
)
async def create_organization(payload: Domain,
                            db: Session=Depends(get_db)):
    dbOrganization = CRUD.readOrganizationById(db, payload.id)
    if dbOrganization:
        raise HTTPException(status_code=400, detail="organization already exits")
    return CRUD.createOrganization(db, payload)



@router.put(
    "/organizations/{id}",
    tags=TAGS,
    status_code=status.HTTP_204_NO_CONTENT,
    # dependencies=[Depends(auth.api_token)],
)
async def update_organization(id: int, payload: Domain, 
                        db: Session = Depends(get_db)):
    dbOrganization = CRUD.readOrganizationById(db, id)
    if not dbOrganization:
        raise HTTPException(status_code=404, detail="organization not found")
    CRUD.updateOrganization(db, payload, dbOrganization) 



@router.delete(
    "/organizations/{id}",
    tags=TAGS,
    status_code=status.HTTP_204_NO_CONTENT,
    # dependencies=[Depends(auth.api_token)],
)
async def delete_organization(id: str, db: Session = Depends(get_db)):
    dbOrganization = CRUD.readOrganizationById(db, id)
    if not dbOrganization:
        raise HTTPException(status_code=404, detail="organization not found")
    CRUD.deleteOrganization(db, id)
