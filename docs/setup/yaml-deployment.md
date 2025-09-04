# 🐳 YAML 格式部署指南

本指南詳細介紹如何使用 YAML 格式部署每日自動更新系統到不同的環境。

## 📋 部署選項

### 1. GitHub Actions (推薦)
- **文件**: `.github/workflows/daily-update.yml`
- **用途**: 自動化部署和執行
- **環境**: GitHub 雲端環境

### 2. Docker Compose
- **文件**: `docker-compose.yml`
- **用途**: 本地開發和測試
- **環境**: 本地 Docker 環境

### 3. Kubernetes
- **文件**: `k8s/*.yml`
- **用途**: 生產環境部署
- **環境**: Kubernetes 集群

## 🚀 GitHub Actions 部署

### 配置文件

`.github/workflows/daily-update.yml`:

```yaml
name: 每日自動更新

on:
  schedule:
    - cron: '0 1 * * *'  # 每天台灣時間 9:00
  workflow_dispatch:
    inputs:
      custom_message:
        description: '自定義提交信息'
        required: false
        default: '🤖 手動觸發每日更新'
        type: string

env:
  TZ: Asia/Taipei
  PYTHON_VERSION: '3.11'

jobs:
  daily-update:
    name: 執行每日更新
    runs-on: ubuntu-latest
    timeout-minutes: 10
    
    permissions:
      contents: write
      actions: read
    
    steps:
      - name: 📥 檢出代碼
        uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          fetch-depth: 0
      
      - name: 🐍 設置 Python 環境
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'
      
      - name: 📦 安裝依賴
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: 🚀 執行每日更新腳本
        run: |
          python update_daily_info.py
      
      # ... 其他步驟
```

### 部署步驟

1. **推送代碼**:
   ```bash
   git add .github/workflows/daily-update.yml
   git commit -m "添加 GitHub Actions 工作流程"
   git push origin main
   ```

2. **啟用 Actions**:
   - 前往 GitHub 倉庫的 "Actions" 頁面
   - 啟用 "每日自動更新" 工作流程

3. **手動測試**:
   - 在 Actions 頁面手動觸發執行
   - 檢查執行結果

## 🐳 Docker Compose 部署

### 配置文件

`docker-compose.yml`:

```yaml
version: '3.8'

services:
  daily-updater:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: daily-updater
    environment:
      - TZ=Asia/Taipei
      - PYTHON_VERSION=3.11
    volumes:
      - .:/app
      - ./daily_logs:/app/daily_logs
    working_dir: /app
    command: python update_daily_info.py
    restart: "no"
    
  dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    container_name: daily-updater-dev
    environment:
      - TZ=Asia/Taipei
      - PYTHON_VERSION=3.11
      - ENV=development
    volumes:
      - .:/app
      - ./daily_logs:/app/daily_logs
    working_dir: /app
    command: tail -f /dev/null
    ports:
      - "8000:8000"
    restart: unless-stopped
```

### 部署步驟

1. **構建和運行**:
   ```bash
   # 構建並運行
   docker-compose up --build
   
   # 後台運行
   docker-compose up -d --build
   
   # 只運行開發環境
   docker-compose up dev
   ```

2. **查看日誌**:
   ```bash
   docker-compose logs -f daily-updater
   ```

3. **停止服務**:
   ```bash
   docker-compose down
   ```

## ☸️ Kubernetes 部署

### 配置文件

`k8s/deployment.yml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: daily-updater
  namespace: default
  labels:
    app: daily-updater
    version: v1.0.0
spec:
  replicas: 1
  selector:
    matchLabels:
      app: daily-updater
  template:
    metadata:
      labels:
        app: daily-updater
        version: v1.0.0
    spec:
      containers:
      - name: daily-updater
        image: daily-updater:latest
        imagePullPolicy: IfNotPresent
        env:
        - name: TZ
          value: "Asia/Taipei"
        - name: PYTHON_VERSION
          value: "3.11"
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        volumeMounts:
        - name: config-volume
          mountPath: /app/config.json
          subPath: config.json
        - name: logs-volume
          mountPath: /app/daily_logs
      volumes:
      - name: config-volume
        configMap:
          name: daily-updater-config
      - name: logs-volume
        persistentVolumeClaim:
          claimName: daily-updater-logs
```

### 部署步驟

1. **使用部署腳本**:
   ```bash
   # 部署到 Kubernetes
   ./k8s/deploy.sh deploy
   
   # 查看狀態
   ./k8s/deploy.sh status
   
   # 查看日誌
   ./k8s/deploy.sh logs
   
   # 清理部署
   ./k8s/deploy.sh cleanup
   ```

2. **手動部署**:
   ```bash
   # 創建命名空間
   kubectl apply -f k8s/namespace.yml
   
   # 部署應用
   kubectl apply -f k8s/deployment.yml
   
   # 部署服務
   kubectl apply -f k8s/service.yml
   
   # 檢查狀態
   kubectl get pods -n daily-updater
   ```

## 🔍 YAML 配置驗證

### 驗證腳本

使用提供的驗證腳本檢查所有 YAML 文件:

```bash
# 驗證所有 YAML 文件
./validate-yaml.sh

# 驗證特定文件
yq eval '.' .github/workflows/daily-update.yml
```

### 驗證內容

- **YAML 語法**: 檢查語法正確性
- **Kubernetes 配置**: 驗證 K8s 資源定義
- **Docker Compose**: 驗證服務配置
- **GitHub Actions**: 檢查工作流程結構

## ⚙️ 配置自定義

### 環境變量

所有部署方式都支持以下環境變量:

```yaml
env:
  TZ: Asia/Taipei              # 時區
  PYTHON_VERSION: '3.11'       # Python 版本
  ENV: production              # 環境類型
  LOG_LEVEL: INFO              # 日誌級別
```

### 資源限制

Kubernetes 部署中的資源限制:

```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "200m"
```

### 健康檢查

Docker 和 Kubernetes 都支持健康檢查:

```yaml
# Docker
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import update_daily_info; print('Health check passed')" || exit 1

# Kubernetes
livenessProbe:
  exec:
    command:
    - python
    - -c
    - "import update_daily_info; print('OK')"
  initialDelaySeconds: 30
  periodSeconds: 60
```

## 🚨 故障排除

### 常見問題

1. **YAML 語法錯誤**:
   ```bash
   # 使用 yq 驗證
   yq eval '.' your-file.yml
   
   # 使用 Python 驗證
   python3 -c "import yaml; yaml.safe_load(open('your-file.yml'))"
   ```

2. **Kubernetes 部署失敗**:
   ```bash
   # 檢查 Pod 狀態
   kubectl get pods -n daily-updater
   
   # 查看 Pod 日誌
   kubectl logs -l app=daily-updater -n daily-updater
   
   # 檢查事件
   kubectl get events -n daily-updater
   ```

3. **Docker Compose 問題**:
   ```bash
   # 檢查服務狀態
   docker-compose ps
   
   # 查看日誌
   docker-compose logs
   
   # 重新構建
   docker-compose up --build --force-recreate
   ```

### 調試技巧

1. **啟用詳細日誌**:
   ```yaml
   env:
     LOG_LEVEL: DEBUG
   ```

2. **使用調試模式**:
   ```bash
   # Docker
   docker-compose -f docker-compose.yml -f docker-compose.debug.yml up
   
   # Kubernetes
   kubectl run debug-pod --image=busybox --rm -it -- /bin/sh
   ```

## 📊 監控和日誌

### 日誌收集

所有部署方式都會生成日誌:

- **GitHub Actions**: 在 Actions 頁面查看
- **Docker**: 使用 `docker-compose logs`
- **Kubernetes**: 使用 `kubectl logs`

### 監控指標

- 執行時間
- 成功率
- 錯誤率
- 資源使用情況

## 🎯 最佳實踐

### 1. 配置管理

- 使用 ConfigMap 管理配置
- 環境變量分離敏感信息
- 版本控制所有配置文件

### 2. 安全性

- 最小權限原則
- 使用 ServiceAccount
- 定期更新基礎鏡像

### 3. 可觀測性

- 添加健康檢查
- 配置日誌收集
- 設置監控告警

## 🎯 下一步

- [安裝指南](installation.md) - 系統安裝
- [部署指南](deployment.md) - 詳細部署說明
- [故障排除](../reference/troubleshooting.md) - 問題解決

---

**需要幫助？** 查看 [故障排除指南](../reference/troubleshooting.md)
