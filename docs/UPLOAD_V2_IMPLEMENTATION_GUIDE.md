#  v2.0 

## overview

based on [biliup-rs](https://github.com/biliup/biliup-rs) project，B，support、selecterror handling。

## features

### 🚀 
- ****: support bda2、qn、alia、bldsa、tx、txa、bda 
- **select**: select
- ****: supportfile，
- **error handling**: error
- **progress**: progressstatusupdate

### 🔧 improve
- **based on biliup-rs**: 
- ****: 
- **Cookie**: fix，supportkeyformat
- **API**: 

## 

### file
```
backend/services/
├── bilibili_service.py          # service（update）
├── bilibili_upload_v2.py        # v2.0
└── bilibili_service_backup.py   # file
```

### 
- `BilibiliUploaderV2`: ，
- `BilibiliUploadServiceV2`: service，status

## usestep

### 1. importCookie

update，needimportBCookie：

1. **fetchCookie**:
   - sign inB
   - open devtools (F12)
   - Networktab
   - Cookie

2. **importCookie**:
   - accessstatuspage: `http://localhost:3000/upload-status`
   - click"status"buttonB
   - "account"tabclick"add account"
   - select"Cookiesign in"
   - Cookie

### 2. test

1. **checkaccountstatus**:
   - accountstatus""
   - checkCookie

2. **create**:
   - projectselectclip
   - click"B"button
   - 、、
   - selectaccount

3. **monitorprogress**:
   - statuspageviewprogress
   - monitorstatuserror

## 

### 
```
1. verifysign instatus → 2. fetchID → 3. select
    ↓
4.  → 5.  → 6.  → 7. returnBV
```

### 
|  | provider | features |
|------|--------|------|
| bda2 |  | default， |
| qn |  |  |
| alia |  | access |
| bldsa | B |  |
| tx |  |  |
| txa |  |  |
| bda |  |  |

### error handling
- **error**: ，3
- **error**: sign in
- **fileerror**: checkfileformat
- **APIerror**: error

## config notes

### env var
```bash
# key（generate）
export ENCRYPTION_KEY="BekpMhcsOolyI_n9Hz9NxzLqMgll3vfa9qJYPOxtQXM="
```

### 
```python
metadata = {
    'title': '',           # max80
    'description': '',     # max2000
    'tags': ['1', '2'],   # 
    'partition_id': 3             # ID
}
```

## troubleshooting

### FAQ

1. **Cookiefailed**
   - reason: usekey
   - solve: importCookie

2. **failed**
   - reason: issueAPIlimit
   - solve: check network connection，

3. **file**
   - reason: B8GBlimit
   - solve: file

4. **accountstatus**
   - reason: Cookie
   - solve: sign infetchCookie

### method

1. **view**:
   ```bash
   tail -f logs/celery.log
   ```

2. **checkdatabase**:
   ```sql
   SELECT * FROM bilibili_upload_records ORDER BY created_at DESC LIMIT 5;
   ```

3. **testAPI**:
   ```bash
   curl -s http://localhost:8000/api/v1/upload/records | jq .
   ```

## performance

### 
- ****: support
- **select**: select
- ****: failed

### 
- **error**: 
- **status**: updatestatus
- ****: file

## changelog

### v2.0.0 (2025-09-11)
- ✅ based on biliup-rs 
- ✅ supportselect
- ✅ fixCookie
- ✅ error handling
- ✅ progress

### 
- 🔄 supportP
- 🔄 
- 🔄 
- 🔄 support

## 

- [biliup-rs project](https://github.com/biliup/biliup-rs)
- [BAPIdocs](https://github.com/biliup/biliup-rs)
- [statuspageuse](./UPLOAD_STATUS_PAGE_GUIDE.md)
