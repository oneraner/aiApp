# 🤖 AI ChatBot Platform

<div align="center">

![TypeScript](https://img.shields.io/badge/TypeScript-5.9-blue?style=for-the-badge&logo=typescript)
![React](https://img.shields.io/badge/React-19-61dafb?style=for-the-badge&logo=react)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=for-the-badge&logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=for-the-badge&logo=redis)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-4.0-38B2AC?style=for-the-badge&logo=tailwind-css)

**一個全端 AI 對話平台，整合 OpenAI 與 Google Gemini API，支援即時串流回應、對話歷史管理與 Rate Limiting 機制**

[🌐 Live Demo (Frontend)](https://ai-app-ai-web.vercel.app/) | [📡 API Endpoint](https://aiapp-wz6i.onrender.com)

</div>

---

## 📑 目錄

- [✨ 專案特點](#-專案特點)
- [🏗️ 系統架構](#️-系統架構)
- [🛠️ 技術棧](#️-技術棧)
- [🚀 快速開始](#-快速開始)
- [☁️ 部署指南](#️-部署指南)
- [🔧 環境變數設定](#-環境變數設定)
- [📁 專案結構](#-專案結構)
- [🧑‍💻 開發者亮點](#-開發者亮點)

---

## ✨ 專案特點

### 🎯 核心功能
- **多模型 AI 對話** - 同時支援 OpenAI GPT 與 Google Gemini，可動態切換模型，因為沒買 OpenAI，所以只能用 Gemini
- **即時串流回應 (SSE)** - Server-Sent Events 實現流暢的打字機效果
- **對話歷史管理** - PostgreSQL 持久化儲存，支援多輪對話上下文
- **全域 Rate Limiting** - Redis 實現 API 請求限制，防止濫用

### 🎨 前端亮點
- **React 19** 就是 React
- **TanStack Router** 類型安全路由，支援 SSR，嘗試 Next.js、React Router 之外的選擇
- **Tailwind CSS 4** 經歷過 300KB~500KB 的 CSS 檔案之後，唯一支持 Tailwind CSS
- **響應式設計 （ＲＷＤ）** 有稍微喬一下但沒有很仔細，畢竟也沒有設計稿
- **深淺主題切換** Gemini 風格藍色配色，支援系統主題偵測
- **UI 優化** 透過 ui-ux-pro-max skill 進行設計系統優化

### ⚡ 後端亮點
- **非同步架構** - 全面採用 async/await，高併發處理能力
- **自動資料庫遷移** - Alembic 整合，啟動時自動執行 migrations
- **依賴注入設計** - 清晰的模組化架構，易於測試與維護
- **完整 CORS 配置** - 支援本地開發與生產環境
- **全域錯誤處理** - API 回傳詳細錯誤訊息 + 修復提示
- **Sentry 整合** - 生產環境即時錯誤監控與追蹤
- **完整測試覆蓋** - 包含單元測試與整合測試，確保系統穩定性

---

## 🏗️ 系統架構

```mermaid
graph TB
    subgraph "Frontend (Vercel)"
        A[React 19 + Vite] --> B[TanStack Router]
        B --> C[Radix UI Components]
    end
    
    subgraph "Backend (Render)"
        D[FastAPI] --> E[AI Services]
        E --> F[OpenAI API]
        E --> G[Gemini API]
        D --> H[Rate Limiter]
    end
    
    subgraph "Database (Render)"
        I[(PostgreSQL)]
    end
    
    subgraph "Cache (Upstash)"
        J[(Redis)]
    end
    
    A -.->|HTTPS + SSE| D
    D --> I
    D --> J
    H --> J
```

### 部署架構概覽

| 服務 | 平台 | 說明 |
|------|------|------|
| **Frontend** | Vercel | React SPA，全球 CDN 分發 |
| **Backend** | Render | FastAPI 服務，Web Service |
| **PostgreSQL** | Render | 託管資料庫服務 |
| **Redis** | Upstash | Serverless Redis，支援全球節點 |

---

## 🛠️ 技術棧

### Frontend (`apps/ai-web`)
| 技術 | 版本 | 用途 |
|------|------|------|
| React | 19.2 | UI 框架 (最新版本) |
| TypeScript | 5.7 | 類型安全 |
| Vite | 7.1 | 建構工具 |
| TanStack Router | 1.132 | 類型安全路由 |
| Tailwind CSS | 4.0 | 樣式系統 |
| Radix UI | Latest | 無障礙元件庫 |
| Biome | 2.2 | Linter & Formatter |

### Backend (`apps/api`)
| 技術 | 版本 | 用途 |
|------|------|------|
| Python | 3.11+ | 主要語言 |
| FastAPI | 0.115 | Web 框架 |
| SQLAlchemy | 2.0 | ORM (async) |
| Alembic | 1.14 | 資料庫遷移 |
| asyncpg | 0.30 | PostgreSQL 驅動 |
| Redis | 7.0 | 快取與 Rate Limiting |
| openai-agents | 0.6 | OpenAI SDK |
| google-genai | Latest | Gemini SDK |

### DevOps & Tooling
| 技術 | 用途 |
|------|------|
| Turborepo | Monorepo 管理 |
| pnpm | 套件管理 |
| Docker Compose | 本地開發環境 |
| GitHub Actions | CI/CD (可選) |

---

## 🚀 快速開始

### 前置需求

- **Node.js** >= 18
- **pnpm** >= 9.0
- **Python** >= 3.11
- **Docker** (用於本地資料庫)

### 1️⃣ Clone 專案

```bash
git clone https://github.com/your-username/aiApp.git
cd aiApp
```

### 2️⃣ 安裝依賴

```bash
# 安裝前端依賴
pnpm install

# 安裝後端依賴
cd apps/api
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ 設定環境變數

```bash
# 前端環境變數
cp apps/ai-web/.env.example apps/ai-web/.env

# 後端環境變數
cp apps/api/.env.example apps/api/.env
# 編輯 .env 填入你的 API Keys
```

### 4️⃣ 啟動本地服務

```bash
# 終端機 1: 啟動 PostgreSQL 與 Redis (Docker)
pnpm dev:services

# 終端機 2: 啟動所有開發伺服器
pnpm dev
```

或者分開啟動：

```bash
# 只啟動前端 (http://localhost:3000)
pnpm --filter ai-web dev

# 只啟動後端 (http://localhost:8000)
cd apps/api && pnpm dev
```

### 5️⃣ 驗證服務

- **前端**: http://localhost:3000
- **後端 API**: http://localhost:8000
- **API 文件**: http://localhost:8000/docs

### 6️⃣ 執行測試

```bash
cd apps/api
source .venv/bin/activate
pytest app/tests/ -v
```

---

## ☁️ 部署指南

### 🔵 Frontend - Vercel

1. **連接 GitHub Repository**
   - 登入 [Vercel](https://vercel.com)
   - Import 你的 GitHub repository

2. **設定 Build Configuration**
   ```
   Framework Preset: Vite
   Root Directory: apps/ai-web
   Build Command: pnpm build
   Output Directory: dist
   ```

3. **設定環境變數**
   ```
   VITE_API_URL=https://your-backend.onrender.com
   ```

4. **部署**
   - 點擊 Deploy，Vercel 會自動建構與部署

---

### 🟣 Backend + PostgreSQL - Render

#### 建立 PostgreSQL 資料庫

1. 登入 [Render](https://render.com)
2. 點擊 **New** → **PostgreSQL**
3. 設定資料庫：
   - Name: `aiapp-db`
   - Region: Singapore (選擇最近的區域)
4. 複製 **Internal Database URL** 備用

#### 部署 Backend Web Service

1. 點擊 **New** → **Web Service**
2. 連接 GitHub Repository
3. 設定服務：
   ```
   Name: aiapp-api
   Root Directory: apps/api
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

4. 設定環境變數：
   | Key | Value |
   |-----|-------|
   | `DATABASE_URL` | `postgresql+asyncpg://...` (從 PostgreSQL 複製並修改 driver) |
   | `REDIS_URL` | (從 Upstash 取得) |
   | `OPENAI_API_KEY` | 你的 OpenAI API Key |
   | `GEMINI_API_KEY` | 你的 Gemini API Key |
   | `FRONTEND_URL` | `https://your-app.vercel.app` |
   | `ENVIRONMENT` | `production` |

5. 點擊 **Create Web Service**

> ⚠️ **注意**: Render 的 PostgreSQL URL 格式為 `postgresql://...`，需要改為 `postgresql+asyncpg://...` 以支援 asyncpg 驅動

---

## 🧪 測試策略與品質保證

嚴格的測試流程確保系統穩定性，目前的測試覆蓋率涵蓋核心業務邏輯與邊界情況：

### 1. 自動化測試範疇 (`apps/api/app/tests/`)
我們使用 **Pytest** 搭配 **Asyncio** 進行完整的非同步測試：

| 測試模組 | 測試內容與目的 | 關鍵測試案例 |
|---------|---------------|-------------|
| **AI Trigger** | 驗證 LLM 觸發邏輯 | • Mock LLM Provider 避免消耗額度<br>• 輸入字元數驗證 (Max 300 chars)<br>• 自動建立/綁定 Conversation 機制 |
| **Conversations** | 對話管理 CRUD | • 建立、讀取、刪除對話<br>• 404 錯誤處理邏輯<br>• 分頁 (Pagination) 功能驗證 |
| **Rate Limiter** | API 流量限制機制 | • 每日請求次數限制 (3次/IP)<br>• Token 用量限制<br>• Admin IP 白名單繞過測試<br>• Health Check 不受限驗證 |
| **Health Check** | 服務存活監控 | • 驗證服務啟動狀態<br>• 確認無額外依賴阻擋 |

### 2. 測試執行
```bash
cd apps/api
# 執行所有測試並顯示詳細資訊
pytest app/tests/ -v

# 產生覆蓋率報告
pytest --cov=app app/tests/
```

---

## 🛡️ Sentry 系統監控

生產環境整合 **Sentry** 進行錯誤追蹤。

### 監控範圍
- **全域異常捕獲**: 自動攔截未被捕獲的 `500 Internal Server Error` (Level: **Error**)。
- **Sentry Logging 整合**: 
    - `logger.error()` -> **Error** 事件 (系統崩潰、資料庫連線失敗)
    - `logger.warning()` -> **Warning** 事件 (API Rate Limit 接近上限、非預期操作)
    - `logger.info()` -> **Breadcrumbs** (操作歷程記錄)
- **FastAPI 整合**: 紀錄完整的 Request Context (URL, Headers, Method, Body)。
- **SQLAlchemy 整合**: 追蹤資料庫查詢效能與連線錯誤。

### 錯誤處理流程
1. **攔截**: Global Exception Handler 捕獲異常。
2. **紀錄**: 將 Stack Trace 與 Context 上傳至 Sentry。
3. **回饋**: API 回傳標準化的 JSON 錯誤訊息給前端，避免洩漏敏感堆疊資訊。


### 🔴 Redis - Upstash

1. 登入 [Upstash](https://upstash.com)
2. 建立新的 Redis Database
3. 選擇區域 (建議與 Backend 相同區域)
4. 複製 **UPSTASH_REDIS_REST_URL** 或 **Redis URL**
5. 在 Render 設定 `REDIS_URL` 環境變數

---

## 🔧 環境變數設定

### Frontend (`apps/ai-web/.env`)

```env
# Backend API URL
VITE_API_URL=http://localhost:8000          # 本地開發
# VITE_API_URL=https://your-api.onrender.com # 生產環境
```

### Backend (`apps/api/.env`)

```env
# AI API Keys
GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key

# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/aiapp

# Redis
REDIS_URL=redis://localhost:6379/0

# Rate Limiting Admin (bypass rate limit)
ADMIN_IPS=127.0.0.1,::1

# CORS
FRONTEND_URL=http://localhost:3000

# Environment
ENVIRONMENT=development
```

---

## 📁 專案結構

```
aiApp/
├── apps/
│   ├── ai-web/                 # 🎨 前端應用
│   │   ├── src/
│   │   │   ├── components/     # 共用元件
│   │   │   ├── features/       # 功能模組 (chat, etc.)
│   │   │   ├── routes/         # 頁面路由
│   │   │   ├── ui/             # UI 元件 (Radix + shadcn)
│   │   │   └── lib/            # 工具函數
│   │   └── package.json
│   │
│   └── api/                    # ⚡ 後端 API
│       ├── app/
│       │   ├── api/v1/         # API 路由
│       │   │   ├── ai/         # AI 對話 endpoints
│       │   │   ├── conversations/
│       │   │   └── admin/
│       │   ├── services/       # 業務邏輯
│       │   │   ├── llm/        # LLM 服務封裝
│       │   │   └── stream/     # SSE 串流處理
│       │   ├── models/         # SQLAlchemy Models
│       │   ├── db/             # 資料庫連線 & 遷移
│       │   └── infra/          # 中介層 (Rate Limit)
│       ├── alembic/            # 資料庫遷移腳本
│       └── requirements.txt
│
├── packages/                   # 共享套件
│   ├── ui/                     # 共用 UI 元件庫
│   ├── eslint-config/          # ESLint 配置
│   └── typescript-config/      # TypeScript 配置
│
├── docker-compose.yml          # 本地開發環境
├── turbo.json                  # Turborepo 配置
└── pnpm-workspace.yaml         # pnpm 工作區配置
```

---

## 📜 License

This project is licensed under the MIT License.

---

<div align="center">

**Built with ❤️ by Jeff**

[GitHub](https://github.com/your-username) • [LinkedIn](https://linkedin.com/in/your-profile)

</div>
