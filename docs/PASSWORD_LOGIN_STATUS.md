# password loginstatusnotes

## issue

password loginfailed，"Request failed with status code 400"error。

## issue

，：

### 1. issue
- **errorreason**：password loginneedverify，useCookieimport method
- **status**：400（）
- **notes**：limit，bug

### 2. technical details
- **dev environment**：mock login succeeded，returntestCookie
- **production**：Bsign in，needverify

### 3. env var
```bash
# dev environment（mock login succeeded）
export ENVIRONMENT=development
export SKIP_COOKIE_VALIDATION=true

# production（verify）
export ENVIRONMENT=production
export SKIP_COOKIE_VALIDATION=false
```

## status

### ✅ solveissue
1. **format**：fixAPIserviceCookieformatissue
2. **error handling**：error
3. **support**：dev environmentsign in

### ⚠️ limit
1. **verify**：Bpassword loginneedverify
2. ****：password loginB
3. ****：verify

## solution

### 1：useCookieimport（recommend）
- **pros**：security、、
- **cons**：needfetchCookie
- **use cases**：daily use、account

### 2：password login
- **pros**：、
- **cons**：needverify、
- **use cases**：sign in、fetchCookie

### 3：
- **dev environment**：mock login succeeded，test
- **production**：useCookieimport

## technical details

### dev environment
```python
if is_development:
    # mock login succeeded，returntestCookie
    mock_cookies = {
        "SESSDATA": f"mock_sessdata_{username}",
        "bili_jct": f"mock_jct_{username}",
        "DedeUserID": "12345",
        "buvid3": f"mock_buvid_{username}"
    }
    return {"success": True, "cookies": mock_cookies}
```

### production
```python
else:
    # Bsign in，needverify
    # verify，useCookieimport
    return {
        "success": False,
        "message": "password loginneedverify，useCookieimport method"
    }
```

## test

### dev environmenttest
```
✅ sign insucceeded (200)
ID: xxx
: dev_user
: 
```

### productiontest
```
❌ sign infailed (400)
error: password loginneedverify，useCookieimport method
```

## 

### daily use
1. ****：Cookieimport method
   - security
   - 
   - 

2. ****：password login
   - Cookieuse
   - verify
   - use

### fetchCookiestep
1. sign inB
2. F12open devtools
3. Networktab
4. refresh page，
5. Cookie

## 

### 
1. **verify**：verify
2. ****：error，
3. ****：improveenv var

### 
1. **verify**：selectsign in
2. ****：sign in
3. ****：sign in

## summary

password login，features：

### ✅ status
- **dev environment**：mock login succeeded，test
- **production**：return400error，useCookieimport
- **error handling**：errorsolve

### 🔧 features
- ****：env var
- ****：fixCookieformatissue
- **error**：error

### 💡 use
- **test**：usedev environment，sign in
- **use**：recommendedCookieimport method
- **issue**：checkenv varsettingserror

test，productionsecuritysign inselect。
