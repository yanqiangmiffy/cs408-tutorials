# CS408 数据结构文档站点

408考研数据结构全部章节Python代码实现文档，基于VitePress构建。

## 🚀 本地预览

```bash
npm ci
npm run docs:dev
# 打开终端输出中的本地地址，通常是 http://localhost:5173/
```

## 📦 部署到 GitHub Pages

1. 将本仓库 push 到 GitHub
2. 进入仓库 Settings → Pages → Source → 选择 **GitHub Actions**
3. Push 到 main 分支，GitHub Actions 自动构建并部署
4. 访问 `https://yanqiangmiffy.github.io/cs408-tutorials/`

## 📝 内容结构

```
docs/
├── index.md                # 首页
├── guide/
│   └── getting-started.md  # 快速开始
├── ch01-intro/             # 第1章 绪论
├── ch02-linear/            # 第2章 线性表
├── ch03-stack-queue/       # 第3章 栈与队列
├── ch04-string/            # 第4章 串
├── ch05-tree/              # 第5章 树与二叉树
├── ch06-graph/             # 第6章 图
├── ch07-search/            # 第7章 查找
└── ch08-sort/              # 第8章 排序
```

## 🛠️ 技术栈

- **框架**: VitePress 1.x
- **语言**: Markdown + TypeScript
- **部署**: GitHub Actions + GitHub Pages

## 📄 许可

MIT License
