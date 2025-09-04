# ⚡ 快速開始

5分鐘快速上手每日自動更新系統！

## 🎯 目標

在 5 分鐘內設置並運行每日自動更新系統，讓您的 GitHub 個人資料保持最新狀態。

## 📋 前置條件

- ✅ GitHub 帳戶
- ✅ 本地 Git 環境
- ✅ Python 3.9+ 環境

## 🚀 快速設置

### 步驟 1: 推送代碼 (1分鐘)

```bash
# 添加所有文件
git add .

# 提交變更
git commit -m "✨ 添加每日自動更新系統"

# 推送到 GitHub
git push origin main
```

### 步驟 2: 啟用 GitHub Actions (1分鐘)

1. 前往您的 GitHub 倉庫
2. 點擊 **"Actions"** 標籤
3. 找到 **"每日自動更新"** 工作流程
4. 點擊 **"Enable workflow"**

### 步驟 3: 手動測試 (2分鐘)

1. 在 Actions 頁面點擊 **"Run workflow"**
2. 選擇 `main` 分支
3. 點擊 **"Run workflow"** 確認執行
4. 等待執行完成（約 1-2 分鐘）

### 步驟 4: 驗證結果 (1分鐘)

檢查以下內容：
- ✅ Actions 執行狀態為綠色
- ✅ README.md 時間戳已更新
- ✅ 個人經歷文件時間戳已更新
- ✅ 生成了每日日誌文件

## 🎉 完成！

恭喜！您的每日自動更新系統已經開始運行。

### 接下來會發生什麼？

- **每天台灣時間 9:00**：系統會自動執行
- **自動更新**：時間戳會自動更新
- **自動推送**：變更會自動提交並推送
- **日誌記錄**：每次執行都會生成日誌

## 🔧 自定義設置

### 修改執行時間

編輯 `.github/workflows/daily-update.yml`：

```yaml
schedule:
  - cron: '0 1 * * *'  # 修改為您想要的時間
```

### 添加更多文件

編輯 `config.json`：

```json
{
  "update_config": {
    "files_to_update": [
      "README.md",
      "個人經歷-已填寫.md",
      "其他文件.md"  // 添加更多文件
    ]
  }
}
```

## 🚨 常見問題

### Q: Actions 執行失敗怎麼辦？

**A**: 檢查以下項目：
1. 確認所有文件已推送到 GitHub
2. 檢查 Actions 是否已啟用
3. 查看執行日誌中的錯誤信息

### Q: 如何手動觸發更新？

**A**: 在 GitHub Actions 頁面：
1. 選擇 "每日自動更新" 工作流程
2. 點擊 "Run workflow" 按鈕

### Q: 如何停止自動更新？

**A**: 在 GitHub Actions 頁面：
1. 選擇 "每日自動更新" 工作流程
2. 點擊 "Disable workflow"

## 📚 更多資源

- [基本使用](basic-usage.md) - 詳細使用說明
- [配置選項](configuration.md) - 自定義配置
- [故障排除](../reference/troubleshooting.md) - 問題解決

## 🎯 下一步

現在您已經成功設置了每日自動更新系統！建議您：

1. **查看基本使用指南**：[基本使用](basic-usage.md)
2. **自定義配置**：[配置選項](configuration.md)
3. **了解故障排除**：[故障排除](../reference/troubleshooting.md)

---

**需要幫助？** 查看 [故障排除指南](../reference/troubleshooting.md) 或創建 GitHub Issue
