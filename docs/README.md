# CS408 数据结构文档站

这是仓库中的 VitePress 文档站点工程，文档源文件位于 `docs/content/`，不是 `docs/` 根目录。

## 本地预览

```bash
cd docs
npm ci
npm run docs:dev
```

如果只需要检查构建是否正常：

```bash
cd docs
npm run docs:build
```

## 文档目录

```text
docs/
├── package.json
├── package-lock.json
├── README.md
└── content/
    ├── .vitepress/
    │   └── config.mts
    ├── index.md
    ├── guide/
    │   └── getting-started.md
    ├── ch01-intro/
    ├── ch02-linear/
    ├── ch03-stack-queue/
    ├── ch04-string/
    ├── ch05-tree/
    ├── ch06-graph/
    ├── ch07-search/
    ├── ch08-sort/
    ├── ch09-offer/
    └── public/
```

## 部署到 GitHub Pages

仓库已配置 `.github/workflows/deploy.yml`，会在 `docs/**` 发生变化后自动构建并发布。

部署前重点确认：

- `docs/content/.vitepress/config.mts` 中的 `base` 必须是 `/cs408-tutorials/`
- 站内导航链接使用绝对路径，例如 `/ch03-stack-queue/`
- 所有静态资源放在 `docs/content/public/`

部署地址：

[https://yanqiangmiffy.github.io/cs408-tutorials/](https://yanqiangmiffy.github.io/cs408-tutorials/)
