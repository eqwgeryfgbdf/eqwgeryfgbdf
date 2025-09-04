# 🖱️ 手動執行指南

本指南詳細介紹如何手動執行每日自動更新系統。

## 🎯 手動執行的場景

手動執行適用於以下場景：
- 本地測試和調試
- 緊急更新需求
- 驗證配置變更
- 故障排除和診斷

## 🖥️ 本地手動執行

### 方法 1: 使用手動執行腳本

#### 首次設置

```bash
# 給腳本執行權限
chmod +x run_update.sh
```

#### 執行腳本

```bash
# 執行手動更新腳本
./run_update.sh
```

#### 腳本功能

手動執行腳本會：
1. 檢查 Python 環境
2. 安裝依賴包
3. 執行更新腳本
4. 檢測文件變更
5. 詢問是否提交並推送

#### 執行示例

```bash
$ ./run_update.sh
🚀 開始執行每日更新腳本...
==================================
📦 安裝 Python 依賴...
Requirement already satisfied: requests in /opt/anaconda3/lib/python3.11/site-packages
🔄 執行更新腳本...
🚀 開始每日更新 - 2025-01-27 10:30
==================================================
✅ 已更新 README.md
✅ 已更新 個人經歷-已填寫.md
✅ 已創建每日日誌: daily_logs/2025-01-27.md
==================================================
✅ 所有更新完成！
📝 檢測到文件變更
變更的文件：
 M README.md
 M 個人經歷-已填寫.md
?? daily_logs/2025-01-27.md
是否要提交並推送變更？(y/n): y
💾 提交變更...
[main abc1234] 🤖 手動執行每日更新 - 2025-01-27 10:30 (Asia/Taipei)
🚀 推送變更...
Enumerating objects: 5, done.
Counting objects: 100% (5/5), done.
Delta compression using up to 8 threads
Compressing objects: 100% (3/3), done.
Writing objects: 100% (3/3), 245 bytes | 245.00 KiB/s, done.
Total 3 (3/3), reused 0 (3/3), remote: 3
To https://github.com/username/repository.git
   def5678..abc1234  main -> main
✅ 更新完成並已推送！
==================================
🎉 腳本執行完成！
```

### 方法 2: 直接執行 Python 腳本

#### 安裝依賴

```bash
# 安裝 Python 依賴
pip3 install -r requirements.txt

# 或手動安裝
pip3 install requests
```

#### 執行腳本

```bash
# 執行更新腳本
python3 update_daily_info.py
```

#### 執行示例

```bash
$ python3 update_daily_info.py
🚀 開始每日更新 - 2025-01-27 10:30
==================================================
✅ 已更新 README.md
✅ 已更新 個人經歷-已填寫.md
✅ 已創建每日日誌: daily_logs/2025-01-27.md
==================================================
✅ 所有更新完成！
```

#### 手動提交變更

```bash
# 檢查變更
git status

# 添加變更
git add .

# 提交變更
git commit -m "🤖 手動執行每日更新 - $(date '+%Y-%m-%d %H:%M') (Asia/Taipei)"

# 推送變更
git push origin main
```

## 🌐 GitHub Actions 手動觸發

### 觸發步驟

1. 前往 GitHub 倉庫
2. 點擊 **"Actions"** 標籤
3. 選擇 **"每日自動更新"** 工作流程
4. 點擊 **"Run workflow"** 按鈕
5. 選擇分支（通常是 `main`）
6. 點擊 **"Run workflow"** 確認執行

### 監控執行

1. 在 Actions 頁面查看執行狀態
2. 點擊執行記錄查看詳細日誌
3. 等待執行完成

### 執行日誌示例

```
✅ 檢出代碼
✅ 設置 Python 環境
✅ 安裝依賴
✅ 執行每日更新腳本
🚀 開始每日更新 - 2025-01-27 10:30
==================================================
✅ 已更新 README.md
✅ 已更新 個人經歷-已填寫.md
✅ 已創建每日日誌: daily_logs/2025-01-27.md
==================================================
✅ 所有更新完成！
✅ 檢查文件變更
📝 檢測到文件變更
✅ 配置 Git
✅ 提交變更
✅ 推送變更
✅ 更新完成通知
```

## 🔧 高級手動執行

### 自定義執行參數

#### 修改執行時間

```python
# 在 update_daily_info.py 中修改
class DailyUpdater:
    def __init__(self, custom_time=None):
        if custom_time:
            self.current_time = custom_time
        else:
            self.taiwan_tz = timezone(timedelta(hours=8))
            self.current_time = datetime.now(self.taiwan_tz)
```

#### 指定更新文件

```python
# 只更新特定文件
updater = DailyUpdater()
updater.update_readme()  # 只更新 README.md
# 跳過其他更新
```

#### 自定義日誌級別

```python
# 設置詳細日誌
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 批量執行

#### 創建批量執行腳本

```bash
#!/bin/bash
# batch_update.sh

echo "🚀 開始批量更新..."

# 更新多個文件
for file in README.md "個人經歷-已填寫.md"; do
    echo "📝 更新 $file"
    python3 update_daily_info.py
done

echo "✅ 批量更新完成！"
```

#### 定時執行

```bash
# 使用 cron 定時執行
# 編輯 crontab
crontab -e

# 添加定時任務
# 每天 9:00 執行
0 9 * * * /path/to/run_update.sh
```

## 🔍 執行結果檢查

### 檢查文件變更

```bash
# 檢查 Git 狀態
git status

# 查看具體變更
git diff

# 查看提交歷史
git log --oneline -5
```

### 檢查生成的文件

```bash
# 檢查日誌目錄
ls -la daily_logs/

# 查看最新日誌
cat daily_logs/$(date +%Y-%m-%d).md

# 檢查文件內容
head -20 README.md
```

### 驗證更新內容

```bash
# 檢查時間戳更新
grep "更新紀錄" README.md
grep "更新紀錄" 個人經歷-已填寫.md

# 檢查日誌文件
find daily_logs/ -name "*.md" -exec echo "=== {} ===" \; -exec cat {} \;
```

## 🚨 故障排除

### 常見問題

#### 1. 腳本執行失敗

**問題**: `python3: command not found`

**解決方案**:
```bash
# 檢查 Python 安裝
which python3
python3 --version

# 如果未安裝，請安裝 Python
# macOS
brew install python3

# Ubuntu/Debian
sudo apt install python3 python3-pip
```

#### 2. 依賴安裝失敗

**問題**: `pip3 install requests` 失敗

**解決方案**:
```bash
# 升級 pip
python3 -m pip install --upgrade pip

# 使用國內鏡像源
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple requests
```

#### 3. 權限問題

**問題**: 腳本無法執行

**解決方案**:
```bash
# 給腳本執行權限
chmod +x run_update.sh
chmod +x update_daily_info.py
```

#### 4. Git 推送失敗

**問題**: `git push` 失敗

**解決方案**:
```bash
# 檢查 Git 配置
git config --list

# 設置用戶信息
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 檢查遠程倉庫
git remote -v
```

### 調試技巧

#### 1. 詳細日誌

```bash
# 啟用詳細輸出
python3 -v update_daily_info.py

# 或修改腳本添加調試信息
```

#### 2. 分步執行

```bash
# 分步執行，檢查每步結果
python3 -c "
from update_daily_info import DailyUpdater
updater = DailyUpdater()
print('初始化完成')
updater.update_readme()
print('README 更新完成')
"
```

#### 3. 檢查環境

```bash
# 檢查 Python 環境
python3 -c "import sys; print(sys.path)"

# 檢查已安裝的包
pip3 list

# 檢查文件權限
ls -la update_daily_info.py
```

## 📊 執行統計

### 記錄執行歷史

```bash
# 創建執行日誌
echo "$(date): 手動執行更新" >> execution.log

# 查看執行歷史
tail -20 execution.log
```

### 性能監控

```bash
# 測量執行時間
time python3 update_daily_info.py

# 監控資源使用
top -p $(pgrep -f update_daily_info.py)
```

## 🎯 最佳實踐

### 1. 執行前檢查

- 確認 Python 環境正常
- 檢查依賴包已安裝
- 驗證配置文件正確

### 2. 執行後驗證

- 檢查文件是否正確更新
- 驗證日誌文件是否生成
- 確認 Git 狀態正常

### 3. 錯誤處理

- 保存錯誤日誌
- 記錄執行時間
- 備份重要文件

## 🎯 下一步

- [基本使用](basic-usage.md) - 日常使用說明
- [配置選項](configuration.md) - 自定義配置
- [故障排除](../reference/troubleshooting.md) - 問題解決

---

**需要幫助？** 查看 [故障排除指南](../reference/troubleshooting.md)
