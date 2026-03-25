# app/routers/transactions.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app import models, schemas, auth

router = APIRouter()


@router.get("/", response_model=list[schemas.TransactionResponse])
def get_transactions(
    category_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    query = db.query(models.Transaction).filter(
        models.Transaction.user_id == current_user.id
    )
    if category_id:
        query = query.filter(models.Transaction.category_id == category_id)
    if start_date:
        query = query.filter(models.Transaction.date >= start_date)
    if end_date:
        query = query.filter(models.Transaction.date <= end_date)
    return query.all()


@router.post("/", response_model=schemas.TransactionResponse)
def create_transaction(
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    new_transaction = models.Transaction(
        user_id=current_user.id,
        type=transaction.type,
        category_id=transaction.category_id,
        note=transaction.note,
        amount=transaction.amount,
        date=transaction.date,
    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction


@router.put("/{transaction_id}", response_model=schemas.TransactionResponse)
def update_transaction(
    transaction_id: int,
    transaction: schemas.TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    db_transaction = (
        db.query(models.Transaction)
        .filter(
            models.Transaction.id == transaction_id,
            models.Transaction.user_id == current_user.id,
        )
        .first()
    )
    if not db_transaction:
        raise HTTPException(status_code=404, detail="找不到此記錄")

    if transaction.type in transaction.model_fields_set:
        db_transaction.type = transaction.type
    if transaction.category_id is not None:
        db_transaction.category_id = transaction.category_id
    if transaction.note is not None:
        db_transaction.note = transaction.note
    if transaction.amount is not None:
        db_transaction.amount = transaction.amount
    if transaction.date is not None:
        db_transaction.date = transaction.date

    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    db_transaction = (
        db.query(models.Transaction)
        .filter(
            models.Transaction.id == transaction_id,
            models.Transaction.user_id == current_user.id,
        )
        .first()
    )
    if not db_transaction:
        raise HTTPException(status_code=404, detail="找不到此記錄")
    db.delete(db_transaction)
    db.commit()
    return {"message": "刪除成功"}
