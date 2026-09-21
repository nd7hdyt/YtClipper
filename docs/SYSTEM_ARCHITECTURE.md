# AutoClip System ArchitectureEN

## 🏗️ EN

AutoClip ENBased on Python + React ENAuto ClippingENCollection GenerationEN，AdoptsFrontend-Backend SeparationEN。

### **EN**

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   EN (React)   │    │   EN (FastAPI) │    │   EN      │
│                 │    │                 │    │                 │
│ - Project Management      │◄──►│ - API EN      │◄──►│ - EN      │
│ - EN      │    │ - EN      │    │ - EN      │
│ - EN      │    │ - EN      │    │ - EN        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                       ┌─────────────────┐
                       │   EN (SQLite) │
                       │                 │
                       │ - EN      │
                       │ - EN    │
                       │ - EN    │
                       │ - EN      │
                       └─────────────────┘
```

## 📁 EN

### **1. EN (SQLite)**

**EN：**
- `projects`: EN
- `clips`: EN
- `collections`: EN
- `tasks`: EN
- `bilibili_accounts`: BENAccountEN
- `upload_records`: ENUploadEN

**EN：**
```
projects (1) ──► (N) clips
projects (1) ──► (N) collections
projects (1) ──► (N) tasks
```

### **2. EN**

**EN：**
```
data/
├── projects/                    # EN
│   └── {project_id}/           # EN
│       ├── raw/                # EN
│       ├── step1_outline/      # EN
│       ├── step2_timeline/     # EN
│       ├── step3_scoring/      # EN
│       ├── step4_title/        # EN
│       ├── step5_clustering/   # EN
│       └── step6_video/        # EN
│           ├── clips_metadata.json    # EN
│           └── collections_metadata.json # EN
├── output/                      # EN
│   ├── clips/                  # EN
│   │   └── {project_id}/       # EN
│   ├── collections/            # EN
│   │   └── {project_id}/       # EN
│   └── metadata/               # EN
├── temp/                       # EN
├── cache/                      # EN
├── uploads/                    # UploadEN
└── backups/                    # EN
```

## 🔄 EN

### **1. EN**

```
ENUploadEN → EN → EN → EN
     ↓
EN: projects EN
EN: data/projects/{project_id}/raw/ EN
```

### **2. EN**

```
EN → EN → EN → EN → Collection Generation → EN
    ↓           ↓         ↓         ↓         ↓         ↓
step1_outline → step2_timeline → step3_scoring → step4_title → step5_clustering → step6_video
```

### **3. EN**

```
EN → EN → EN → EN
        ↓              ↓           ↓           ↓
   clips_metadata.json → EN → ENclipsEN → APIEN
collections_metadata.json → EN → ENcollectionsEN → APIEN
```

## 🔧 EN

### **1. EN**

- **EN**: EN
- **EN**: ProvidesEN
- **EN**: EN

### **2. EN**

- **EN**: `backend/core/unified_paths.py`
- **EN**: EN
- **EN**: EN

### **3. EN**

- **EN**: pending → processing → completed
- **EN**: pending → running → completed/failed
- **EN**: WebSocket + EN

## 🚨 FAQEN

### **1. EN**

**EN**: EN，EN
**EN**: EN
**EN**: EN `scripts/sync_complete_metadata.py`

### **2. EN**

**EN**: EN
**EN**: EN
**EN**: EN

### **3. EN**

**EN**: ENAPIEN，EN
**EN**: EN
**EN**: EN，EN

## 📋 EN

### **1. EN**

- **EN**: EN
- **EN**: EN
- **EN**: EN

### **2. EN**

- **EN**: EN SQLite EN
- **EN**: EN
- **EN**: EN

### **3. EN**

- **EN**: EN
- **EN**: EN
- **EN**: EN

## 🚀 EN

### **1. EN**

- EN
- EN
- EN

### **2. EN**

- EN
- EN
- EN

### **3. EN**

- EN
- EN
- EN
