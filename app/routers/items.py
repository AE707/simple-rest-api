from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.auth import get_current_active_user
from app.db import get_db
from app.models import Item, User
from app.schemas import ItemCreate, ItemResponse, ItemUpdate

router = APIRouter(prefix="/items", tags=["items"])


@router.post("", response_model=ItemResponse, status_code=201, summary="Create a new item")
def create_item(
    item_in: ItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new item owned by the current user."""
    item = Item(**item_in.model_dump(), owner_id=current_user.id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("", response_model=List[ItemResponse], summary="List items")
def list_items(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Return a paginated list of items owned by the current user."""
    return (
        db.query(Item)
        .filter(Item.owner_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get("/{item_id}", response_model=ItemResponse, summary="Get item by ID")
def get_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Fetch a single item by its ID (must belong to current user)."""
    item = db.query(Item).filter(Item.id == item_id, Item.owner_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=ItemResponse, summary="Update an item")
def update_item(
    item_id: int,
    item_in: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update an existing item. Only the owner can update."""
    item = db.query(Item).filter(Item.id == item_id, Item.owner_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    update_data = item_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=204, summary="Delete an item")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete an item by ID. Only the owner can delete."""
    item = db.query(Item).filter(Item.id == item_id, Item.owner_id == current_user.id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
