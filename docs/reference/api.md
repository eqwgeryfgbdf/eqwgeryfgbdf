# 📚 API 參考

本文件詳細介紹每日自動更新系統的 API 接口和腳本功能。

## 🐍 Python 腳本 API

### DailyUpdater 類

主要的更新器類，負責執行所有更新操作。

#### 初始化

```python
updater = DailyUpdater()
```

**功能**：
- 設置台灣時區 (UTC+8)
- 獲取當前時間
- 格式化日期和時間字符串

#### 主要方法

##### `get_github_stats() -> Dict[str, Any]`

獲取 GitHub 統計資訊。

**返回值**：
```python
{
    "profile_views": "1,234",
    "last_activity": "2025-01-27 10:30",
    "commit_count": "156"
}
```

**示例**：
```python
stats = updater.get_github_stats()
print(f"Profile views: {stats['profile_views']}")
```

##### `update_readme()`

更新 README.md 文件。

**功能**：
- 更新最後更新時間戳
- 更新 GitHub 統計資訊（如果配置）
- 保持其他內容不變

**示例**：
```python
updater.update_readme()
```

##### `update_profile()`

更新個人經歷文件。

**功能**：
- 更新最後更新時間戳
- 保持其他內容不變

**示例**：
```python
updater.update_profile()
```

##### `create_daily_log()`

創建每日日誌文件。

**功能**：
- 在 `daily_logs/` 目錄下生成日誌文件
- 文件名格式：`YYYY-MM-DD.md`
- 包含更新時間、變更內容等詳細資訊

**示例**：
```python
updater.create_daily_log()
```

##### `run_update()`

執行所有更新操作。

**功能**：
- 按順序執行所有更新方法
- 提供詳細的執行日誌
- 錯誤處理和異常捕獲

**示例**：
```python
updater.run_update()
```

## ⚙️ 配置文件 API

### config.json 結構

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

### 配置字段說明

#### update_config

| 字段 | 類型 | 說明 | 默認值 |
|------|------|------|--------|
| `timezone` | string | 時區設置 | "Asia/Taipei" |
| `update_time` | string | 更新時間 | "09:00" |
| `files_to_update` | array | 要更新的文件列表 | ["README.md", "個人經歷-已填寫.md"] |
| `log_directory` | string | 日誌保存目錄 | "daily_logs" |
| `github_username` | string | GitHub 用戶名 | "your-username" |
| `commit_message_template` | string | 提交信息模板 | "🤖 每日自動更新 - {date} {time} (Asia/Taipei)" |

#### github_actions

| 字段 | 類型 | 說明 | 默認值 |
|------|------|------|--------|
| `schedule` | string | Cron 表達式 | "0 1 * * *" |
| `timezone` | string | UTC 時區 | "UTC" |
| `python_version` | string | Python 版本 | "3.9" |
| `auto_push` | boolean | 是否自動推送 | true |

#### notifications

| 字段 | 類型 | 說明 | 默認值 |
|------|------|------|--------|
| `enable_logs` | boolean | 是否啟用日誌 | true |
| `log_level` | string | 日誌級別 | "INFO" |

## 🔧 GitHub Actions API

### 工作流程文件

`.github/workflows/daily-update.yml`

#### 觸發條件

```yaml
on:
  schedule:
    - cron: '0 1 * * *'  # 每天台灣時間 9:00
  workflow_dispatch:     # 手動觸發
```

#### 執行環境

```yaml
jobs:
  daily-update:
    runs-on: ubuntu-latest
```

#### 執行步驟

1. **檢出代碼**
   ```yaml
   - name: 檢出代碼
     uses: actions/checkout@v4
   ```

2. **設置 Python 環境**
   ```yaml
   - name: 設置 Python 環境
     uses: actions/setup-python@v4
     with:
       python-version: '3.9'
   ```

3. **安裝依賴**
   ```yaml
   - name: 安裝依賴
     run: |
       python -m pip install --upgrade pip
       pip install requests
   ```

4. **執行更新腳本**
   ```yaml
   - name: 執行每日更新腳本
     run: |
       python update_daily_info.py
   ```

5. **檢查文件變更**
   ```yaml
   - name: 檢查文件變更
     id: verify-changes
     run: |
       if [ -n "$(git status --porcelain)" ]; then
         echo "changes=true" >> $GITHUB_OUTPUT
       else
         echo "changes=false" >> $GITHUB_OUTPUT
       fi
   ```

6. **提交和推送變更**
   ```yaml
   - name: 提交變更
     if: steps.verify-changes.outputs.changes == 'true'
     run: |
       git add .
       git commit -m "🤖 每日自動更新 - $(date '+%Y-%m-%d %H:%M') (Asia/Taipei)"
   
   - name: 推送變更
     if: steps.verify-changes.outputs.changes == 'true'
     run: |
       git push origin main
   ```

## 📝 日誌格式 API

### 每日日誌格式

文件路徑：`daily_logs/YYYY-MM-DD.md`

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

### 更新記錄格式

#### README.md 更新記錄

```markdown
## 更新紀錄
- 2025-01-27：自動更新時間戳與統計資訊（Asia/Taipei 09:00）
```

#### 個人經歷文件更新記錄

```markdown
更新紀錄
- 2025-01-27：自動更新時間戳與統計資訊（Asia/Taipei 09:00）
```

## 🔌 擴展 API

### 自定義更新函數

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

### 自定義統計資訊

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

### 自定義日誌格式

```python
def create_custom_log(self):
    """創建自定義日誌格式"""
    log_dir = "custom_logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, f"{self.date_str}.json")
    
    log_data = {
        "date": self.date_str,
        "time": self.time_str,
        "timezone": "Asia/Taipei",
        "updates": [
            "README.md",
            "個人經歷-已填寫.md"
        ],
        "status": "success"
    }
    
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 已創建自定義日誌: {log_file}")
```

## 🚨 錯誤處理 API

### 異常類型

```python
class DailyUpdateError(Exception):
    """每日更新錯誤基類"""
    pass

class FileUpdateError(DailyUpdateError):
    """文件更新錯誤"""
    pass

class GitOperationError(DailyUpdateError):
    """Git 操作錯誤"""
    pass
```

### 錯誤處理示例

```python
def safe_update(self):
    """安全的更新操作"""
    try:
        self.update_readme()
    except FileNotFoundError as e:
        print(f"❌ 文件未找到: {e}")
        raise FileUpdateError(f"README.md 文件未找到: {e}")
    except PermissionError as e:
        print(f"❌ 權限錯誤: {e}")
        raise FileUpdateError(f"沒有權限更新文件: {e}")
    except Exception as e:
        print(f"❌ 未知錯誤: {e}")
        raise DailyUpdateError(f"更新過程中發生未知錯誤: {e}")
```

## 📊 性能監控 API

### 執行時間監控

```python
import time

def run_update_with_timing(self):
    """帶時間監控的更新操作"""
    start_time = time.time()
    
    try:
        self.run_update()
        end_time = time.time()
        execution_time = end_time - start_time
        
        print(f"⏱️ 執行時間: {execution_time:.2f} 秒")
        
        # 記錄執行時間到日誌
        self.log_execution_time(execution_time)
        
    except Exception as e:
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"❌ 執行失敗，耗時: {execution_time:.2f} 秒")
        raise

def log_execution_time(self, execution_time):
    """記錄執行時間"""
    log_file = os.path.join(self.log_directory, "performance.log")
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"{self.date_str} {self.time_str}: {execution_time:.2f}s\n")
```

## 🎯 下一步

- [配置文件](config.md) - 配置文件格式詳解
- [故障排除](troubleshooting.md) - 問題解決指南

---

**需要幫助？** 查看 [故障排除指南](troubleshooting.md)
