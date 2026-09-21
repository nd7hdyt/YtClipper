# 🚀 AIclipproject - quick start

## 📋 project

AIcliptoolbased onAIcliptool，。project，targetbackend。

## 🎯 target

1. ****: SQLite + SQLAlchemy
2. **service**: FastAPI，service
3. ****: backend

## 🏗️ project

```
autoclip/
├── backend/                    # backendservice
│   ├── app/                   # FastAPI
│   ├── api/                   # APIroute
│   ├── core/                  # core modules
│   ├── models/                # model
│   ├── services/              # service
│   └── tasks/                 # 
├── frontend/                   # frontend
├── shared/                     # 
├── docs/                       # docs
└── data/                       # file
```

## 🛠️ dev environment

### tool
- Python 3.10+（recommend 3.11）
- Node.js 16+
- Redis
- Git

### installstep

1. **project**
```bash
git clone <repository-url>
cd autoclip
```

2. **backendsettings**
```bash
cd backend
# installPoetry (not installed)
curl -sSL https://install.python-poetry.org | python3 -

# installdependencies
poetry install

# 
poetry shell
```

3. **frontendsettings**
```bash
cd frontend
npm install
```

4. **startRedis**
```bash
# macOS
brew install redis
brew services start redis

# Ubuntu
sudo apt-get install redis-server
sudo systemctl start redis
```

## 🚀 quick start

### 1. startbackendservice
```bash
cd backend
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. startfrontendservice
```bash
cd frontend
npm run dev
```

### 3. access
- frontend: http://localhost:3000
- backendAPI: http://localhost:8000
- APIdocs: http://localhost:8000/docs

## 📚 

### backend dev

#### APIroute
1.  `backend/api/v1/` createroutefile
2.  `backend/app/main.py` route
3.  `backend/services/` service

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

#### model
1.  `backend/models/` createmodelfile
2.  `Base` 
3. database

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

#### service
1.  `backend/services/` createservicefile
2. 
3. error handling

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

### frontend dev

#### page
1.  `frontend/src/pages/` createpage
2. routeconfigpage
3. 

```typescript
// frontend/src/pages/ExamplePage.tsx
import React from 'react';
import { Card, Table } from 'antd';

const ExamplePage: React.FC = () => {
  return (
    <Card title="page">
      <Table />
    </Card>
  );
};

export default ExamplePage;
```

#### APIcall
1.  `frontend/src/services/` APImethod
2. useAPIcall
3. error handlingstatus

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

## 🧪 test

### backendtest
```bash
cd backend
poetry run pytest
```

### frontendtest
```bash
cd frontend
npm test
```

### test
```bash
# startservice
npm run test:e2e
```

## 📊 database

### create
```bash
cd backend
alembic revision --autogenerate -m ""
```

### 
```bash
alembic upgrade head
```

### 
```bash
alembic downgrade -1
```

## 🔧 

### 
```bash
# startbackend devserver
poetry run uvicorn app.main:app --reload

# startfrontend devserver
npm run dev

# buildfrontend
npm run build

# test
poetry run pytest
npm test
```

### database
```bash
# create
alembic revision --autogenerate -m ""

# 
alembic upgrade head

# view
alembic history
```

### deploy
```bash
# buildDocker
docker build -t autoclip .

# Docker
docker run -p 8000:8000 autoclip
```

## 🐛 FAQ

### 1. databaseconnection failed
**issue**: database
**solution**:
- checkdatabasefile
- confirmdatabasesettings
- checkdatabase

### 2. Redisconnection failed
**issue**: CeleryRedis
**solution**:
- confirmRedisservice
- checkRedisconfig
- confirmRedisport

### 3. frontendbuildfailed
**issue**: npm run build failed
**solution**:
- node_modulesinstall
- checkTypeScripterror
- confirmdependenciesinstall

### 4. APIcallfailed
**issue**: frontendcallbackendAPI
**solution**:
- confirmbackendservice
- checkCORSconfig
- verifyAPI

## 📞 get help

### docs
- [project management](./PROJECT_MANAGEMENT.md)

### docs
- [FastAPIdocs](https://fastapi.tiangolo.com/)
- [SQLAlchemydocs](https://docs.sqlalchemy.org/)
- [Celerydocs](https://docs.celeryproject.org/)
- [Reactdocs](https://reactjs.org/docs/)

### issue
- createGitHub Issue
- project
- viewprojectWiki

## 🎉 

1. **project**: docs
2. **settingsdev environment**: stepconfig
3. ****: startservicetest
4. ****: select
5. ****: followproject

---

**docsversion**: 1.0  
**createdate**: 202412  
**last updated**: 202412 