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
    """
    Merge two contacts into one.
    """

    # Prevent merging same contact
    if id1 == id2:
        raise HTTPException(400, "Cannot merge the same contact")

    c1 = db.query(Contact).filter(Contact.id == id1).first()
    c2 = db.query(Contact).filter(Contact.id == id2).first()

    if not c1 or not c2:
        raise HTTPException(404, "One or both contacts not found")

    # Direct conflict validation
    if c1.phone and c2.phone and c1.phone != c2.phone:
        raise HTTPException(400, "Phone number conflict")

    if c1.email and c2.email and c1.email != c2.email:
        raise HTTPException(400, "Email conflict")

    try:
        # STEP 1: delete secondary contact first
        db.delete(c2)
        db.flush()  # ensures deletion is applied before update

        # STEP 2: now safely merge
        if not c1.name:
            c1.name = c2.name

        if not c1.phone:
            c1.phone = c2.phone

        if not c1.email:
            c1.email = c2.email

        # STEP 3: commit
        db.commit()
        db.refresh(c1)

        return c1

    except IntegrityError:
        db.rollback()
        raise HTTPException(400, "Database integrity error during merge")

    except Exception as e:
        db.rollback()
        raise HTTPException(500, str(e))