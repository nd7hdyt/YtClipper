# AutoClip notes

## 🏗️ 

AutoClip based on Python + React clipgenerate，backend。

### ****

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   frontend (React)   │    │   backend (FastAPI) │    │   file system      │
│                 │    │                 │    │                 │
│ - project management      │◄──►│ - API service      │◄──►│ - projectfile      │
│ -       │    │ -       │    │ - file      │
│ - statusmonitor      │    │ -       │    │ - metadata        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                       ┌─────────────────┐
                       │   database (SQLite) │
                       │                 │
                       │ - project      │
                       │ - clipmetadata    │
                       │ - metadata    │
                       │ - status      │
                       └─────────────────┘
```

## 📁 

### **1. database (SQLite)**

**：**
- `projects`: project
- `clips`: clipmetadata
- `collections`: metadata
- `tasks`: status
- `bilibili_accounts`: Bsite account
- `upload_records`: file upload

**：**
```
projects (1) ──► (N) clips
projects (1) ──► (N) collections
projects (1) ──► (N) tasks
```

### **2. file system**

**：**
```
data/
├── projects/                    # projectfile
│   └── {project_id}/           # project
│       ├── raw/                # file
│       ├── step1_outline/      # outlinegenerate
│       ├── step2_timeline/     # 
│       ├── step3_scoring/      # content scoring
│       ├── step4_title/        # title generation
│       ├── step5_clustering/   # 
│       └── step6_video/        # generate
│           ├── clips_metadata.json    # clipmetadata
│           └── collections_metadata.json # metadata
├── output/                      # file
│   ├── clips/                  # clipfile
│   │   └── {project_id}/       # project
│   ├── collections/            # file
│   │   └── {project_id}/       # project
│   └── metadata/               # metadata
├── temp/                       # file
├── cache/                      # cachefile
├── uploads/                    # upload file
└── backups/                    # database
```

## 🔄 

### **1. projectcreate**

```
 → createproject → file → 
     ↓
database: projects added
file system: data/projects/{project_id}/raw/ 
```

### **2. **

```
 → subtitles →  → clipgenerate → generate → 
    ↓           ↓         ↓         ↓         ↓         ↓
step1_outline → step2_timeline → step3_scoring → step4_title → step5_clustering → step6_video
```

### **3. **

```
file systemcompleted → metadatagenerate → database → frontend
        ↓              ↓           ↓           ↓
   clips_metadata.json → metadata → clips → APIreturn
collections_metadata.json → metadata → collections → APIreturn
```

## 🔧 technical details

### **1. **

- ****: completedmetadatadatabase
- ****: 
- ****: added

### **2. **

- ****: `backend/core/unified_paths.py`
- ****: auto-detect
- **verify**: checkconfig

### **3. state management**

- **project status**: pending → processing → completed
- **status**: pending → running → completed/failed
- **update**: WebSocket + 

## 🚨 FAQsolution

### **1. issue**

**phenomenon**: file system，database
**reason**: failed
**solve**:  `scripts/sync_complete_metadata.py`

### **2. issue**

**phenomenon**: file
**reason**: config
**solve**: use

### **3. frontend**

**phenomenon**: backendAPI，frontend
**reason**: frontendcachestate managementissue
**solve**: cache，frontendservice

## 📋 monitor

### **1. check**

- ****: checkfile systemdatabase
- **config**: verifyconfig
- ****: monitoruse

### **2. **

- **database**:  SQLite database
- **file**: projectfile
- **config**: configfile

### **3. monitor**

- ****: monitorstatus
- **error**: issue
- ****: monitor

## 🚀 best practices

### **1. data management**

- 
- filecache
- file system

### **2. **

- test
- useconfig
- updatedocs

### **3. deploy**

- production
- monitoruse
- updatedependenciesfixsecurity
