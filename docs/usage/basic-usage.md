# 📖 基本使用指南

本指南將詳細介紹如何使用每日自動更新系統。

## 🎯 系統概述

每日自動更新系統會：
- 每天台灣時間 9:00 自動執行
- 更新 README.md 和個人經歷文件的時間戳
- 自動提交並推送變更到 GitHub
- 生成詳細的每日日誌

## 📅 自動執行

### 執行時間

系統會每天在以下時間自動執行：
- **台灣時間**: 上午 9:00
- **UTC 時間**: 上午 1:00
- **Cron 表達式**: `0 1 * * *`

### 執行流程

1. **環境準備**: 設置 Python 環境並安裝依賴
2. **執行更新**: 運行 `update_daily_info.py` 腳本
3. **變更檢測**: 檢查是否有文件變更
4. **自動提交**: 如果有變更，自動提交並推送
5. **日誌記錄**: 記錄執行結果和狀態

## 🔧 手動執行

### 本地手動執行

#### 方法 1: 使用手動執行腳本

```bash
# 給腳本執行權限（首次使用）
chmod +x run_update.sh

# 執行腳本
./run_update.sh
```

腳本會：
- 自動安裝依賴
- 執行更新腳本
- 詢問是否要提交並推送變更

#### 方法 2: 直接執行 Python 腳本

```bash
# 安裝依賴
pip3 install -r requirements.txt

# 執行更新腳本
python3 update_daily_info.py
```

### GitHub Actions 手動觸發

1. 前往 GitHub 倉庫的 **"Actions"** 頁面
2. 選擇 **"每日自動更新"** 工作流程
3. 點擊 **"Run workflow"** 按鈕
4. 選擇分支（通常是 `main`）
5. 點擊 **"Run workflow"** 確認執行

## 📊 更新內容

### README.md 更新

系統會更新 README.md 中的：
- 最後更新時間戳
- GitHub 統計資訊（如果配置）

**更新格式**：
```markdown
## 更新紀錄
- 2025-01-27：自動更新時間戳與統計資訊（Asia/Taipei 09:00）
```

### 個人經歷文件更新

系統會更新個人經歷文件中的：
- 最後更新時間戳

**更新格式**：
```markdown
更新紀錄
- 2025-01-27：自動更新時間戳與統計資訊（Asia/Taipei 09:00）
```

### 每日日誌生成

系統會在 `daily_logs/` 目錄下生成每日日誌：

**文件格式**: `YYYY-MM-DD.md`

**日誌內容**：
```markdown
# 每日更新日誌 - 2025-01-27

## 更新時間
- 日期：2025-01-27
- 時間：09:00 (Asia/Taipei)
- 時區：UTC+8

## 更新內容
- ✅ 更新 README.md 時間戳
- ✅ 更新個人經歷文件時間戳
- ✅ 生成每日日誌

## 統計資訊
- 文件更新數量：2
- 更新類型：自動化時間戳更新

## 備註
此更新由 GitHub Actions 自動執行
```

## 🔍 監控和日誌

### GitHub Actions 日誌

1. 前往 GitHub 倉庫的 **"Actions"** 頁面
2. 點擊最新的工作流程執行
3. 查看每個步驟的詳細日誌

**日誌內容包括**：
- 環境設置
- 依賴安裝
- 腳本執行
- 變更檢測
- 提交和推送

### 本地日誌

每日日誌保存在 `daily_logs/` 目錄：
- 文件名格式：`YYYY-MM-DD.md`
- 包含更新時間、變更內容等詳細資訊

## ⚙️ 配置管理

### 配置文件

主要配置文件：`config.json`

```json
{
  "update_config": {
    "timezone": "Asia/Taipei",
    "update_time": "09:00",
    "files_to_update": [
      "README.md",
      "個人經歷-已填寫.md"
    ],
    "log_directory": "daily_logs",
    "github_username": "your-username"
  }
}
```

### 修改配置

1. 編輯 `config.json` 文件
2. 提交變更到 GitHub
3. 下次執行時會使用新配置

## 🚨 故障處理

### 檢查執行狀態

1. **GitHub Actions 頁面**：查看執行狀態和日誌
2. **本地日誌**：檢查 `daily_logs/` 目錄
3. **Git 狀態**：檢查是否有未提交的變更

### 常見問題

1. **執行失敗**
   - 檢查 Python 版本和依賴
   - 查看 Actions 執行日誌

2. **文件未更新**
   - 檢查文件路徑是否正確
   - 確認文件編碼為 UTF-8

3. **推送失敗**
   - 檢查 Git 配置和權限
   - 確認沒有合併衝突

## 📈 最佳實踐

### 1. 定期檢查

- 每週檢查一次 Actions 執行狀態
- 查看每日日誌確保正常運行

### 2. 備份重要文件

- 定期備份 `config.json` 配置文件
- 備份重要的個人資料文件

### 3. 監控變更

- 關注 GitHub 提交歷史
- 檢查自動生成的提交信息

## 🎯 下一步

- [配置選項](configuration.md) - 自定義配置
- [手動執行](manual-execution.md) - 詳細的手動執行說明
- [故障排除](../reference/troubleshooting.md) - 問題解決

---

**需要幫助？** 查看 [故障排除指南](../reference/troubleshooting.md)
