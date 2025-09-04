# ⚙️ 配置選項

本指南詳細介紹如何自定義配置每日自動更新系統。

## 📋 配置文件概述

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
    "github_username": "your-username",
    "commit_message_template": "🤖 每日自動更新 - {date} {time} (Asia/Taipei)"
  },
  "github_actions": {
    "schedule": "0 1 * * *",
    "timezone": "UTC",
    "python_version": "3.9",
    "auto_push": true
  },
  "notifications": {
    "enable_logs": true,
    "log_level": "INFO"
  }
}
```

## 🕐 時間配置

### 時區設置

```json
{
  "update_config": {
    "timezone": "Asia/Taipei"  // 台灣時區
  }
}
```

**支持的時區**：
- `Asia/Taipei` - 台灣時區 (UTC+8)
- `Asia/Shanghai` - 中國時區 (UTC+8)
- `Asia/Tokyo` - 日本時區 (UTC+9)
- `America/New_York` - 美東時區 (UTC-5)
- `Europe/London` - 英國時區 (UTC+0)

### 更新時間

```json
{
  "update_config": {
    "update_time": "09:00"  // 每天 9:00 執行
  }
}
```

### GitHub Actions 調度

編輯 `.github/workflows/daily-update.yml`：

```yaml
schedule:
  - cron: '0 1 * * *'  # 每天台灣時間 9:00 (UTC 01:00)
```

**常用 Cron 表達式**：
- `'0 1 * * *'` - 每天台灣時間 9:00
- `'0 9 * * *'` - 每天台灣時間 17:00
- `'0 17 * * *'` - 每天台灣時間 1:00
- `'0 0 * * 1'` - 每週一台灣時間 8:00
- `'0 0 1 * *'` - 每月 1 號台灣時間 8:00

## 📁 文件配置

### 要更新的文件

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

### 日誌目錄

```json
{
  "update_config": {
    "log_directory": "daily_logs"  // 日誌保存目錄
  }
}
```

## 🔧 GitHub Actions 配置

### Python 版本

編輯 `.github/workflows/daily-update.yml`：

```yaml
- name: 設置 Python 環境
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'  # 修改為您需要的版本
```

**支持的版本**：
- `3.9`
- `3.10`
- `3.11`
- `3.12`

### 自動推送設置

```json
{
  "github_actions": {
    "auto_push": true  // 是否自動推送變更
  }
}
```

## 📝 提交信息配置

### 提交信息模板

```json
{
  "update_config": {
    "commit_message_template": "🤖 每日自動更新 - {date} {time} (Asia/Taipei)"
  }
}
```

**可用變量**：
- `{date}` - 日期 (YYYY-MM-DD)
- `{time}` - 時間 (HH:MM)
- `{timezone}` - 時區

**示例模板**：
- `"🤖 每日自動更新 - {date} {time} (Asia/Taipei)"`
- `"📅 自動更新時間戳 - {date}"`
- `"🔄 每日同步 - {date} {time}"`

## 🔔 通知配置

### 日誌設置

```json
{
  "notifications": {
    "enable_logs": true,    // 是否啟用日誌
    "log_level": "INFO"     // 日誌級別
  }
}
```

**日誌級別**：
- `DEBUG` - 詳細調試信息
- `INFO` - 一般信息
- `WARNING` - 警告信息
- `ERROR` - 錯誤信息

## 🎨 自定義擴展

### 添加新的更新邏輯

編輯 `update_daily_info.py`：

```python
def custom_update_function(self):
    """自定義更新函數"""
    # 添加您的自定義邏輯
    pass

def run_update(self):
    """執行所有更新操作"""
    print(f"🚀 開始每日更新 - {self.date_str} {self.time_str}")
    print("=" * 50)
    
    try:
        self.update_readme()
        self.update_profile()
        self.custom_update_function()  # 添加自定義更新
        self.create_daily_log()
        
        print("=" * 50)
        print("✅ 所有更新完成！")
        
    except Exception as e:
        print(f"❌ 更新過程中發生錯誤: {e}")
        raise
```

### 添加新的統計資訊

```python
def get_custom_stats(self) -> Dict[str, Any]:
    """獲取自定義統計資訊"""
    try:
        # 添加您的統計邏輯
        return {
            "custom_metric": "value",
            "another_metric": "value"
        }
    except Exception as e:
        print(f"獲取自定義統計資訊時發生錯誤: {e}")
        return {}
```

## 🔍 配置驗證

### 驗證配置文件

```bash
# 檢查 JSON 語法
python3 -m json.tool config.json

# 測試配置加載
python3 -c "
import json
with open('config.json', 'r') as f:
    config = json.load(f)
    print('配置加載成功:', config)
"
```

### 測試配置變更

1. 修改配置文件
2. 提交變更到 GitHub
3. 手動觸發 GitHub Actions
4. 檢查執行結果

## 📊 配置最佳實踐

### 1. 備份配置

```bash
# 備份配置文件
cp config.json config.json.backup
```

### 2. 版本控制

將配置文件加入 Git 版本控制：

```bash
git add config.json
git commit -m "更新配置文件"
```

### 3. 環境特定配置

為不同環境創建不同配置：

```bash
# 開發環境
cp config.json config.dev.json

# 生產環境
cp config.json config.prod.json
```

## 🚨 配置注意事項

### 1. 時區一致性

確保所有時間相關配置使用相同的時區：
- `config.json` 中的 `timezone`
- GitHub Actions 中的 cron 表達式
- 提交信息中的時區標記

### 2. 文件路徑

確保文件路徑正確：
- 使用相對路徑
- 檢查文件是否存在
- 確認文件編碼為 UTF-8

### 3. 權限設置

確保 GitHub Actions 具有必要權限：
- 讀取倉庫內容
- 提交變更
- 推送代碼

## 🎯 下一步

- [手動執行](manual-execution.md) - 詳細的手動執行說明
- [API 參考](../reference/api.md) - 腳本 API 說明
- [故障排除](../reference/troubleshooting.md) - 問題解決

---

**需要幫助？** 查看 [故障排除指南](../reference/troubleshooting.md)
