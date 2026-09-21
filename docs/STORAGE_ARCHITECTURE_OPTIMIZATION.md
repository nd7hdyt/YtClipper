# 

## issue

### issue

1. ****: file systemdatabase
2. ****: 
3. ****: need
4. **issue**: impact

### 

project：
- file: 100MB
- subtitlesfile: 1MB
- processingfile: 50MB
- clipfile: 200MB
- databasemetadata: 1MB

****: 352MB (file system) + 1MB (database) = 353MB
****: 351MB (file system) + 1MB (database) = 352MB

project，project。

## 

### ：databasemetadata，file systemfile

```
┌─────────────────┐    ┌─────────────────┐
│   database        │    │   file system      │
│   (metadata)      │    │   (file)    │
├─────────────────┤    ├─────────────────┤
│ Project         │    │ file    │
│ - id            │    │ subtitlesfile        │
│ - name          │    │ processingfile    │
│ - status        │    │ clipfile    │
│ - metadata      │    │ file        │
├─────────────────┤    ├─────────────────┤
│ Clip            │    │ file    │
│ - id            │    │ - video_path    │
│ - title         │    │ - subtitle_path │
│ - start_time    │    │ - output_path   │
│ - end_time      │    │ - clip_path     │
│ - score         │    │ - collection_path│
│ - metadata      │    │                 │
│ - file_path     │    │                 │
└─────────────────┘    └─────────────────┘
```

### ：

```
┌─────────────────────────────────────────────────────────┐
│                                                   │
├─────────────────────────────────────────────────────────┤
│                    service                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ projectservice    │  │ clipservice    │  │ service    │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
├─────────────────────────────────────────────────────────┤
│                                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ database      │  │ file system    │  │ cache    │     │
│  │ (metadata)    │  │ (file)  │  │ ()  │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
```

## 

### 1. databasemodel

```python
# backend/models/project.py
class Project(BaseModel, TimestampMixin):
    __tablename__ = "projects"
    
    # 
    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.PENDING)
    project_type = Column(Enum(ProjectType), default=ProjectType.DEFAULT)
    
    # file (file)
    video_path = Column(String(500), comment="file")
    subtitle_path = Column(String(500), comment="subtitlesfile")
    
    # configmetadata
    processing_config = Column(JSON, comment="config")
    project_metadata = Column(JSON, comment="projectmetadata")
    
    #  (，)
    @property
    def clips_count(self):
        return len(self.clips) if self.clips else 0
    
    @property
    def collections_count(self):
        return len(self.collections) if self.collections else 0
```

```python
# backend/models/clip.py
class Clip(BaseModel):
    __tablename__ = "clips"
    
    # 
    id = Column(String(36), primary_key=True)
    project_id = Column(String(36), ForeignKey("projects.id"))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    # 
    start_time = Column(Integer, nullable=False)
    end_time = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    
    # 
    score = Column(Float)
    recommendation_reason = Column(Text)
    
    # file (file)
    video_path = Column(String(500), comment="clipfile")
    thumbnail_path = Column(String(500), comment="file")
    
    # metadata
    clip_metadata = Column(JSON, comment="clipmetadata")
    status = Column(Enum(ClipStatus), default=ClipStatus.PENDING)
```

### 2. file system

```
data/
├── projects/
│   └── {project_id}/
│       ├── raw/                    # file
│       │   ├── video.mp4
│       │   └── subtitle.srt
│       ├── processing/             # processingfile
│       │   ├── step1_outline.json
│       │   ├── step2_timeline.json
│       │   ├── step3_scoring.json
│       │   ├── step4_title.json
│       │   └── step5_clustering.json
│       └── output/                 # file
│           ├── clips/
│           │   ├── clip_1.mp4
│           │   ├── clip_2.mp4
│           │   └── ...
│           └── collections/
│               ├── collection_1.mp4
│               └── ...
├── temp/                           # file
└── cache/                          # cachefile
```

### 3. service

```python
# backend/services/storage_service.py
class StorageService:
    """service"""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.project_dir = self._get_project_dir()
    
    def save_metadata(self, metadata: Dict[str, Any], step: str) -> str:
        """metadatafile system"""
        metadata_file = self.project_dir / "processing" / f"{step}.json"
        metadata_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        return str(metadata_file)
    
    def save_clip_file(self, clip_data: Dict[str, Any], clip_id: str) -> str:
        """clipfile"""
        clip_file = self.project_dir / "output" / "clips" / f"{clip_id}.mp4"
        clip_file.parent.mkdir(parents=True, exist_ok=True)
        
        # file
        # ...
        
        return str(clip_file)
    
    def get_file_path(self, file_type: str, file_id: str = None) -> Path:
        """fetchfile"""
        if file_type == "video":
            return self.project_dir / "raw" / "video.mp4"
        elif file_type == "subtitle":
            return self.project_dir / "raw" / "subtitle.srt"
        elif file_type == "clip":
            return self.project_dir / "output" / "clips" / f"{file_id}.mp4"
        elif file_type == "collection":
            return self.project_dir / "output" / "collections" / f"{file_id}.mp4"
        else:
            raise ValueError(f"supportfile: {file_type}")
```

### 4. access

```python
# backend/repositories/clip_repository.py
class ClipRepository(BaseRepository[Clip]):
    def create_clip(self, clip_data: Dict[str, Any]) -> Clip:
        """createclip"""
        # 1. clipfilefile system
        storage_service = StorageService(clip_data["project_id"])
        video_path = storage_service.save_clip_file(clip_data, clip_data["id"])
        
        # 2. metadatadatabase
        clip = Clip(
            id=clip_data["id"],
            project_id=clip_data["project_id"],
            title=clip_data["title"],
            description=clip_data.get("description"),
            start_time=clip_data["start_time"],
            end_time=clip_data["end_time"],
            duration=clip_data["duration"],
            score=clip_data.get("score"),
            video_path=video_path,  # 
            clip_metadata=clip_data.get("metadata", {})
        )
        
        self.db.add(clip)
        self.db.commit()
        return clip
    
    def get_clip_file(self, clip_id: str) -> Optional[Path]:
        """fetchclipfile"""
        clip = self.get_by_id(clip_id)
        if clip and clip.video_path:
            return Path(clip.video_path)
        return None
```

## 

### 

| project |  |  |  |
|---------|---------|-----------|---------|
| 10project | 3.53GB | 3.52GB | 10MB |
| 100project | 35.3GB | 35.2GB | 100MB |
| 1000project | 353GB | 352GB | 1GB |

### performance

1. ****: 50%
2. ****: database，fileaccess
3. ****: no need
4. ****: candatabasefile system

### 

1. ****: 
2. **error**: issue
3. ****: issue
4. ****: support

## 

### stage： (1)

1. **databasemodel**
   - 
   - file
   - 

2. **service**
   - service
   - file
   - file

### stage：service (1)

1. **Repository**
   - access
   - file
   - cache

2. **API**
   - file uploaddownload
   - 
   - fileverify

### stage： (0.5)

1. ****
   - 
   - file
   - verify

2. **test**
   - test
   - testaccess
   - issue

## summary

，can：

1. ****: 
2. ****: 
3. ****: 
4. ****: 

，。
