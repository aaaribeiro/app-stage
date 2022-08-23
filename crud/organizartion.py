from typing import List
from sqlalchemy.orm import Session

from database.models import Organizations as ModelOrg
from domain.organization import Organization as DomainOrg


class CRUDOrganization:

    def readOrganizations(self, db: Session, skip: int=0,
                            limit: int=100) -> List[ModelOrg]:
        return db.query(ModelOrg).offset(skip).\
            limit(limit).all()


    def readOrganizationById(self, db: Session, id: str) -> ModelOrg:
        return db.query(ModelOrg).get(id)
       

    def createOrganization(self, db: Session, payload: DomainOrg) -> None:
        dbOrganization = ModelOrg(
            id = payload.id,
            name = payload.name
            )
        db.add(dbOrganization)
        db.commit()


    def updateOrganization(self, db: Session, payload: DomainOrg,
                            dbOrganization: ModelOrg) -> None:
        dbOrganization.name = payload.name
        db.commit()


    def deleteOrganization(self, db: Session, id: str) -> None:
        dbOrganization = self.readOrganizationById(db, id)
        db.delete(dbOrganization)
        db.commit()