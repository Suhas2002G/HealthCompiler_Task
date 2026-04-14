from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from models.contact_model import Contact


def create_contact(db: Session, contact):
    try:
        db_contact = Contact(**contact.dict())
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone or Email already exists"
        )


def search_contacts(db: Session, query: str):
    return db.query(Contact).filter(
        (Contact.name.ilike(f"%{query}%")) |
        (Contact.phone.ilike(f"%{query}%")) |
        (Contact.email.ilike(f"%{query}%"))
    ).all()


def delete_contact(db: Session, contact_id: int):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()

    if not contact:
        raise HTTPException(
            status_code=404,
            detail="Contact not found"
        )

    db.delete(contact)
    db.commit()
    return True


def merge_contacts(db: Session, id1: int, id2: int):
    c1 = db.query(Contact).filter(Contact.id == id1).first()
    c2 = db.query(Contact).filter(Contact.id == id2).first()

    if not c1 or not c2:
        raise HTTPException(
            status_code=404,
            detail="One or both contacts not found"
        )

    try:
        c1.name = c1.name or c2.name
        c1.phone = c1.phone or c2.phone
        c1.email = c1.email or c2.email

        db.delete(c2)
        db.commit()
        db.refresh(c1)

        return c1

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Conflict while merging"
        )