from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from core.database import get_db
from schemas.contact_schema import ContactCreate
from services import contact_service
from utils.response import success_response, error_response


router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_contact(contact: ContactCreate, db: Session = Depends(get_db)):
    try:
        data = contact_service.create_contact(db, contact)
        return success_response(data, "Contact created successfully")
    
    except Exception as e:
        return error_response(str(e))


@router.get("/search")
def search_contacts(q: str, db: Session = Depends(get_db)):
    try:
        data = contact_service.search_contacts(db, q)
        return success_response(data, "Contacts fetched successfully")
    except Exception as e:
        return error_response(str(e))


@router.delete("/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    try:
        contact_service.delete_contact(db, contact_id)
        return success_response(message="Contact deleted successfully")
    except Exception as e:
        return error_response(str(e))


@router.put("/merge")
def merge_contacts(id1: int, id2: int, db: Session = Depends(get_db)):
    try:
        data = contact_service.merge_contacts(db, id1, id2)
        return success_response(data, "Contacts merged successfully")
    except Exception as e:
        return error_response(str(e))