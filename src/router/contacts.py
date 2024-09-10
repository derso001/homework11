from fastapi import Depends, HTTPException, status, Query, APIRouter
from sqlalchemy.orm import Session
from typing import List
from src.db.db import get_db
from src.db.models import Contact
from src.schemas import ContactCreate, ContactResponse

router =  APIRouter(prefix='/tags', tags=["tags"])

@router.post("/contacts")
async def create_note(contact: ContactCreate, db: Session = Depends(get_db)):
    new_contact = Contact(
        first_name=contact.first_name,
        last_name=contact.last_name,
        email=contact.email,
        phone_number=contact.phone_number,
        birthday=contact.birthday,
        additional_info=contact.additional_info)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact


@router.get("/contacts")
async def read_contacts(skip: int = 0, limit: int = Query(default=10, le=100, ge=10), db: Session = Depends(get_db)):
    contacts = db.query(Contact).offset(skip).limit(limit).all()
    return contacts


@router.get("/contacts/{contact_id}")
async def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

# # Контакти повинні бути доступні для пошуку за іменем, прізвищем чи адресою електронної пошти (Query).

# @app.get("/contacts/{}")
# async def 
# # API повинен мати змогу отримати список контактів з днями народження на найближчі 7 днів.

@router.put("/contacts/{contact_id}")
async def update_contact(contact_id: int, contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.dict().items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

@router.delete("/contacts/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    return None
