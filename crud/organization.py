from typing import List
from sqlalchemy.orm import Session

from database.models import Organizations as ModelOrg
from domain.organization import Organization as DomainOrg


class Organization:

    @classmethod
    def readOrganizations(self, db: Session, skip: int=0,
                            limit: int=100) -> List[ModelOrg]:
        return db.query(ModelOrg).offset(skip).\
            limit(limit).all()


    @classmethod
    def readOrganizationById(self, db: Session, id: str) -> ModelOrg:
        return db.query(ModelOrg).get(id)


    @classmethod
    def createOrganization(self, db: Session, payload: DomainOrg) -> None:
        dbOrganization = ModelOrg(
            id = payload.id,
            name = payload.name
            )
        db.add(dbOrganization)
        db.commit()


    @classmethod
    def updateOrganization(self, db: Session, payload: DomainOrg,
                            id: str) -> None:
        dbOrganization = self.readOrganizationById(db, id)
        if payload.name is not None:
            dbOrganization.name = payload.name
        db.commit()


    @classmethod
    def deleteOrganization(self, db: Session, id: str) -> None:
        dbOrganization = self.readOrganizationById(db, id)
        db.delete(dbOrganization)
        db.commit()