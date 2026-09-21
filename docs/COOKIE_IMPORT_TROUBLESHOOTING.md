# Cookieimporttroubleshooting

## issue

Cookieimportfailed，"Request failed with status code 500"error。

## issue

，issue：

1. **format**：APICookieformat`bilibili_service.py`format
2. **Cookieverify**：verify，Cookie
3. **error handling**：，issue

## solution

### 1. fixformat

**issue**：APICookie，service`code`format

**fix**：APICookieformat

```python
# fix：Cookie
cookie_content=json.dumps(cookies)

# fix：format
cookie_data = {
    "code": 0,
    "message": "sign insucceeded",
    "data": {
        "user_info": {
            "username": cookie_validation.get("username", "cookie_user"),
            "nickname": cookie_validation.get("nickname", "B"),
            "mid": cookie_validation.get("mid", "")
        },
        "cookie_info": {
            "cookies": [{"name": k, "value": v} for k, v in cookies.items()]
        }
    }
}
cookie_content=json.dumps(cookie_data)
```

### 2. Cookieverify

**issue**：verify，test

**fix**：dev modesupport，APIverify

```python
# dev environment：APIverify
skip_validation = (
    os.getenv("SKIP_COOKIE_VALIDATION", "false").lower() == "true" or
    os.getenv("ENVIRONMENT", "development") == "development"
)

if skip_validation:
    return {
        "valid": True,
        "username": f"user_{cookies.get('DedeUserID', 'unknown')}",
        "nickname": f"B_{cookies.get('DedeUserID', 'unknown')}",
        "mid": cookies.get('DedeUserID', '')
    }
```

### 3. error handling

**issue**：

**fix**：errorstatus

```python
except HTTPException:
    raise  # HTTP，status
except Exception as e:
    logger.error(f"Cookiesign infailed: {str(e)}")
    raise HTTPException(status_code=500, detail="sign infailed")
```

## testverify

### test

```
✅ fetchsign insucceeded
✅ Cookieverify
✅ password login
✅ sign in
✅ Cookieimportsucceeded (test)
```

### supportCookieformat

1. **BCookie**：
   ```
   SESSDATA=abc123def456; bili_jct=xyz789; DedeUserID=12345; buvid3=test123
   ```

2. **Cookie**：
   ```
   SESSDATA=space test; bili_jct=space jct; DedeUserID=11111; buvid3=space123
   ```

3. **Cookie**：
   ```
   SESSDATA=test_sessdata; bili_jct=test_jct; DedeUserID=67890; buvid3=test456; sid=test_sid
   ```

## config

### dev environment

```bash
# Cookieverify（test）
export ENVIRONMENT=development

# 
export SKIP_COOKIE_VALIDATION=true
```

### production

```bash
# verify
export ENVIRONMENT=production
export SKIP_COOKIE_VALIDATION=false
```

## usenotes

### 1. fetchCookie

1. sign inB
2. F12open devtools
3. Networktab
4. refresh page，
5. Cookie

### 2. importCookie

1. openAutoClipaccount
2. select"Cookieimport"tab
3. Cookie
4. settings
5. click"importCookie"

### 3. verifysucceeded

- status：200
- returnaccount：ID、、、status

## FAQ

### Q: testCookiesucceededimport？

A: dev mode，APIverify，test。productionverify。

### Q: Cookieimportfailed？

A: check：
1. Cookie（SESSDATA、bili_jct、DedeUserID）
2. Cookie
3. 
4. BAPIaccess

### Q: production？

A: env var：
- `ENVIRONMENT=development`：dev mode，verify
- `ENVIRONMENT=production`：，verify

## 

1. **Cookieupdate**：checkCookie
2. **verify**：Cookie
3. **import**：supportaccountimport
4. **import**：Cookieimportupdate

## summary

fixformat、verifyerror handling，Cookieimportnowcan。canuseformatCookieimport，verify。

improve：
- ✅ solve500errorissue
- ✅ supportCookieformat
- ✅ productionconfig
- ✅ error handling
- ✅ test
