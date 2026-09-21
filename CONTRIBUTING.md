# Contributing

ENAutoClipEN！EN，EN：

- 🐛 BugEN
- ✨ EN
- 📚 EN
- 🧪 EN
- 💡 EN
- 🎨 UI/UXEN

## EN

### 1. ForkEN

```bash
# ForkENGitHubEN，EN
git clone https://github.com/your-username/autoclip.git
cd autoclip

# EN
git remote add upstream https://github.com/original-username/autoclip.git
```

### 2. EN

```bash
# EN
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# EN venv\Scripts\activate  # Windows

# EN
pip install -r requirements.txt
cd frontend && npm install && cd ..

# EN
cp env.example .env
# EN.envEN，EN
```

### 3. EN

```bash
# ENRedis
brew services start redis  # macOS
# EN sudo systemctl start redis-server  # Linux

# EN
python -m uvicorn backend.main:app --reload --port 8000

# ENCelery Worker（EN -Q，EN `celery` EN，EN）
celery -A backend.core.celery_app worker --loglevel=info -Q celery,processing,video,notification,upload

# EN
cd frontend && npm run dev
```

## EN

### 1. EN

```bash
# ENmainEN
git checkout main
git pull upstream main
git checkout -b feature/your-feature-name
```

### 2. EN

#### EN

**Python (EN)**
- ENPEP 8EN
- ENBlackEN
- ENisortEN
- ENdocstring

```python
def example_function(param1: str, param2: int) -> bool:
    """
    EN
    
    Args:
        param1: EN1EN
        param2: EN2EN
        
    Returns:
        EN
    """
    pass
```

**TypeScript (EN)**
- ENESLintENPrettier
- ENJSDocEN
- ENHooks
- ENAnt DesignEN

```typescript
/**
 * EN
 */
interface ExampleProps {
  /** EN */
  title: string;
  /** EN */
  optional?: boolean;
}

const ExampleComponent: React.FC<ExampleProps> = ({ title, optional = false }) => {
  return <div>{title}</div>;
};
```

#### EN

EN：

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**EN (type):**
- `feat`: EN
- `fix`: BugEN
- `docs`: EN
- `style`: EN
- `refactor`: EN
- `test`: EN
- `chore`: EN

**EN:**
```
feat(api): add video download endpoint
fix(ui): resolve upload modal display issue
docs(readme): update installation instructions
```

### 3. EN

#### EN

```bash
# EN
pytest

# EN
pytest tests/test_api.py

# EN
pytest --cov=backend --cov-report=html
```

#### EN

```bash
cd frontend

# EN
npm test

# ENlintEN
npm run lint

# EN
npm run type-check
```

### 4. EN

```bash
# EN
git add .

# EN
git commit -m "feat(api): add video download endpoint"

# EN
git push origin feature/your-feature-name
```

### 5. ENPull Request

1. ENGitHubENPull Request
2. ENPREN
3. EN
4. ENCode Review

## Code ReviewEN

### EN

- ✅ EN
- ✅ EN
- ✅ EN
- ✅ EN
- ✅ EN
- ✅ EN

### EN

- EN
- EN
- ENPREN
- EN

## EN

### BugEN

ENGitHub IssuesENBugEN，EN：

1. **EN**
   - EN
   - PythonEN
   - Node.jsEN
   - EN

2. **EN**
   - EN
   - EN
   - EN

3. **EN**
   - EN
   - EN

4. **EN**
   - EN
   - EN
   - EN

### EN

EN，EN：

1. **EN**
   - EN
   - EN
   - EN

2. **EN**
   - EN
   - EN
   - EN

3. **EN**
   - EN
   - EN
   - EN

## EN

### EN

- 📖 EN
- 🔧 EN
- 🚀 Deployment
- ❓ FAQ
- 📝 APIEN

### EN

- ENMarkdownEN
- EN
- EN
- EN
- EN

## ENAs StandardEN

### EN

EN，EN：

- EN
- EN
- EN
- EN

### EN

- ENLanguageEN
- EN
- EN
- EN
- EN

## ContactEN

- **GitHub Issues**: [ENIssues](https://github.com/your-username/autoclip/issues)
- **GitHub Discussions**: [EN](https://github.com/your-username/autoclip/discussions)
- **EN**: support@autoclip.com

## Acknowledgments

ENAutoClipEN！EN。

---

**EN！** 🎉
