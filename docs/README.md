# 📚 每日自動更新系統文檔

歡迎使用每日自動更新系統！這個系統會自動更新您的 GitHub 個人資料和履歷文件，並通過 GitHub Actions 進行每日自動化部署。

## 📖 文檔導航

### 🚀 快速開始
- [安裝指南](setup/installation.md) - 系統安裝和配置
- [部署指南](setup/deployment.md) - GitHub Actions 部署
- [YAML 部署指南](setup/yaml-deployment.md) - 多種 YAML 部署方式
- [快速開始](usage/quick-start.md) - 5分鐘快速上手

### 📋 使用指南
- [基本使用](usage/basic-usage.md) - 日常使用說明
- [配置選項](usage/configuration.md) - 自定義配置
- [手動執行](usage/manual-execution.md) - 本地測試和手動執行

### 🔧 參考資料
- [API 參考](reference/api.md) - 腳本 API 說明
- [配置文件](reference/config.md) - 配置文件格式
- [故障排除](reference/troubleshooting.md) - 常見問題解決

## 🎯 系統特色

- ✅ **自動時間戳更新**：每日自動更新 README.md 和個人經歷文件中的時間戳
- ✅ **GitHub Actions 集成**：使用 GitHub Actions 進行自動化部署
- ✅ **台灣時區支持**：使用 Asia/Taipei 時區
- ✅ **智能變更檢測**：只有當文件實際發生變更時才會提交和推送
- ✅ **詳細日誌記錄**：生成每日更新日誌文件
- ✅ **手動執行支持**：支持本地測試和手動執行

## 📁 項目結構

```
├── .github/workflows/
│   └── daily-update.yml          # GitHub Actions 工作流程
├── docs/                         # 📚 文檔目錄
│   ├── setup/                    # 安裝和部署指南
│   ├── usage/                    # 使用指南
│   ├── reference/                # 參考資料
│   └── README.md                 # 文檔索引（本文件）
├── daily_logs/                   # 每日日誌目錄（自動生成）
├── update_daily_info.py          # 主要更新腳本
├── run_update.sh                 # 手動執行腳本
├── requirements.txt              # Python 依賴
├── config.json                   # 配置文件
├── README.md                     # 項目主頁
└── 個人經歷-已填寫.md            # 個人履歷文件
```

## 🚀 快速開始

1. **查看安裝指南**：[安裝指南](setup/installation.md)
2. **部署到 GitHub**：[部署指南](setup/deployment.md)
3. **開始使用**：[快速開始](usage/quick-start.md)

## 📞 支援

如有問題或建議，請：
- 查看 [故障排除指南](reference/troubleshooting.md)
- 創建 GitHub Issue
- 聯繫：lungyuchengroy@gmail.com

---

**最後更新**：2025-01-27  
**版本**：1.0.0
