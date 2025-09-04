# 🚨 故障排除指南

本指南幫助您解決每日自動更新系統的常見問題。

## 🔍 問題診斷流程

### 1. 檢查系統狀態

```bash
# 檢查 Python 版本
python3 --version

# 檢查依賴包
pip3 list | grep requests

# 檢查文件權限
ls -la update_daily_info.py

# 檢查 Git 狀態
git status
```

### 2. 查看日誌

```bash
# 查看最新日誌
ls -la daily_logs/
cat daily_logs/$(date +%Y-%m-%d).md

# 查看 GitHub Actions 日誌
# 前往 GitHub 倉庫的 Actions 頁面
```

### 3. 測試執行

```bash
# 手動執行腳本
python3 update_daily_info.py

# 使用手動執行腳本
./run_update.sh
```

## 🚨 常見問題解決

### Python 環境問題

#### 問題 1: Python 未安裝

**症狀**：
```bash
$ python3 --version
bash: python3: command not found
```

**解決方案**：

**macOS**：
```bash
# 使用 Homebrew
brew install python3

# 或從官網下載
# https://python.org/downloads/
```

**Ubuntu/Debian**：
```bash
sudo apt update
sudo apt install python3 python3-pip
```

**Windows**：
1. 前往 https://python.org/downloads/
2. 下載並安裝 Python 3.9+
3. 確保勾選 "Add Python to PATH"

#### 問題 2: Python 版本過低

**症狀**：
```bash
$ python3 --version
Python 3.6.9
```

**解決方案**：
```bash
# 升級 Python
# macOS
brew upgrade python3

# Ubuntu/Debian
sudo apt update
sudo apt install python3.9 python3.9-pip
```

#### 問題 3: 依賴包安裝失敗

**症狀**：
```bash
$ pip3 install requests
ERROR: Could not find a version that satisfies the requirement requests
```

**解決方案**：
```bash
# 升級 pip
python3 -m pip install --upgrade pip

# 使用國內鏡像源
pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple requests

# 或使用阿里雲鏡像
pip3 install -i https://mirrors.aliyun.com/pypi/simple/ requests
```

### 腳本執行問題

#### 問題 1: 權限錯誤

**症狀**：
```bash
$ ./run_update.sh
bash: ./run_update.sh: Permission denied
```

**解決方案**：
```bash
# 給腳本執行權限
chmod +x run_update.sh
chmod +x update_daily_info.py
```

#### 問題 2: 文件未找到

**症狀**：
```bash
$ python3 update_daily_info.py
❌ 找不到 README.md 文件
```

**解決方案**：
```bash
# 檢查文件是否存在
ls -la README.md

# 檢查當前目錄
pwd

# 確認在正確的目錄中執行
cd /path/to/your/repository
```

#### 問題 3: 編碼錯誤

**症狀**：
```bash
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xXX
```

**解決方案**：
```bash
# 檢查文件編碼
file README.md

# 轉換文件編碼
iconv -f gbk -t utf-8 README.md > README_utf8.md
mv README_utf8.md README.md
```

### Git 操作問題

#### 問題 1: Git 未配置

**症狀**：
```bash
$ git commit
*** Please tell me who you are.
```

**解決方案**：
```bash
# 設置 Git 用戶信息
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# 檢查配置
git config --list
```

#### 問題 2: 推送失敗

**症狀**：
```bash
$ git push origin main
remote: Permission to user/repo.git denied to user.
```

**解決方案**：
```bash
# 檢查遠程倉庫
git remote -v

# 更新遠程倉庫 URL
git remote set-url origin https://github.com/username/repository.git

# 或使用 SSH
git remote set-url origin git@github.com:username/repository.git
```

#### 問題 3: 合併衝突

**症狀**：
```bash
$ git push origin main
error: failed to push some refs to 'origin'
hint: Updates were rejected because the remote contains work that you do
```

**解決方案**：
```bash
# 拉取最新變更
git pull origin main

# 解決衝突後提交
git add .
git commit -m "解決合併衝突"

# 推送變更
git push origin main
```

### GitHub Actions 問題

#### 問題 1: Actions 未啟用

**症狀**：
在 GitHub 倉庫中看不到 Actions 標籤

**解決方案**：
1. 前往 GitHub 倉庫設置
2. 在左側菜單中點擊 "Actions"
3. 選擇 "Allow all actions and reusable workflows"
4. 保存設置

#### 問題 2: 工作流程執行失敗

**症狀**：
GitHub Actions 執行狀態為紅色（失敗）

**解決方案**：
1. 點擊失敗的執行記錄
2. 查看詳細日誌
3. 根據錯誤信息進行修復

**常見錯誤**：

**Python 版本錯誤**：
```yaml
# 修改 .github/workflows/daily-update.yml
- name: 設置 Python 環境
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'  # 使用支持的版本
```

**依賴安裝失敗**：
```yaml
# 修改安裝步驟
- name: 安裝依賴
  run: |
    python -m pip install --upgrade pip
    pip install requests --no-cache-dir
```

#### 問題 3: 權限不足

**症狀**：
```
Error: fatal: could not read Username for 'https://github.com'
```

**解決方案**：
1. 檢查倉庫權限設置
2. 確認 `GITHUB_TOKEN` 具有寫入權限
3. 檢查分支保護規則

### 配置文件問題

#### 問題 1: JSON 語法錯誤

**症狀**：
```bash
$ python3 -m json.tool config.json
Expecting ',' delimiter: line 5 column 3 (char 89)
```

**解決方案**：
```bash
# 檢查 JSON 語法
python3 -m json.tool config.json

# 修復語法錯誤
# 確保所有字符串用雙引號
# 確保所有對象和數組正確關閉
```

#### 問題 2: 配置項缺失

**症狀**：
```bash
KeyError: 'timezone'
```

**解決方案**：
```bash
# 檢查配置文件
cat config.json

# 確保所有必要的配置項都存在
# 參考配置文檔添加缺失的配置項
```

#### 問題 3: 時區設置錯誤

**症狀**：
```bash
pytz.exceptions.UnknownTimeZoneError: 'Asia/Taipei'
```

**解決方案**：
```json
{
  "update_config": {
    "timezone": "Asia/Taipei"  // 確保時區名稱正確
  }
}
```

## 🔧 調試技巧

### 1. 啟用詳細日誌

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# 在腳本中添加調試信息
print(f"DEBUG: 當前時間: {self.current_time}")
print(f"DEBUG: 文件路徑: {readme_path}")
```

### 2. 分步執行

```bash
# 分步執行，檢查每步結果
python3 -c "
from update_daily_info import DailyUpdater
updater = DailyUpdater()
print('初始化完成')
"

python3 -c "
from update_daily_info import DailyUpdater
updater = DailyUpdater()
updater.update_readme()
print('README 更新完成')
"
```

### 3. 檢查環境變量

```bash
# 檢查 Python 環境
python3 -c "import sys; print(sys.path)"

# 檢查已安裝的包
pip3 list

# 檢查文件權限
ls -la update_daily_info.py
```

### 4. 使用調試模式

```bash
# 啟用 Python 調試模式
python3 -v update_daily_info.py

# 或使用 pdb 調試器
python3 -m pdb update_daily_info.py
```

## 📊 性能問題

### 執行時間過長

**可能原因**：
- 網絡連接慢
- 文件過大
- 系統資源不足

**解決方案**：
```bash
# 測量執行時間
time python3 update_daily_info.py

# 監控資源使用
top -p $(pgrep -f update_daily_info.py)
```

### 內存使用過高

**解決方案**：
```python
# 優化文件讀寫
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()
# 處理完成後立即關閉文件
```

## 🆘 緊急恢復

### 恢復配置文件

```bash
# 從備份恢復
cp config.json.backup config.json

# 或重新創建默認配置
cat > config.json << EOF
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
EOF
```

### 重置 Git 狀態

```bash
# 重置到最後一次提交
git reset --hard HEAD

# 清理未跟蹤的文件
git clean -fd

# 重新添加文件
git add .
git commit -m "重置到穩定狀態"
```

### 重新部署

```bash
# 重新推送代碼
git add .
git commit -m "修復問題並重新部署"
git push origin main

# 手動觸發 GitHub Actions
# 前往 GitHub 倉庫的 Actions 頁面
```

## 📞 獲取幫助

### 1. 查看文檔

- [安裝指南](../setup/installation.md)
- [部署指南](../setup/deployment.md)
- [基本使用](../usage/basic-usage.md)

### 2. 檢查日誌

- 本地日誌：`daily_logs/` 目錄
- GitHub Actions 日誌：Actions 頁面

### 3. 創建 Issue

如果問題仍然存在：
1. 前往 GitHub 倉庫
2. 創建新的 Issue
3. 提供詳細的錯誤信息和日誌

### 4. 聯繫支援

- 郵箱：lungyuchengroy@gmail.com
- GitHub：https://github.com/eqwgeryfgbdf

## 🎯 預防措施

### 1. 定期備份

```bash
# 備份重要文件
cp config.json config.json.backup
cp -r daily_logs daily_logs.backup
```

### 2. 監控執行

- 每週檢查一次 Actions 執行狀態
- 查看每日日誌確保正常運行

### 3. 測試變更

- 修改配置前先備份
- 在測試環境中驗證變更
- 小步迭代，避免大幅修改

---

**需要更多幫助？** 查看其他文檔或創建 GitHub Issue
