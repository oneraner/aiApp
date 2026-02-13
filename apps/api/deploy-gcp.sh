#!/bin/bash
# =============================================================================
# GCP Cloud Run 部署腳本
# 使用方式: ./deploy-gcp.sh
# 前提: 已安裝 gcloud CLI 且已登入 (gcloud auth login)
# =============================================================================

set -e

# ---- 設定 ----
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
REGION="asia-east1"          # 台灣 (彰化)
SERVICE_NAME="aiapp-api"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

if [ -z "$PROJECT_ID" ]; then
  echo "❌ 請先設定 GCP 專案: gcloud config set project YOUR_PROJECT_ID"
  exit 1
fi

echo "🚀 部署到 GCP Cloud Run"
echo "   專案: ${PROJECT_ID}"
echo "   區域: ${REGION}"
echo "   服務: ${SERVICE_NAME}"
echo ""

# ---- Step 1: 啟用必要的 API ----
echo "📦 啟用必要的 GCP API..."
gcloud services enable run.googleapis.com containerregistry.googleapis.com cloudbuild.googleapis.com

# ---- Step 2: Build & Deploy ----
# 使用 gcloud run deploy --source 直接從原始碼部署
# 這會自動 build Docker image 並部署到 Cloud Run
echo "🔨 建構並部署中..."
gcloud run deploy ${SERVICE_NAME} \
  --source . \
  --region ${REGION} \
  --platform managed \
  --allow-unauthenticated \
  --min-instances 0 \
  --max-instances 2 \
  --memory 256Mi \
  --cpu 1 \
  --timeout 300 \
  --set-env-vars "ENVIRONMENT=production"

# ---- Step 3: 取得服務 URL ----
SERVICE_URL=$(gcloud run services describe ${SERVICE_NAME} --region ${REGION} --format 'value(status.url)')

echo ""
echo "✅ 部署完成！"
echo "   服務 URL: ${SERVICE_URL}"
echo ""
echo "📋 接下來你需要："
echo "   1. 在 GCP Console 設定環境變數 (DATABASE_URL, REDIS_URL, GEMINI_API_KEY 等)"
echo "      gcloud run services update ${SERVICE_NAME} --region ${REGION} \\"
echo "        --set-env-vars 'DATABASE_URL=postgresql+asyncpg://...,REDIS_URL=redis://...,GEMINI_API_KEY=...,OPENAI_API_KEY=...,FRONTEND_URL=https://your-app.vercel.app'"
echo ""
echo "   2. 在 Vercel 更新 VITE_API_URL 為: ${SERVICE_URL}"
echo ""
echo "   3. 測試 health check: curl ${SERVICE_URL}/health"
echo "   4. 測試 API docs: ${SERVICE_URL}/docs"
