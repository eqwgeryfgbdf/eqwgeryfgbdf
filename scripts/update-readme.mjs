import fs from 'fs/promises';
import path from 'path';

const repositoryRoot = path.resolve(process.cwd());
const readmePath = path.join(repositoryRoot, 'README.md');

const markers = {
  QUOTE: { start: '<!-- QUOTE:START -->', end: '<!-- QUOTE:END -->' },
  CLOCK: { start: '<!-- CLOCK:START -->', end: '<!-- CLOCK:END -->' },
  PROMPT: { start: '<!-- PROMPT:START -->', end: '<!-- PROMPT:END -->' },
};

function replaceBetween(content, { start, end }, replacement) {
  const startIndex = content.indexOf(start);
  const endIndex = content.indexOf(end);
  if (startIndex === -1 || endIndex === -1 || endIndex < startIndex) {
    return content;
  }
  const before = content.slice(0, startIndex + start.length);
  const after = content.slice(endIndex);
  const inner = `\n${replacement}\n`;
  return `${before}${inner}${after}`;
}

async function fetchQuote() {
  const fallbacks = [
    '「程式是給人讀的，順便讓機器執行。」— Martin Fowler',
    '「完美是無法再刪去任何東西時。」— Antoine de Saint-Exupéry',
    '「最好的程式碼是你不需要寫的程式碼。」',
    '「慢就是快，先把方向走對。」',
    '「成長來自把不確定拆成小步驟。」',
  ];
  try {
    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), 8000);
    const resp = await fetch('https://api.quotable.io/random?tags=technology|wisdom|inspirational', { signal: controller.signal });
    clearTimeout(timer);
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const data = await resp.json();
    const text = (data?.content || '').trim();
    const author = (data?.author || 'Anonymous').trim();
    if (!text) throw new Error('Empty quote');
    return `💡 ${text} — ${author}`;
  } catch (_) {
    const pick = fallbacks[Math.floor(Math.random() * fallbacks.length)];
    return `💡 ${pick}`;
  }
}

function formatTaipeiTime(date = new Date()) {
  const fmt = new Intl.DateTimeFormat('zh-TW', {
    timeZone: 'Asia/Taipei',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    weekday: 'short',
    hour12: false,
  });
  return fmt.format(date);
}

function generatePrompt() {
  const prompts = [
    '用純 CSS 畫一個你最愛的食物。',
    '用 50 行內寫一個迷你待辦清單（可排序）。',
    '把一段 API 回應以時間軸視覺化呈現。',
    '做一個只能用鍵盤操作的迷你遊戲（無滑鼠）。',
    '用畫面解釋一個複雜概念（例如 Event Loop）。',
    '把你今天學到的一件事做成圖卡。',
    '寫個 CLI：輸入關鍵字自動幫你搜集三個資料來源。',
    '把 Markdown 轉成投影片的最小可行工具。',
  ];
  const pick = prompts[Math.floor(Math.random() * prompts.length)];
  const issueTitle = encodeURIComponent(`我要挑戰：${pick}`);
  const issueBody = encodeURIComponent('勾選完成、貼上截圖或連結吧！');
  const repo = process.env.GITHUB_REPOSITORY || '';
  const issueLink = repo
    ? `https://github.com/${repo}/issues/new?title=${issueTitle}&body=${issueBody}`
    : '#';
  return `🎯 ${pick} ｜ [建立 Issue 開始](<${issueLink}>)`;
}

async function main() {
  const readme = await fs.readFile(readmePath, 'utf8');

  const [quote, timeStr, prompt] = await Promise.all([
    fetchQuote(),
    Promise.resolve(formatTaipeiTime()),
    Promise.resolve(generatePrompt()),
  ]);

  const clockLine = `🕒 台北時間：${timeStr}`;

  let next = readme;
  next = replaceBetween(next, markers.QUOTE, quote);
  next = replaceBetween(next, markers.CLOCK, clockLine);
  next = replaceBetween(next, markers.PROMPT, prompt);

  if (next !== readme) {
    await fs.writeFile(readmePath, next, 'utf8');
    console.log('README updated.');
  } else {
    console.log('No changes detected.');
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(0);
});


