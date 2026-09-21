# Auto Clips Frontend

EN React + TypeScript + Vite + Ant Design ENAutoEN。

## EN

### 🎯 EN
- **ENUpload**: ENUploadEN
- **ENProcessing**: AI AutoEN
- **EN**: EN、EN、DownloadEN
- **EN**: AI EN + ManualEN
- **EN**: ProcessingEN

### 🎨 EN
- **EN**: EN Ant Design EN
- **EN**: EN
- **EN**: EN、ENDownload
- **StatusEN**: ENProcessingStatusEN

## EN

- **EN**: React 18 + TypeScript
- **ENTool**: Vite
- **UI EN**: Ant Design
- **StatusEN**: Zustand
- **EN**: React Router DOM
- **HTTP EN**: Axios
- **EN**: React Beautiful DnD
- **EN**: React Player
- **ENUpload**: React Dropzone

## EN

### EnvironmentEN
- Node.js >= 16
- npm EN yarn

### InstallDependencies
```bash
npm install
# EN
yarn install
```

### StartENServiceEN
```bash
npm run dev
# EN
yarn dev
```

EN http://localhost:3000

### ENVersion
```bash
npm run build
# EN
yarn build
```

## ProjectEN

```
frontend/
├── public/                 # EN
├── src/
│   ├── components/         # EN
│   │   ├── Header.tsx      # EN
│   │   ├── FileUpload.tsx  # ENUploadEN
│   │   ├── ProjectCard.tsx # ProjectEN
│   │   ├── ClipCard.tsx    # EN
│   │   └── CollectionCard.tsx # EN
│   ├── pages/              # EN
│   │   ├── HomePage.tsx    # ProjectEN
│   │   └── ProjectDetailPage.tsx # ProjectEN
│   ├── services/           # API Service
│   │   └── api.ts          # API EN
│   ├── store/              # StatusEN
│   │   └── useProjectStore.ts # ProjectStatus
│   ├── App.tsx             # EN
│   ├── main.tsx            # EN
│   └── index.css           # EN
├── package.json
├── vite.config.ts          # Vite Config
├── tsconfig.json           # TypeScript Config
└── README.md
```

## EN

### ProjectEN (`/`)
- ProjectEN
- EN
- ENProject（ENUpload）
- ProjectStatusEN

### ProjectEN (`/project/:id`)
- ProjectENProcessingStatus
- EN
- AI EN
- ManualEN
- DownloadEN

## EN

### FileUpload
- ENUpload
- ENVerify
- UploadEN
- AutoENProject

### ProjectCard
- ProjectEN
- StatusEN
- EN
- EN

### ClipCard
- EN
- EN
- ENDownload
- EN

### CollectionCard
- EN
- EN
- EN
- GenerateEN

## API EN

EN `/api` EN，EN：

- `GET /api/projects` - ENProjectEN
- `POST /api/projects` - ENProject
- `GET /api/projects/:id` - ENProjectEN
- `POST /api/projects/:id/upload` - UploadEN
- `POST /api/projects/:id/process` - ENProcessing
- `GET /api/projects/:id/status` - ENProcessingStatus
- `PUT /api/projects/:id/clips/:clipId` - EN
- `PUT /api/projects/:id/collections/:collectionId` - EN
- `GET /api/projects/:id/download` - DownloadEN

## EN

### StatusEN
EN Zustand ENStatusEN，EN：
- ProjectENCurrentProject
- EN
- ENStatusENErrorEN

### EN
- EN Ant Design EN
- EN，EN
- EN
- EN

### EN
AllEN TypeScript EN，EN。

## EN

### ENEnvironment
```bash
npm run dev
```

### ENEnvironment
```bash
npm run build
npm run preview
```

### Docker EN
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

## EN

### EN
- [ ] EN
- [ ] EN
- [ ] EN
- [ ] EN
- [ ] EN

### EN
- [ ] EN
- [ ] EN
- [ ] EN
- [ ] EN

### EN
- [ ] EN
- [ ] EN
- [ ] EN
- [ ] EN

## EN

1. Fork Project
2. EN
3. EN
4. EN
5. EN Pull Request

## EN

MIT License