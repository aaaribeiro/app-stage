from typing import List
from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session
from app.database.crud.crudOrganization import CrudOrganization
from app.domain.organization import Organization
from app.database.dbHandlers import get_db
# from auth import auth


# constants
TAGS = ["organizations",]
router = APIRouter()

@router.get(
    "/organizations",
    tags=TAGS,
    response_model=List[Organization],
    # dependencies=[Depends(auth.api_token)],
)
async def read_organizations(skip: int = 0, limit: int = 100,
                            db: Session = Depends(get_db)):
    dbOrganizations = CrudOrganization.readOrganizations(db, skip, limit)
    return dbOrganizations


@router.get(
    "/organizations/{id}",
    tags=TAGS,
    status_code=status.HTTP_200_OK,
    response_model=Organization,
    # dependencies=[Depends(auth.api_token)]
)
async def read_organization(id: str, db:Session=Depends(get_db)):
    if not CrudOrganization.readOrganizationById(db, id):
        raise HTTPException(status_code=404, detail="organization not found")
    return CrudOrganization.readOrganizationById(db, id)


@router.post(
    "/organizations",
    tags=TAGS,
    status_code=status.HTTP_201_CREATED, 
    # dependencies=[Depends(auth.api_token)],
)
async def create_organization(payload: Organization,
                            db: Session=Depends(get_db)):
    if CrudOrganization.readOrganizationById(db, payload.id):
        raise HTTPException(status_code=400, detail="organization already exits")
    CrudOrganization.createOrganization(db, payload)



@router.patch(
    "/organizations/{id}",
    tags=TAGS,
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(auth.api_token)],
)
async def update_organization(id: str, payload: Organization, 
                        db: Session = Depends(get_db)):
    if not CrudOrganization.readOrganizationById(db, id):
        raise HTTPException(status_code=404, detail="organization not found")
    CrudOrganization.updateOrganization(db, payload, id) 



@router.delete(
    "/organizations/{id}",
    tags=TAGS,
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(auth.api_token)],
)
async def delete_organization(id: str, db: Session = Depends(get_db)):
    if not CrudOrganization.readOrganizationById(db, id):
        raise HTTPException(status_code=404, detail="organization not found")
    CrudOrganization.deleteOrganization(db, id)
