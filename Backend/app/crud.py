from sqlalchemy.orm import Session
from . import models

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_items(db: Session):
    return db.query(models.Item).all()

def log_interaction(db, user_id, item_id, feedback_type):
    try:
        interaction = models.Interaction(
            user_id=user_id,
            item_id=item_id,
            type=feedback_type
        )
        db.add(interaction)
        db.commit()
        db.refresh(interaction)
        return interaction
    except Exception as e:
        db.rollback()  
        raise e

