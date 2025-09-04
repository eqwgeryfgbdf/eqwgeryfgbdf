# 🚀 部署指南

本指南將幫助您將每日自動更新系統部署到 GitHub Actions。

## 📋 部署前準備

### 1. 確認文件完整性

確保以下文件已準備就緒：
- ✅ `update_daily_info.py` - 主要更新腳本
- ✅ `.github/workflows/daily-update.yml` - GitHub Actions 工作流程
- ✅ `requirements.txt` - Python 依賴
- ✅ `config.json` - 配置文件
- ✅ `README.md` - 項目主頁
- ✅ `個人經歷-已填寫.md` - 個人履歷文件

### 2. 本地測試

在部署前，請先在本地測試：

```bash
# 測試腳本執行
python3 update_daily_info.py

# 檢查 Git 狀態
git status
```

## 🚀 部署步驟

### 1. 推送代碼到 GitHub

```bash
# 添加所有文件
git add .

# 提交變更
git commit -m "✨ 添加每日自動更新系統"

# 推送到 GitHub
git push origin main
```

### 2. 啟用 GitHub Actions

1. 前往您的 GitHub 倉庫
2. 點擊 **"Actions"** 標籤
3. 確認 **"每日自動更新"** 工作流程已出現
4. 點擊 **"Enable workflow"** 啟用

### 3. 手動測試執行

在 GitHub Actions 頁面：
1. 選擇 **"每日自動更新"** 工作流程
2. 點擊 **"Run workflow"** 按鈕
3. 選擇分支（通常是 `main`）
4. 點擊 **"Run workflow"** 確認執行

### 4. 驗證部署結果

執行完成後，檢查：
- ✅ Actions 執行狀態為綠色（成功）
- ✅ 文件已自動更新
- ✅ 變更已自動提交和推送
- ✅ 生成了每日日誌文件

## ⚙️ 配置選項

### 修改執行時間

編輯 `.github/workflows/daily-update.yml` 中的 cron 表達式：

```yaml
schedule:
  - cron: '0 1 * * *'  # 每天台灣時間 9:00 (UTC 01:00)
```

**常用時間設置**：
- `'0 1 * * *'` - 每天台灣時間 9:00
- `'0 9 * * *'` - 每天台灣時間 17:00
- `'0 17 * * *'` - 每天台灣時間 1:00
- `'0 0 * * 1'` - 每週一台灣時間 8:00

### 修改更新文件

編輯 `config.json` 中的 `files_to_update` 數組：

```json
{
  "update_config": {
    "files_to_update": [
      "README.md",
      "個人經歷-已填寫.md",
      "其他文件.md"
    ]
  }
}
```

### 修改 Python 版本

編輯 `.github/workflows/daily-update.yml`：

```yaml
- name: 設置 Python 環境
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'  # 修改為您需要的版本
```

## 🔍 監控和日誌

### GitHub Actions 日誌

1. 前往 GitHub 倉庫的 **"Actions"** 頁面
2. 點擊最新的工作流程執行
3. 查看每個步驟的詳細日誌

### 本地日誌

每日日誌保存在 `daily_logs/` 目錄：
- 文件名格式：`YYYY-MM-DD.md`
- 包含更新時間、變更內容等詳細資訊

## 🚨 故障排除

### GitHub Actions 執行失敗

**常見原因和解決方案**：

1. **權限問題**
   - 檢查倉庫是否啟用 Actions
   - 確認 `GITHUB_TOKEN` 具有寫入權限

2. **代碼錯誤**
   - 檢查 Python 語法錯誤
   - 確認所有依賴已正確安裝

3. **文件路徑問題**
   - 確認所有文件路徑正確
   - 檢查文件編碼為 UTF-8

### 自動推送失敗

**常見原因和解決方案**：

1. **Git 配置問題**
   ```yaml
   - name: 配置 Git
     run: |
       git config --local user.email "action@github.com"
       git config --local user.name "GitHub Action"
   ```

2. **分支保護規則**
   - 檢查是否有分支保護規則阻止推送
   - 確認 Actions 具有推送權限

3. **合併衝突**
   - 檢查是否有合併衝突
   - 考慮使用 `git pull --rebase` 解決衝突

## 📊 部署檢查清單

- [ ] 所有文件已推送到 GitHub
- [ ] GitHub Actions 已啟用
- [ ] 手動測試執行成功
- [ ] 自動提交和推送功能正常
- [ ] 每日日誌生成正常
- [ ] 定時執行設置正確

## 🎯 預期結果

部署成功後，您將看到：

1. **每日自動執行**：每天台灣時間 9:00 自動運行
2. **自動更新**：README.md 和個人經歷文件的時間戳會自動更新
3. **自動提交**：變更會自動提交並推送到 GitHub
4. **日誌記錄**：在 `daily_logs/` 目錄下生成每日日誌

## 🚀 下一步

部署完成後，請繼續：
1. [快速開始](../usage/quick-start.md) - 開始使用系統
2. [基本使用](../usage/basic-usage.md) - 日常使用說明
3. [配置選項](../usage/configuration.md) - 自定義配置

---

**部署完成後，您的每日自動更新系統就開始運行了！** 🎉

**需要幫助？** 查看 [故障排除指南](../reference/troubleshooting.md)
