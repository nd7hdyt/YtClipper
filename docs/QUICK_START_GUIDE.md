# 🚀 AIEN - Quick StartEN

## 📋 Project Overview

AIENBased onAIENAuto ClippingEN，EN。EN，EN。

## 🎯 EN

1. **EN**: ENSQLite + SQLAlchemyEN
2. **EN**: ENFastAPI，EN
3. **EN**: EN

## 🏗️ Project Structure

```
autoclip/
├── backend/                    # EN
│   ├── app/                   # FastAPIEN
│   ├── api/                   # APIEN
│   ├── core/                  # EN
│   ├── models/                # EN
│   ├── services/              # EN
│   └── tasks/                 # Task Queue
├── frontend/                   # EN
├── shared/                     # EN
├── docs/                       # EN
└── data/                       # EN
```

## 🛠️ EN

### EN
- Python 3.10+（EN 3.11）
- Node.js 16+
- Redis
- Git

### EN

1. **EN**
```bash
git clone <repository-url>
cd autoclip
```

2. **EN**
```bash
cd backend
# ENPoetry (EN)
curl -sSL https://install.python-poetry.org | python3 -

# EN
poetry install

# EN
poetry shell
```

3. **EN**
```bash
cd frontend
npm install
```

4. **ENRedis**
```bash
# macOS
brew install redis
brew services start redis

# Ubuntu
sudo apt-get install redis-server
sudo systemctl start redis
```

## 🚀 Quick Start

### 1. EN
```bash
cd backend
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. EN
```bash
cd frontend
npm run dev
```

### 3. EN
- EN: http://localhost:3000
- ENAPI: http://localhost:8000
- APIEN: http://localhost:8000/docs

## 📚 Development Guide

### EN

#### ENAPIEN
1. EN `backend/api/v1/` EN
2. EN `backend/app/main.py` EN
3. EN `backend/services/` EN

```python
# backend/api/v1/example.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.services.example_service import ExampleService

router = APIRouter()

@router.get("/example")
async def get_example(db: Session = Depends(get_db)):
    service = ExampleService(db)
    return service.get_examples()
```

#### EN
1. EN `backend/models/` EN
2. EN `Base` EN
3. EN

```python
# backend/models/example.py
from sqlalchemy import Column, String, DateTime
from backend.models.base import Base, TimestampMixin

class Example(Base, TimestampMixin):
    __tablename__ = "examples"
    
    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(500))
```

#### EN
1. EN `backend/services/` EN
2. EN
3. EN

```python
# backend/services/example_service.py
from sqlalchemy.orm import Session
from backend.models.example import Example
from backend.schemas.example import ExampleCreate

class ExampleService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_example(self, example_data: ExampleCreate) -> Example:
        example = Example(**example_data.dict())
        self.db.add(example)
        self.db.commit()
        self.db.refresh(example)
        return example
```

### EN

#### EN
1. EN `frontend/src/pages/` EN
2. EN
3. EN

```typescript
// frontend/src/pages/ExamplePage.tsx
import React from 'react';
import { Card, Table } from 'antd';

const ExamplePage: React.FC = () => {
  return (
    <Card title="EN">
      <Table />
    </Card>
  );
};

export default ExamplePage;
```

#### ENAPIEN
1. EN `frontend/src/services/` ENAPIEN
2. ENAPIEN
3. EN

```typescript
// frontend/src/services/api.ts
export const exampleApi = {
  getExamples: async (): Promise<Example[]> => {
    const response = await apiService.get('/examples');
    return response.data;
  },
  
  createExample: async (data: ExampleCreate): Promise<Example> => {
    const response = await apiService.post('/examples', data);
    return response.data;
  }
};
```

## 🧪 EN

### EN
```bash
cd backend
poetry run pytest
```

### EN
```bash
cd frontend
npm test
```

### EN
```bash
# EN
npm run test:e2e
```

## 📊 EN

### EN
```bash
cd backend
alembic revision --autogenerate -m "EN"
```

### EN
```bash
alembic upgrade head
```

### EN
```bash
alembic downgrade -1
```

## 🔧 EN

### EN
```bash
# EN
poetry run uvicorn app.main:app --reload

# EN
npm run dev

# EN
npm run build

# EN
poetry run pytest
npm test
```

### EN
```bash
# EN
alembic revision --autogenerate -m "EN"

# EN
alembic upgrade head

# EN
alembic history
```

### EN
```bash
# ENDockerEN
docker build -t autoclip .

# ENDockerEN
docker run -p 8000:8000 autoclip
```

## 🐛 FAQ

### 1. EN
**EN**: EN
**EN**:
- EN
- EN
- EN

### 2. RedisEN
**EN**: CeleryENRedis
**EN**:
- ENRedisEN
- ENRedisEN
- ENRedisEN

### 3. EN
**EN**: npm run build EN
**EN**:
- ENnode_modulesEN
- ENTypeScriptEN
- EN

### 4. APIEN
**EN**: ENAPI
**EN**:
- EN
- ENCORSEN
- ENAPIEN

## 📞 EN

### EN
- [Project Management](./PROJECT_MANAGEMENT.md)

### Tech StackEN
- [FastAPIEN](https://fastapi.tiangolo.com/)
- [SQLAlchemyEN](https://docs.sqlalchemy.org/)
- [CeleryEN](https://docs.celeryproject.org/)
- [ReactEN](https://reactjs.org/docs/)

### EN
- ENGitHub Issue
- ContactEN
- ENWiki

## 🎉 EN

1. **ENProject Structure**: EN
2. **EN**: EN
3. **EN**: EN
4. **EN**: EN
5. **EN**: EN

---

**EN**: 1.0  
**EN**: 2024EN12EN  
**EN**: 2024EN12EN 