# 快速开始

欢迎使用 408 数据结构 Python 实现文档站。

这个站点面向两类场景：

- 408 考研复习：快速回顾概念、复杂度、考点和易错点。
- 面试或练习：直接定位到某个数据结构或算法的 Python 实现。

## 站点内容

主线内容按照王道 408 数据结构章节组织，共 8 章：

| 章节 | 内容 | 重点 |
|------|------|------|
| 第1章 | 绪论 | 数据结构三要素、时间复杂度、空间复杂度 |
| 第2章 | 线性表 | 顺序表、单链表、双链表、循环链表 |
| 第3章 | 栈与队列 | 栈、队列、括号匹配、表达式求值 |
| 第4章 | 串 | 朴素匹配、KMP、next/nextval |
| 第5章 | 树与二叉树 | 遍历、线索树、哈夫曼树、并查集 |
| 第6章 | 图 | BFS、DFS、最小生成树、最短路径、拓扑排序 |
| 第7章 | 查找 | 顺序查找、折半查找、BST、AVL、散列表 |
| 第8章 | 排序 | 常见排序算法实现与复杂度对比 |

除了基础知识目录外，还补充了 [剑指 Offer](/coding-interview-offer/) 专题和 [408 大题真题](/408-exam-questions/) 专题；其中 [冲刺与速记](/408-exam-questions/sprint/) 被收纳在 408 真题目录下，方便按考试场景集中查看。

## 本地运行

文档站点的工作目录在 `docs/`。

```bash
cd docs
npm ci
npm run docs:dev
```

启动后，终端会输出一个本地地址，通常是 `http://localhost:5173/`。

如果你只想验证构建是否正常，可以执行：

```bash
cd docs
npm run docs:build
```

## 仓库目录说明

```text
G:\Projects\cs408-tutorials
├── code/                  Python 示例代码
├── docs/
│   ├── package.json       文档脚本与依赖
│   ├── package-lock.json
│   ├── README.md
│   └── content/           VitePress 文档源目录
│       ├── .vitepress/    站点配置与构建产物
│       ├── guide/         使用说明
│       ├── data-structure-fundamentals/
│       │   ├── ch01-intro/    第1章 绪论
│       │   ├── ch02-linear/   第2章 线性表
│       │   ├── ...
│       │   └── ch08-sort/     第8章 排序
│       ├── coding-interview-offer/   剑指 Offer 专题
│       └── 408-exam-questions/       408 大题真题专题
│           └── sprint/               冲刺与速记专题
└── .github/workflows/     GitHub Pages 部署工作流
```

## 推荐阅读方式

### 如果你在准备 408

1. 先读 [第1章 绪论](/data-structure-fundamentals/ch01-intro/)，把复杂度分析框架建立起来。
2. 然后顺序阅读线性表、栈队列、串、树、图、查找、排序。
3. 每章优先看概念、手写过程、复杂度总结，再看完整代码。

### 如果你在准备面试

1. 先复习链表、树、图、查找和排序。
2. 再进入 [408 大题真题](/408-exam-questions/) 复盘历年大题模型。
3. 最后进入 [剑指 Offer](/coding-interview-offer/) 做分类刷题。
4. 临考前切到 [冲刺与速记](/408-exam-questions/sprint/) 做高频压缩复习。
5. 对容易手写的题，建议自己脱离文档重新实现一遍。

## 部署到 GitHub Pages

本仓库已经包含 GitHub Actions 工作流，默认会在 `main` 分支的 `docs/**` 发生变化时自动构建。

部署步骤：

1. 将仓库推送到 GitHub。
2. 打开仓库 `Settings -> Pages`。
3. 在 `Source` 中选择 `GitHub Actions`。
4. 后续只要 push 到 `main`，页面就会自动更新。

默认访问地址：

[https://yanqiangmiffy.github.io/cs408-tutorials/](https://yanqiangmiffy.github.io/cs408-tutorials/)

## 常见问题

### 1. 为什么首页能点，进了章节页再点顶部菜单就 404？

原因通常是站内链接写成了相对路径，例如：

```ts
{ text: '第3章 栈与队列', link: 'ch03-stack-queue/' }
```

当你当前在 `/data-structure-fundamentals/ch02-linear/` 页面时，浏览器会把它拼成：

```text
/cs408-tutorials/data-structure-fundamentals/ch02-linear/ch03-stack-queue/
```

这个地址当然不存在，所以会跳到 404。

正确写法应该是绝对路径：

```ts
{ text: '第3章 栈与队列', link: '/data-structure-fundamentals/ch03-stack-queue/' }
```

### 2. GitHub Pages 部署后静态资源丢失怎么办？

优先检查 `docs/content/.vitepress/config.mts` 中的 `base`：

```ts
base: '/cs408-tutorials/'
```

这个值必须与 GitHub 仓库名一致。

### 3. 修改文档后没有生效怎么办？

- 本地开发环境下，先确认是否运行在 `docs` 目录。
- 部署环境下，检查 GitHub Actions 是否成功执行。
- 如果修改的是配置文件，最好重新执行一次 `npm run docs:build` 验证。

## Python 示例代码

文档之外，仓库根目录的 `code/` 下还提供了可运行的 Python 示例。比如：

```bash
python code/7_search/7_4_btree.py
python code/8_sorting/quick_sort.py
```

这种方式适合在阅读完文档后，对照运行结果进一步理解算法行为。
