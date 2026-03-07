---
name: cs408-docs-site
description: >
  Build a complete GitHub Pages documentation site for CS408 Data Structures
  (计算机科学408-数据结构) projects with Python code examples. Use this skill
  whenever the user wants to create a VitePress/Docusaurus/MkDocs static site
  for algorithm documentation, wants to publish CS408 study notes online,
  needs GitHub Actions CI/CD for auto-deployment, or wants to generate
  beautiful algorithm docs with code highlighting, diagrams, and exam tips.
  Trigger even if the user just says "docs网站", "github博客", "算法文档", or
  "online documentation" for a data structures project.
---

# CS408 GitHub Docs Site Skill

Generate a **complete, deployable** GitHub Pages documentation site for a
CS408 / Data Structures Python project. The output is a self-contained
VitePress site with full algorithm documentation, ready to push and deploy.

---

## Overview of What to Produce

```
docs-site/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions auto-deploy
├── docs/
│   ├── .vitepress/
│   │   ├── config.mts          # Site config, nav, sidebar, theme
│   │   └── theme/
│   │       └── index.ts        # Custom theme (optional)
│   ├── public/
│   │   └── logo.svg            # Site logo
│   ├── index.md                # Home page
│   ├── guide/
│   │   └── getting-started.md  # Quick start
│   ├── ch01-intro/             # Chapter 1: 绪论
│   │   └── index.md
│   ├── ch02-linear/            # Chapter 2: 线性表
│   │   └── index.md
│   ├── ch03-stack-queue/       # Chapter 3: 栈与队列
│   │   └── index.md
│   ├── ch04-string/            # Chapter 4: 串
│   │   └── index.md
│   ├── ch05-tree/              # Chapter 5: 树与二叉树
│   │   └── index.md
│   ├── ch06-graph/             # Chapter 6: 图
│   │   └── index.md
│   ├── ch07-search/            # Chapter 7: 查找
│   │   └── index.md
│   └── ch08-sort/              # Chapter 8: 排序
│       └── index.md
├── package.json
└── README.md
```

---

## Step-by-Step Instructions

### Step 1 — Scaffold the Project

```bash
mkdir -p docs-site/docs/.vitepress/theme
mkdir -p docs-site/docs/public
mkdir -p docs-site/docs/{guide,ch01-intro,ch02-linear,ch03-stack-queue,ch04-string,ch05-tree,ch06-graph,ch07-search,ch08-sort}
mkdir -p docs-site/.github/workflows
cd docs-site
```

### Step 2 — Write `package.json`

```json
{
  "name": "cs408-docs",
  "version": "1.0.0",
  "description": "408考研数据结构 Python 实现文档",
  "scripts": {
    "docs:dev": "vitepress dev docs",
    "docs:build": "vitepress build docs",
    "docs:preview": "vitepress preview docs"
  },
  "devDependencies": {
    "vitepress": "^1.3.4"
  }
}
```

### Step 3 — Write VitePress Config (`docs/.vitepress/config.mts`)

Use this exact structure. Fill in `base` with the GitHub repo name (e.g. `/cs408-python/`):

```typescript
import { defineConfig } from 'vitepress'

export default defineConfig({
  base: '/YOUR_REPO_NAME/',
  lang: 'zh-CN',
  title: '408数据结构 · Python实现',
  description: '王道408数据结构全部章节Python代码实现，含原理讲解、复杂度分析与考研要点',

  head: [
    ['link', { rel: 'icon', href: '/favicon.ico' }],
    ['meta', { name: 'theme-color', content: '#3c8772' }],
  ],

  themeConfig: {
    logo: '/logo.svg',
    siteTitle: '408数据结构',

    nav: [
      { text: '首页', link: '/' },
      { text: '快速开始', link: '/guide/getting-started' },
      {
        text: '章节',
        items: [
          { text: '第1章 绪论', link: '/ch01-intro/' },
          { text: '第2章 线性表', link: '/ch02-linear/' },
          { text: '第3章 栈与队列', link: '/ch03-stack-queue/' },
          { text: '第4章 串', link: '/ch04-string/' },
          { text: '第5章 树与二叉树', link: '/ch05-tree/' },
          { text: '第6章 图', link: '/ch06-graph/' },
          { text: '第7章 查找', link: '/ch07-search/' },
          { text: '第8章 排序', link: '/ch08-sort/' },
        ]
      },
    ],

    sidebar: {
      '/ch01-intro/': [{ text: '第1章 绪论', items: [
        { text: '基本概念与三要素', link: '/ch01-intro/#concepts' },
        { text: '时间复杂度', link: '/ch01-intro/#time-complexity' },
        { text: '空间复杂度', link: '/ch01-intro/#space-complexity' },
      ]}],
      '/ch02-linear/': [{ text: '第2章 线性表', items: [
        { text: '顺序表', link: '/ch02-linear/#sequential' },
        { text: '单链表', link: '/ch02-linear/#singly-linked' },
        { text: '双链表', link: '/ch02-linear/#doubly-linked' },
        { text: '循环链表', link: '/ch02-linear/#circular' },
        { text: '静态链表', link: '/ch02-linear/#static' },
      ]}],
      '/ch03-stack-queue/': [{ text: '第3章 栈与队列', items: [
        { text: '栈', link: '/ch03-stack-queue/#stack' },
        { text: '队列', link: '/ch03-stack-queue/#queue' },
        { text: '栈的应用', link: '/ch03-stack-queue/#applications' },
        { text: '矩阵压缩', link: '/ch03-stack-queue/#matrix' },
      ]}],
      '/ch04-string/': [{ text: '第4章 串', items: [
        { text: '朴素匹配', link: '/ch04-string/#naive' },
        { text: 'KMP算法', link: '/ch04-string/#kmp' },
      ]}],
      '/ch05-tree/': [{ text: '第5章 树与二叉树', items: [
        { text: '二叉树遍历', link: '/ch05-tree/#traversal' },
        { text: '线索二叉树', link: '/ch05-tree/#threaded' },
        { text: '哈夫曼树', link: '/ch05-tree/#huffman' },
        { text: '并查集', link: '/ch05-tree/#union-find' },
      ]}],
      '/ch06-graph/': [{ text: '第6章 图', items: [
        { text: '图的存储', link: '/ch06-graph/#storage' },
        { text: 'BFS / DFS', link: '/ch06-graph/#traversal' },
        { text: '最小生成树', link: '/ch06-graph/#mst' },
        { text: '最短路径', link: '/ch06-graph/#shortest-path' },
        { text: '拓扑排序 & 关键路径', link: '/ch06-graph/#topo' },
      ]}],
      '/ch07-search/': [{ text: '第7章 查找', items: [
        { text: '顺序/折半/分块查找', link: '/ch07-search/#basic' },
        { text: 'BST & AVL树', link: '/ch07-search/#bst-avl' },
        { text: '散列表', link: '/ch07-search/#hash' },
      ]}],
      '/ch08-sort/': [{ text: '第8章 排序', items: [
        { text: '插入排序类', link: '/ch08-sort/#insertion' },
        { text: '交换排序类', link: '/ch08-sort/#exchange' },
        { text: '选择排序类', link: '/ch08-sort/#selection' },
        { text: '归并 & 基数排序', link: '/ch08-sort/#merge-radix' },
        { text: '排序算法比较', link: '/ch08-sort/#comparison' },
      ]}],
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/YOUR_USERNAME/YOUR_REPO' }
    ],

    footer: {
      message: '基于 MIT 许可发布',
      copyright: 'Copyright © 2024 · 408数据结构Python实现'
    },

    search: {
      provider: 'local'
    },

    editLink: {
      pattern: 'https://github.com/YOUR_USERNAME/YOUR_REPO/edit/main/docs/:path',
      text: '在 GitHub 上编辑此页'
    },

    lastUpdated: {
      text: '最后更新于',
      formatOptions: { dateStyle: 'short' }
    },
  },

  markdown: {
    theme: {
      light: 'github-light',
      dark: 'one-dark-pro'
    },
    lineNumbers: true,
  }
})
```

### Step 4 — Write the Home Page (`docs/index.md`)

```markdown
---
layout: home

hero:
  name: "408数据结构"
  text: "Python 全实现"
  tagline: 王道408全部章节 · 原理讲解 · 代码实现 · 考研要点
  image:
    src: /logo.svg
    alt: Logo
  actions:
    - theme: brand
      text: 快速开始 →
      link: /guide/getting-started
    - theme: alt
      text: GitHub
      link: https://github.com/YOUR_USERNAME/YOUR_REPO

features:
  - icon: 📝
    title: 原理详解
    details: 每个算法配有详细的原理讲解、图解演示和复杂度分析。
  - icon: 🐍
    title: Python 实现
    details: 所有数据结构与算法均用 Python 实现，代码简洁易读。
  - icon: ✅
    title: 考研要点
    details: 针对408考研，标注高频考点、易错点和真题思路。
  - icon: ⚡
    title: 8大章节
    details: 覆盖绪论、线性表、栈队列、串、树、图、查找、排序全部内容。
---
```

### Step 5 — Write Chapter Documentation Pages

For **each chapter page**, follow this template structure. Write full content — do NOT leave placeholders:

````markdown
# 第N章 章节名称

> **考研要点速记**：... (2-3句核心结论)

## 1. 概念介绍

[2-3段原理说明，使用类比帮助理解]

## 2. 核心操作

### 操作名称

**原理**：...

**时间复杂度**：O(?) | **空间复杂度**：O(?)

```python
# 完整可运行的 Python 代码
# 包含详细行注释
```

**运行示例**：
```
输入: ...
输出: ...
```

## 3. 考研重点 & 易错点

- ⚠️ 易错点1
- 📌 高频考点

## 4. 复杂度总结表

| 操作 | 时间复杂度 | 空间复杂度 |
|------|-----------|-----------|
| ...  | O(?)      | O(?)      |
````

**Apply this template to all 8 chapters.** Each chapter page should be
300-600 lines of rich content. See the "Content Requirements per Chapter"
section below for what to include in each.

### Step 6 — GitHub Actions (`/.github/workflows/deploy.yml`)

```yaml
name: Deploy VitePress to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Install dependencies
        run: npm ci

      - name: Build with VitePress
        run: npm run docs:build

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: docs/.vitepress/dist

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    needs: build
    runs-on: ubuntu-latest
    name: Deploy
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

---

## Content Requirements per Chapter

Write each chapter's `index.md` with these specific contents:

### Ch01 — 绪论
- 数据、数据元素、数据结构三要素（逻辑结构、存储结构、运算）
- 时间复杂度：大O记号定义、常见增长量级排序表、递推分析法
- 空间复杂度：原地算法定义
- Python 示例：分析循环嵌套的T(n)，手写O推导

### Ch02 — 线性表
- 顺序表：随机存取、插入O(n)、删除O(n)，完整Python类实现
- 单链表：头插法/尾插法建表、按值查找、插入、删除，完整Python类
- 双链表：前驱指针操作，插入和删除的指针修改顺序（重点！）
- 循环链表：判空条件（`head.next == head`）
- 静态链表：游标数组模拟指针，适合无指针语言
- 顺序表 vs 链表对比表格

### Ch03 — 栈与队列
- 顺序栈：`top`指针初始化为-1，判空判满
- 链栈：带头节点 vs 不带头节点
- 共享栈：两栈共享一个数组，`top1+1==top2`时满
- 循环队列：`(rear+1)%MaxSize==front`判满，`front==rear`判空，有效长度公式
- 链队列：入队出队操作
- 双端队列：输入受限/输出受限
- 括号匹配：用栈，完整代码
- 中缀→后缀表达式：运算符优先级栈，完整代码
- 特殊矩阵压缩：对称矩阵、三角矩阵、三对角矩阵的下标公式推导

### Ch04 — 串
- 朴素模式匹配：O(mn) 完整代码
- KMP算法：next数组构造（详细推导！）、匹配过程，O(m+n)
- nextval数组优化
- 手工计算next数组的方法（考研必考）

### Ch05 — 树与二叉树
- 二叉树性质（5个定理）
- 先序/中序/后序递归+非递归遍历，层序遍历（BFS）
- 由遍历序列还原二叉树
- 线索化：中序线索化完整代码，找前驱后继
- 哈夫曼树：构造过程、WPL计算、哈夫曼编码完整代码
- 并查集：路径压缩+按秩合并，完整代码，应用场景

### Ch06 — 图
- 邻接矩阵：适合稠密图，完整Python类
- 邻接表：适合稀疏图，完整Python类
- BFS：层序遍历思想，`visited[]`数组，完整代码
- DFS：递归+非递归，完整代码
- Prim算法：适合稠密图，O(V²)，完整代码
- Kruskal算法：适合稀疏图，O(ElogE)，配合并查集，完整代码
- Dijkstra：单源最短路，不适用负权边，O(V²)，完整代码
- Floyd：全源最短路，O(V³)，完整代码
- 拓扑排序：Kahn算法（BFS），检测环，完整代码
- 关键路径：AOE网，最早/最晚时间，关键活动，完整代码

### Ch07 — 查找
- 顺序查找：ASL计算（成功/失败）
- 折半查找：仅适用于有序顺序表，判定树，ASL=O(log n)，完整代码
- 分块查找：折半查找索引+顺序查找块
- BST：插入、删除（三种情况！）、查找，完整Python类
- AVL树：平衡因子、四种旋转（LL/RR/LR/RL），完整Python类（含旋转代码）
- 散列表：除留余数法、线性探测、二次探测、拉链法，ASL计算
- 装填因子对散列表性能的影响

### Ch08 — 排序

包含 **所有9种排序算法** 的完整Python实现，并附：

对每种排序：
- 原理说明（1段）
- 完整Python代码（含注释）
- 一个手工推导示例（数组变化过程）
- 稳定性结论

最后附 **排序算法综合比较表**：

| 算法 | 最好 | 平均 | 最坏 | 空间 | 稳定性 | 适用场景 |
|------|------|------|------|------|--------|---------|
| 直接插入 | O(n) | O(n²) | O(n²) | O(1) | ✅稳定 | 基本有序 |
| 冒泡 | O(n) | O(n²) | O(n²) | O(1) | ✅稳定 | 小规模 |
| 简单选择 | O(n²) | O(n²) | O(n²) | O(1) | ❌不稳定 | - |
| 希尔 | O(n) | O(n^1.3) | O(n²) | O(1) | ❌不稳定 | 中等规模 |
| 快速排序 | O(nlogn) | O(nlogn) | O(n²) | O(logn) | ❌不稳定 | 大规模 |
| 堆排序 | O(nlogn) | O(nlogn) | O(nlogn) | O(1) | ❌不稳定 | 大规模 |
| 归并排序 | O(nlogn) | O(nlogn) | O(nlogn) | O(n) | ✅稳定 | 要求稳定 |
| 计数排序 | O(n+k) | O(n+k) | O(n+k) | O(k) | ✅稳定 | 整数范围小 |
| 基数排序 | O(d(n+r)) | O(d(n+r)) | O(d(n+r)) | O(r) | ✅稳定 | 多关键字 |

---

## Logo SVG

Write a simple but attractive SVG logo to `docs/public/logo.svg`:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <rect width="100" height="100" rx="20" fill="#3c8772"/>
  <text x="50" y="55" font-family="monospace" font-size="36"
        font-weight="bold" fill="white" text-anchor="middle"
        dominant-baseline="middle">DS</text>
  <text x="50" y="80" font-family="sans-serif" font-size="12"
        fill="#a8d5c2" text-anchor="middle">408</text>
</svg>
```

---

## Deployment Instructions to Include in README

```markdown
## 🚀 本地预览

```bash
npm install
npm run docs:dev
# 打开 http://localhost:5173
```

## 📦 部署到 GitHub Pages

1. 将本仓库 push 到 GitHub
2. 进入 Settings → Pages → Source → 选择 **GitHub Actions**
3. Push 到 main 分支，GitHub Actions 自动构建并部署
4. 访问 `https://YOUR_USERNAME.github.io/YOUR_REPO/`

### 重要：修改配置中的占位符

- `docs/.vitepress/config.mts` 中的 `base` 改为你的仓库名
- `socialLinks` 中的 GitHub 链接改为你的链接
- `editLink` 中的路径改为你的仓库路径
```

---

## Quality Checklist

Before finishing, verify:

- [ ] `config.mts` has correct `base` path (matches GitHub repo name)
- [ ] All 8 chapter `index.md` files exist with substantial content (300+ lines each)
- [ ] Every code block in docs has syntax highlighting (` ```python `)
- [ ] `deploy.yml` workflow is correct and has right artifact path
- [ ] `package.json` has correct VitePress version
- [ ] Home page hero section has working links
- [ ] Sidebar items link to real heading anchors
- [ ] Logo SVG exists at `docs/public/logo.svg`
- [ ] Local build succeeds: `npm run docs:build`

---

## Common Mistakes to Avoid

- **Wrong `base` path**: Must be `/repo-name/` (with slashes) or `/` for user pages
- **Broken anchor links**: VitePress generates anchors from Chinese headings — test them
- **Missing `npm ci`**: Use `npm ci` not `npm install` in CI for reproducibility
- **Code block language**: Always specify ` ```python ` not just ` ``` `
- **Line numbers**: Enabled globally in config, no per-block action needed
