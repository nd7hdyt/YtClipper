# AutoClip 

## 🎯 target

，status。nowcan，、、。

## 📋 status

### **✅ completed**
- [x] database（0）
- [x] file systemcompleted
- [x] filecompleted
- [x] create
- [x] database

### **🏗️ need**
- [ ] databaseverify
- [ ] configcheck
- [ ] frontendstatus
- [ ] projectcreatetest

## 🔧 step

### **：verify**

1. **checkdatabase**
   ```bash
   sqlite3 data/autoclip.db ".schema"
   ```

2. **check**
   ```bash
   tree data/ -L 3
   ```

3. **verifyconfigfile**
   - `backend/core/config.py`
   - `backend/core/unified_paths.py`

### **：starttest**

1. **startbackendservice**
   ```bash
   cd backend
   python main.py
   ```

2. **startfrontendservice**
   ```bash
   cd frontend
   npm run dev
   ```

3. **checkservicestatus**
   - backendAPI: http://localhost:8000/health
   - frontendpage: http://localhost:3000

### **：createtestproject**

1. **test**
   - usefrontend
   - verifyprojectcreate

2. **check**
   - verifydatabase
   - verifyfile system
   - verifyfrontend

## 📁 

```
data/
├── autoclip.db                 # database
├── autoclip_backup_*.db        # database
├── projects/                   # project
├── output/                     # 
│   ├── clips/                  # clip
│   ├── collections/            # 
│   └── metadata/               # metadata
├── temp/                       # file
├── cache/                      # cachefile
├── uploads/                    # upload file
└── backups/                    # file
```

## 🚀 best practices

### **1. data management**
- projectcompletedmetadatadatabase
- check
- filecache

### **2. **
- use
- 
- verifyconfig

### **3. status**
- file system、database、frontendstatus
- useWebSocketupdatestatus
- 

## 🔍 monitorcheck

### **1. checkproject**
```bash
# checkdatabasestatus
python scripts/check_database_status.py

# checkfile system
python scripts/validate_paths.py

# checkfrontendstatus
python scripts/check_frontend_state.py
```

### **2. **
```bash
# projectmetadata
python scripts/sync_complete_metadata.py

# project
python scripts/sync_complete_metadata.py <project_id>
```

### **3. verify**
```bash
# verifyconfig
python scripts/validate_paths.py
```

## 🚨 

### **1. stage**
- test
- usefiletest
- test

### **2. production**
- databasefile
- monitoruse
- settings

### **3. **
- database
- config
- 

## 📚 related docs

- [notes](SYSTEM_ARCHITECTURE.md)
- [quick start](../QUICK_START_GUIDE.md)

## 🎉 completedcheck

- [ ] start
- [ ] database
- [ ] frontend
- [ ] projectcreate
- [ ] check
- [ ] configverify
- [ ] docsupdatecompleted

---

**completed，：**
- 
- 
- 
- monitorchecktool
- docs
