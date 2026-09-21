# Auto Clips Frontend

based on React + TypeScript + Vite + Ant Design clipfrontend。

## features

### 🎯 
- ****: supportfilesubtitlesfile
- ****: AI 
- ****: view、edit、download
- **create**: AI recommend + create collection
- **monitor**: progress

### 🎨 
- ****: based on Ant Design 
- ****: support
- ****: 、download
- **status**: statusprogress

## 

- **frontend**: React 18 + TypeScript
- **buildtool**: Vite
- **UI **: Ant Design
- **state management**: Zustand
- **route**: React Router DOM
- **HTTP **: Axios
- ****: React Beautiful DnD
- ****: React Player
- **file upload**: React Dropzone

## quick start

### 
- Node.js >= 16
- npm  yarn

### installdependencies
```bash
npm install
# 
yarn install
```

### startserver
```bash
npm run dev
# 
yarn dev
```

access http://localhost:3000

### buildversion
```bash
npm run build
# 
yarn build
```

## project

```
frontend/
├── public/                 # 
├── src/
│   ├── components/         # 
│   │   ├── Header.tsx      # page
│   │   ├── FileUpload.tsx  # file upload
│   │   ├── ProjectCard.tsx # project
│   │   ├── ClipCard.tsx    # 
│   │   └── CollectionCard.tsx # 
│   ├── pages/              # page
│   │   ├── HomePage.tsx    # project
│   │   └── ProjectDetailPage.tsx # project
│   ├── services/           # API service
│   │   └── api.ts          # API API
│   ├── store/              # state management
│   │   └── useProjectStore.ts # project status
│   ├── App.tsx             # 
│   ├── main.tsx            # 
│   └── index.css           # 
├── package.json
├── vite.config.ts          # Vite config
├── tsconfig.json           # TypeScript config
└── README.md
```

## pagenotes

### project (`/`)
- project
- 
- new project（file upload）
- project statusmonitor

### project (`/project/:id`)
- projectstatus
- 
- AI 
- create collection
- downloadexport

## notes

### FileUpload
- supportclick
- fileverify
- progress
- createproject

### ProjectCard
- project
- status
- button
- progress

### ClipCard
- 
- 
- editdownload
- 

### CollectionCard
- 
- 
- 
- generate

## API API

frontend `/api` proxybackend，API：

- `GET /api/projects` - fetchproject
- `POST /api/projects` - createproject
- `GET /api/projects/:id` - fetchproject
- `POST /api/projects/:id/upload` - upload file
- `POST /api/projects/:id/process` - 
- `GET /api/projects/:id/status` - fetchstatus
- `PUT /api/projects/:id/clips/:clipId` - update
- `PUT /api/projects/:id/collections/:collectionId` - update
- `GET /api/projects/:id/download` - download

## notes

### state management
use Zustand state management，：
- projectproject
- 
- statuserror

### 
- use Ant Design 
- responsive design，support
- 
- 

### 
 TypeScript ，security。

## deploynotes

### dev environment
```bash
npm run dev
```

### production
```bash
npm run build
npm run preview
```

### Docker deploy
```dockerfile
FROM node:16-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

## 

### 
- [ ] edit
- [ ] 
- [ ] exportformat
- [ ] 
- [ ] cloudintegration

### performance
- [ ] 
- [ ] 
- [ ] 
- [ ] cache

### 
- [ ] support
- [ ] 
- [ ] 
- [ ] access

## contributing guide

1. Fork project
2. create
3. 
4. 
5. create Pull Request

## 

MIT License