"""
ENRepositoryEN
EN
"""

from typing import TypeVar, Generic, Optional, List, Dict, Any, Type
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from ..models.base import BaseModel

# EN
ModelType = TypeVar("ModelType", bound=BaseModel)

class BaseRepository(Generic[ModelType]):
    """
    ENRepositoryEN，ENCRUDEN
    
    Generic[ModelType]: EN，ModelTypemustENBaseModelEN
    """
    
    def __init__(self, model: Type[ModelType], db: Session):
        """
        initializeRepository
        
        Args:
            model: EN
            db: databaseEN
        """
        self.model = model
        self.db = db
    
    def create(self, auto_commit: bool = True, **kwargs) -> ModelType:
        """
        createEN
        
        Args:
            **kwargs: EN
            
        Returns:
            createEN
        """
        instance = self.model(**kwargs)
        self.db.add(instance)
        if auto_commit:
            self.db.commit()
        else:
            self.db.flush()
        self.db.refresh(instance)
        return instance
    
    def get_by_id(self, id: str) -> Optional[ModelType]:
        """
        ENIDfetchEN
        
        Args:
            id: ENID
            
        Returns:
            ENNone
        """
        return self.db.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """
        fetchallEN
        
        Args:
            skip: EN
            limit: returnEN
            
        Returns:
            EN
        """
        return self.db.query(self.model).offset(skip).limit(limit).all()
    
    def update(self, id: str, auto_commit: bool = True, **kwargs) -> Optional[ModelType]:
        """
        updateEN
        
        Args:
            id: ENID
            **kwargs: ENupdateEN
            
        Returns:
            updateENNone
        """
        instance = self.get_by_id(id)
        if instance:
            for field, value in kwargs.items():
                if hasattr(instance, field):
                    setattr(instance, field, value)
            if auto_commit:
                self.db.commit()
            else:
                self.db.flush()
            self.db.refresh(instance)
        return instance
    
    def delete(self, id: str, auto_commit: bool = True) -> bool:
        """
        deleteEN
        
        Args:
            id: ENID
            
        Returns:
            ENdeletesucceeded
        """
        instance = self.get_by_id(id)
        if instance:
            self.db.delete(instance)
            if auto_commit:
                self.db.commit()
            else:
                self.db.flush()
            return True
        return False
    
    def count(self) -> int:
        """
        fetchEN
        
        Returns:
            EN
        """
        return self.db.query(self.model).count()
    
    def exists(self, id: str) -> bool:
        """
        checkEN
        
        Args:
            id: ENID
            
        Returns:
            EN
        """
        return self.db.query(self.model).filter(self.model.id == id).first() is not None
    
    def find_by(self, **kwargs) -> List[ModelType]:
        """
        EN
        
        Args:
            **kwargs: EN
            
        Returns:
            EN
        """
        filters = []
        for field, value in kwargs.items():
            if hasattr(self.model, field):
                filters.append(getattr(self.model, field) == value)
        
        if filters:
            return self.db.query(self.model).filter(and_(*filters)).all()
        return []
    
    def find_one_by(self, **kwargs) -> Optional[ModelType]:
        """
        EN
        
        Args:
            **kwargs: EN
            
        Returns:
            ENNone
        """
        filters = []
        for field, value in kwargs.items():
            if hasattr(self.model, field):
                filters.append(getattr(self.model, field) == value)
        
        if filters:
            return self.db.query(self.model).filter(and_(*filters)).first()
        return None
    
    def find_by_condition(self, condition) -> List[ModelType]:
        """
        EN
        
        Args:
            condition: SQLAlchemyEN
            
        Returns:
            EN
        """
        return self.db.query(self.model).filter(condition).all()
    
    def find_one_by_condition(self, condition) -> Optional[ModelType]:
        """
        EN
        
        Args:
            condition: SQLAlchemyEN
            
        Returns:
            ENNone
        """
        return self.db.query(self.model).filter(condition).first()
    
    def bulk_create(self, instances: List[Dict[str, Any]], auto_commit: bool = True) -> List[ModelType]:
        """
        ENcreateEN
        
        Args:
            instances: ENcreateEN
            
        Returns:
            createEN
        """
        created_instances = []
        for instance_data in instances:
            instance = self.model(**instance_data)
            self.db.add(instance)
            created_instances.append(instance)
        
        if auto_commit:
            self.db.commit()
        else:
            self.db.flush()
        
        # ENallEN
        for instance in created_instances:
            self.db.refresh(instance)
        
        return created_instances
    
    def bulk_update(self, instances: List[ModelType], auto_commit: bool = True) -> List[ModelType]:
        """
        ENupdateEN
        
        Args:
            instances: ENupdateEN
            
        Returns:
            updateEN
        """
        for instance in instances:
            self.db.merge(instance)
        
        if auto_commit:
            self.db.commit()
        else:
            self.db.flush()
        return instances
    
    def bulk_delete(self, ids: List[str], auto_commit: bool = True) -> int:
        """
        ENdeleteEN
        
        Args:
            ids: ENdeleteENIDEN
            
        Returns:
            deleteEN
        """
        deleted_count = self.db.query(self.model).filter(
            self.model.id.in_(ids)
        ).delete(synchronize_session=False)
        
        if auto_commit:
            self.db.commit()
        else:
            self.db.flush()
        return deleted_count