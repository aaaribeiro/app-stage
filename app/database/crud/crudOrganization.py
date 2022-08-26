from typing import List
from sqlalchemy.orm import Session
from app.database.models import Organizations as ModelOrg
from app.domain.organization import Organization as DomainOrg


class CrudOrganization:

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
        dbOrganization = ModelOrg()
        for attr in payload.fields_set():
            setattr(dbOrganization, attr, getattr(payload, attr))
        db.add(dbOrganization)
        db.commit()


    @classmethod
    def updateOrganization(self, db: Session, payload: DomainOrg,
                            id: str) -> None:
        dbOrganization = self.readOrganizationById(db, id)
        for attr in payload.fields_set():
            setattr(dbOrganization, attr, getattr(payload, attr))
        db.commit()


    @classmethod
    def deleteOrganization(self, db: Session, id: str) -> None:
        dbOrganization = self.readOrganizationById(db, id)
        db.delete(dbOrganization)
        db.commit()