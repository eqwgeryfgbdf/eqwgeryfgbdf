# ⚙️ 配置文件參考

本文件詳細介紹每日自動更新系統的配置文件格式和選項。

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

## 🔧 配置選項詳解

### update_config

更新相關的配置選項。

#### timezone

**類型**: `string`  
**默認值**: `"Asia/Taipei"`  
**說明**: 系統使用的時區

**支持的值**：
```json
{
  "timezone": "Asia/Taipei"    // 台灣時區 (UTC+8)
}
```

**常用時區**：
- `Asia/Taipei` - 台灣時區 (UTC+8)
- `Asia/Shanghai` - 中國時區 (UTC+8)
- `Asia/Tokyo` - 日本時區 (UTC+9)
- `America/New_York` - 美東時區 (UTC-5)
- `Europe/London` - 英國時區 (UTC+0)

#### update_time

**類型**: `string`  
**默認值**: `"09:00"`  
**說明**: 每日更新的時間（24小時制）

**格式**: `HH:MM`

**示例**：
```json
{
  "update_time": "09:00"    // 每天 9:00
}
```

#### files_to_update

**類型**: `array`  
**默認值**: `["README.md", "個人經歷-已填寫.md"]`  
**說明**: 要更新的文件列表

**格式**: 文件路徑數組

**示例**：
```json
{
  "files_to_update": [
    "README.md",
    "個人經歷-已填寫.md",
    "其他文件.md"
  ]
}
```

#### log_directory

**類型**: `string`  
**默認值**: `"daily_logs"`  
**說明**: 日誌文件保存目錄

**示例**：
```json
{
  "log_directory": "daily_logs"
}
```

#### github_username

**類型**: `string`  
**默認值**: `"your-username"`  
**說明**: GitHub 用戶名

**示例**：
```json
{
  "github_username": "eqwgeryfgbdf"
}
```

#### commit_message_template

**類型**: `string`  
**默認值**: `"🤖 每日自動更新 - {date} {time} (Asia/Taipei)"`  
**說明**: 提交信息的模板

**可用變量**：
- `{date}` - 日期 (YYYY-MM-DD)
- `{time}` - 時間 (HH:MM)
- `{timezone}` - 時區

**示例**：
```json
{
  "commit_message_template": "🤖 每日自動更新 - {date} {time} (Asia/Taipei)"
}
```

### github_actions

GitHub Actions 相關的配置選項。

#### schedule

**類型**: `string`  
**默認值**: `"0 1 * * *"`  
**說明**: Cron 表達式，定義執行時間

**格式**: `分 時 日 月 週`

**示例**：
```json
{
  "schedule": "0 1 * * *"    // 每天台灣時間 9:00 (UTC 01:00)
}
```

**常用 Cron 表達式**：
- `'0 1 * * *'` - 每天台灣時間 9:00
- `'0 9 * * *'` - 每天台灣時間 17:00
- `'0 17 * * *'` - 每天台灣時間 1:00
- `'0 0 * * 1'` - 每週一台灣時間 8:00
- `'0 0 1 * *'` - 每月 1 號台灣時間 8:00

#### timezone

**類型**: `string`  
**默認值**: `"UTC"`  
**說明**: GitHub Actions 使用的時區

**示例**：
```json
{
  "timezone": "UTC"
}
```

#### python_version

**類型**: `string`  
**默認值**: `"3.9"`  
**說明**: Python 版本

**支持的值**：
- `"3.9"`
- `"3.10"`
- `"3.11"`
- `"3.12"`

**示例**：
```json
{
  "python_version": "3.11"
}
```

#### auto_push

**類型**: `boolean`  
**默認值**: `true`  
**說明**: 是否自動推送變更

**示例**：
```json
{
  "auto_push": true
}
```

### notifications

通知相關的配置選項。

#### enable_logs

**類型**: `boolean`  
**默認值**: `true`  
**說明**: 是否啟用日誌記錄

**示例**：
```json
{
  "enable_logs": true
}
```

#### log_level

**類型**: `string`  
**默認值**: `"INFO"`  
**說明**: 日誌級別

**支持的值**：
- `"DEBUG"` - 詳細調試信息
- `"INFO"` - 一般信息
- `"WARNING"` - 警告信息
- `"ERROR"` - 錯誤信息

**示例**：
```json
{
  "log_level": "INFO"
}
```

## 📝 配置文件示例

### 基本配置

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
    "github_username": "eqwgeryfgbdf"
  }
}
```

### 完整配置

```json
{
  "update_config": {
    "timezone": "Asia/Taipei",
    "update_time": "09:00",
    "files_to_update": [
      "README.md",
      "個人經歷-已填寫.md",
      "其他文件.md"
    ],
    "log_directory": "daily_logs",
    "github_username": "eqwgeryfgbdf",
    "commit_message_template": "🤖 每日自動更新 - {date} {time} (Asia/Taipei)"
  },
  "github_actions": {
    "schedule": "0 1 * * *",
    "timezone": "UTC",
    "python_version": "3.11",
    "auto_push": true
  },
  "notifications": {
    "enable_logs": true,
    "log_level": "DEBUG"
  }
}
```

### 自定義配置

```json
{
  "update_config": {
    "timezone": "America/New_York",
    "update_time": "17:00",
    "files_to_update": [
      "README.md",
      "profile.md",
      "resume.md"
    ],
    "log_directory": "logs",
    "github_username": "myusername",
    "commit_message_template": "📅 每日更新 - {date} {time}"
  },
  "github_actions": {
    "schedule": "0 22 * * *",
    "timezone": "UTC",
    "python_version": "3.12",
    "auto_push": true
  },
  "notifications": {
    "enable_logs": true,
    "log_level": "WARNING"
  }
}
```

## 🔍 配置文件驗證

### JSON 語法檢查

```bash
# 檢查 JSON 語法
python3 -m json.tool config.json

# 或使用 jq
jq . config.json
```

### 配置加載測試

```python
import json

def test_config():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
            print("✅ 配置文件加載成功")
            print(f"時區: {config['update_config']['timezone']}")
            print(f"更新時間: {config['update_config']['update_time']}")
            print(f"要更新的文件: {config['update_config']['files_to_update']}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON 語法錯誤: {e}")
    except FileNotFoundError:
        print("❌ 配置文件未找到")
    except KeyError as e:
        print(f"❌ 缺少必要的配置項: {e}")

if __name__ == "__main__":
    test_config()
```

### 配置驗證腳本

```python
import json
import os
from datetime import datetime

def validate_config():
    """驗證配置文件"""
    errors = []
    warnings = []
    
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(f"JSON 語法錯誤: {e}")
        return errors, warnings
    except FileNotFoundError:
        errors.append("配置文件未找到")
        return errors, warnings
    
    # 檢查必要的配置項
    required_fields = [
        'update_config.timezone',
        'update_config.update_time',
        'update_config.files_to_update'
    ]
    
    for field in required_fields:
        keys = field.split('.')
        value = config
        try:
            for key in keys:
                value = value[key]
        except KeyError:
            errors.append(f"缺少必要的配置項: {field}")
    
    # 檢查時區格式
    if 'update_config' in config and 'timezone' in config['update_config']:
        timezone = config['update_config']['timezone']
        if not isinstance(timezone, str):
            errors.append("時區必須是字符串")
    
    # 檢查時間格式
    if 'update_config' in config and 'update_time' in config['update_config']:
        update_time = config['update_config']['update_time']
        try:
            datetime.strptime(update_time, '%H:%M')
        except ValueError:
            errors.append("更新時間格式錯誤，應為 HH:MM")
    
    # 檢查文件是否存在
    if 'update_config' in config and 'files_to_update' in config['update_config']:
        files = config['update_config']['files_to_update']
        for file in files:
            if not os.path.exists(file):
                warnings.append(f"文件不存在: {file}")
    
    return errors, warnings

if __name__ == "__main__":
    errors, warnings = validate_config()
    
    if errors:
        print("❌ 配置錯誤:")
        for error in errors:
            print(f"  - {error}")
    
    if warnings:
        print("⚠️ 配置警告:")
        for warning in warnings:
            print(f"  - {warning}")
    
    if not errors and not warnings:
        print("✅ 配置文件驗證通過")
```

## 🔄 配置文件管理

### 備份配置

```bash
# 備份配置文件
cp config.json config.json.backup

# 創建帶時間戳的備份
cp config.json "config.$(date +%Y%m%d_%H%M%S).json"
```

### 版本控制

```bash
# 將配置文件加入版本控制
git add config.json
git commit -m "更新配置文件"

# 查看配置變更歷史
git log --oneline config.json
```

### 環境特定配置

```bash
# 創建不同環境的配置
cp config.json config.dev.json
cp config.json config.prod.json

# 使用特定配置
ln -sf config.prod.json config.json
```

## 🚨 配置注意事項

### 1. 時區一致性

確保所有時間相關配置使用相同的時區：
- `config.json` 中的 `timezone`
- GitHub Actions 中的 cron 表達式
- 提交信息中的時區標記

### 2. 文件路徑

- 使用相對路徑
- 檢查文件是否存在
- 確認文件編碼為 UTF-8

### 3. 權限設置

確保 GitHub Actions 具有必要權限：
- 讀取倉庫內容
- 提交變更
- 推送代碼

### 4. 配置更新

修改配置後：
1. 驗證配置文件語法
2. 提交變更到 GitHub
3. 手動觸發 GitHub Actions 測試

## 🎯 下一步

- [API 參考](api.md) - 腳本 API 說明
- [故障排除](troubleshooting.md) - 問題解決指南

---

**需要幫助？** 查看 [故障排除指南](troubleshooting.md)
