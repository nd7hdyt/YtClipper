# EN

## EN

### EN

1. **EN**: EN
2. **EN**: EN
3. **EN**: EN
4. **EN**: EN

### EN

EN：
- EN: 100MB
- EN: 1MB
- EN: 50MB
- EN: 200MB
- EN: 1MB

**EN**: 352MB (EN) + 1MB (EN) = 353MB
**EN**: 351MB (EN) + 1MB (EN) = 352MB

EN，EN。

## EN

### EN：EN，EN

```
┌─────────────────┐    ┌─────────────────┐
│   EN        │    │   EN      │
│   (EN)      │    │   (EN)    │
├─────────────────┤    ├─────────────────┤
│ Project         │    │ EN    │
│ - id            │    │ EN        │
│ - name          │    │ EN    │
│ - status        │    │ EN    │
│ - metadata      │    │ EN        │
├─────────────────┤    ├─────────────────┤
│ Clip            │    │ EN    │
│ - id            │    │ - video_path    │
│ - title         │    │ - subtitle_path │
│ - start_time    │    │ - output_path   │
│ - end_time      │    │ - clip_path     │
│ - score         │    │ - collection_path│
│ - metadata      │    │                 │
│ - file_path     │    │                 │
└─────────────────┘    └─────────────────┘
```

### EN：EN

```
┌─────────────────────────────────────────────────────────┐
│                    EN                               │
├─────────────────────────────────────────────────────────┤
│                    EN                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ EN    │  │ EN    │  │ EN    │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
├─────────────────────────────────────────────────────────┤
│                    EN                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ EN      │  │ EN    │  │ EN    │     │
│  │ (EN)    │  │ (EN)  │  │ (EN)  │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
```

## EN

### 1. EN

```python
# backend/models/project.py
class Project(BaseModel, TimestampMixin):
    __tablename__ = "projects"
    
    # EN
    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.PENDING)
    project_type = Column(Enum(ProjectType), default=ProjectType.DEFAULT)
    
    # EN (EN)
    video_path = Column(String(500), comment="EN")
    subtitle_path = Column(String(500), comment="EN")
    
    # EN
    processing_config = Column(JSON, comment="EN")
    project_metadata = Column(JSON, comment="EN")
    
    # EN (EN，EN)
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
    
    # EN
    id = Column(String(36), primary_key=True)
    project_id = Column(String(36), ForeignKey("projects.id"))
    title = Column(String(255), nullable=False)
    description = Column(Text)
    
    # EN
    start_time = Column(Integer, nullable=False)
    end_time = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    
    # EN
    score = Column(Float)
    recommendation_reason = Column(Text)
    
    # EN (EN)
    video_path = Column(String(500), comment="EN")
    thumbnail_path = Column(String(500), comment="EN")
    
    # EN
    clip_metadata = Column(JSON, comment="EN")
    status = Column(Enum(ClipStatus), default=ClipStatus.PENDING)
```

### 2. EN

```
data/
├── projects/
│   └── {project_id}/
│       ├── raw/                    # EN
│       │   ├── video.mp4
│       │   └── subtitle.srt
│       ├── processing/             # EN
│       │   ├── step1_outline.json
│       │   ├── step2_timeline.json
│       │   ├── step3_scoring.json
│       │   ├── step4_title.json
│       │   └── step5_clustering.json
│       └── output/                 # EN
│           ├── clips/
│           │   ├── clip_1.mp4
│           │   ├── clip_2.mp4
│           │   └── ...
│           └── collections/
│               ├── collection_1.mp4
│               └── ...
├── temp/                           # EN
└── cache/                          # EN
```

### 3. EN

```python
# backend/services/storage_service.py
class StorageService:
    """EN"""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.project_dir = self._get_project_dir()
    
    def save_metadata(self, metadata: Dict[str, Any], step: str) -> str:
        """EN"""
        metadata_file = self.project_dir / "processing" / f"{step}.json"
        metadata_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        return str(metadata_file)
    
    def save_clip_file(self, clip_data: Dict[str, Any], clip_id: str) -> str:
        """EN"""
        clip_file = self.project_dir / "output" / "clips" / f"{clip_id}.mp4"
        clip_file.parent.mkdir(parents=True, exist_ok=True)
        
        # EN
        # ...
        
        return str(clip_file)
    
    def get_file_path(self, file_type: str, file_id: str = None) -> Path:
        """EN"""
        if file_type == "video":
            return self.project_dir / "raw" / "video.mp4"
        elif file_type == "subtitle":
            return self.project_dir / "raw" / "subtitle.srt"
        elif file_type == "clip":
            return self.project_dir / "output" / "clips" / f"{file_id}.mp4"
        elif file_type == "collection":
            return self.project_dir / "output" / "collections" / f"{file_id}.mp4"
        else:
            raise ValueError(f"ENSupportEN: {file_type}")
```

### 4. EN

```python
# backend/repositories/clip_repository.py
class ClipRepository(BaseRepository[Clip]):
    def create_clip(self, clip_data: Dict[str, Any]) -> Clip:
        """EN"""
        # 1. EN
        storage_service = StorageService(clip_data["project_id"])
        video_path = storage_service.save_clip_file(clip_data, clip_data["id"])
        
        # 2. EN
        clip = Clip(
            id=clip_data["id"],
            project_id=clip_data["project_id"],
            title=clip_data["title"],
            description=clip_data.get("description"),
            start_time=clip_data["start_time"],
            end_time=clip_data["end_time"],
            duration=clip_data["duration"],
            score=clip_data.get("score"),
            video_path=video_path,  # EN
            clip_metadata=clip_data.get("metadata", {})
        )
        
        self.db.add(clip)
        self.db.commit()
        return clip
    
    def get_clip_file(self, clip_id: str) -> Optional[Path]:
        """EN"""
        clip = self.get_by_id(clip_id)
        if clip and clip.video_path:
            return Path(clip.video_path)
        return None
```

## EN

### EN

| EN | EN | EN | EN |
|---------|---------|-----------|---------|
| 10EN | 3.53GB | 3.52GB | 10MB |
| 100EN | 35.3GB | 35.2GB | 100MB |
| 1000EN | 353GB | 352GB | 1GB |

### Performance

1. **EN**: EN50%EN
2. **EN**: EN，EN
3. **EN**: EN
4. **EN**: EN

### EN

1. **EN**: EN
2. **EN**: EN
3. **EN**: EN
4. **EN**: SupportEN

## EN

### EN：EN (1EN)

1. **EN**
   - EN
   - EN
   - EN

2. **EN**
   - EN
   - EN
   - EN

### EN：EN (1EN)

1. **RepositoryEN**
   - EN
   - EN
   - EN

2. **APIEN**
   - ENUploadEN
   - EN
   - EN

### EN：EN (0.5EN)

1. **EN**
   - EN
   - EN
   - EN

2. **EN**
   - EN
   - EN
   - EN

## EN

EN，EN：

1. **EN**: EN
2. **EN**: EN
3. **EN**: EN
4. **EN**: EN

EN，EN。
