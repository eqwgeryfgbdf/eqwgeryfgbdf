# 🛠️ 安裝指南

本指南將幫助您安裝和配置每日自動更新系統。

## 📋 系統要求

- **Python**: 3.9 或更高版本
- **Git**: 2.0 或更高版本
- **GitHub 帳戶**: 具有倉庫寫入權限
- **操作系統**: Windows、macOS 或 Linux

## 🔧 安裝步驟

### 1. 檢查 Python 版本

```bash
python3 --version
# 或
python --version
```

如果版本低於 3.9，請先升級 Python。

### 2. 安裝依賴

```bash
# 安裝 Python 依賴
pip3 install -r requirements.txt

# 或手動安裝
pip3 install requests
```

### 3. 驗證安裝

```bash
# 測試腳本執行
python3 update_daily_info.py
```

如果看到以下輸出，表示安裝成功：
```
🚀 開始每日更新 - 2025-01-27 10:00
==================================================
✅ 已更新 README.md
✅ 已更新 個人經歷-已填寫.md
✅ 已創建每日日誌: daily_logs/2025-01-27.md
==================================================
✅ 所有更新完成！
```

## ⚙️ 配置設置

### 1. 編輯配置文件

編輯 `config.json` 文件來自定義設置：

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

### 2. 配置 Git（如果需要）

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 🔍 驗證配置

### 1. 檢查文件結構

確認以下文件存在：
- ✅ `update_daily_info.py`
- ✅ `config.json`
- ✅ `requirements.txt`
- ✅ `README.md`
- ✅ `個人經歷-已填寫.md`

### 2. 測試手動執行

```bash
# 使用手動執行腳本
./run_update.sh

# 或直接執行 Python 腳本
python3 update_daily_info.py
```

### 3. 檢查生成的文件

執行後應該生成：
- ✅ 更新的 README.md（時間戳已更新）
- ✅ 更新的個人經歷文件（時間戳已更新）
- ✅ `daily_logs/YYYY-MM-DD.md` 日誌文件

## 🚨 常見問題

### Python 版本問題

**問題**: `python3: command not found`

**解決方案**:
```bash
# macOS (使用 Homebrew)
brew install python3

# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# Windows
# 從 https://python.org 下載並安裝
```

### 依賴安裝失敗

**問題**: `pip3 install requests` 失敗

**解決方案**:
```bash
# 升級 pip
python3 -m pip install --upgrade pip

# 使用國內鏡像源
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple requests
```

### 權限問題

**問題**: 腳本無法執行

**解決方案**:
```bash
# 給腳本執行權限
chmod +x run_update.sh
chmod +x update_daily_info.py
```

## ✅ 安裝完成檢查清單

- [ ] Python 3.9+ 已安裝
- [ ] 依賴包已安裝
- [ ] 配置文件已設置
- [ ] 手動測試執行成功
- [ ] 文件更新功能正常
- [ ] 日誌生成功能正常

## 🚀 下一步

安裝完成後，請繼續：
1. [部署指南](deployment.md) - 設置 GitHub Actions
2. [快速開始](../usage/quick-start.md) - 開始使用系統

---

**需要幫助？** 查看 [故障排除指南](../reference/troubleshooting.md)
