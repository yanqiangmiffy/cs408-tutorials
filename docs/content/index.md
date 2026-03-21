---
layout: home

hero:
  name: "408数据结构"
  text: "Python 全实现"
  tagline: 王道408全部章节 · 原理讲解 · 代码实现 · 考研要点
  image:
    src: /logo.svg
    alt: 408 数据结构
  actions:
    - theme: brand
      text: 快速开始 →
      link: /guide/getting-started
    - theme: alt
      text: 查看仓库
      link: https://github.com/yanqiangmiffy/cs408-tutorials

features:
  - icon: 🧠
    title: 原理先行
    details: 每章先讲概念、结构和复杂度，再过渡到代码实现，适合复习和打基础。
  - icon: 🐍
    title: Python 实现
    details: 全部示例使用 Python，保留清晰注释和可手写的核心版本，便于理解。
  - icon: 🎯
    title: 考研导向
    details: 把高频考点、易错点、复杂度结论集中整理，减少后期二次归纳成本。
  - icon: 📚
    title: 内容完整
    details: 覆盖 8 章主线内容，并额外整理了剑指 Offer、408 大题真题和冲刺速记专题，方便刷题和临考复盘。
---

## 学习入口

如果你是第一次使用这个站点，建议按下面顺序阅读：

1. 从 [快速开始](/guide/getting-started) 了解站点结构、运行方式和目录说明。
2. 按基础知识主线复习，从 [第1章 绪论](/data-structure-fundamentals/ch01-intro/) 一直读到 [第8章 排序](/data-structure-fundamentals/ch08-sort/)。
3. 主线过完后，先进入 [408 大题真题](/408-exam-questions/) 回看历年题型。
4. 再进入 [剑指 Offer](/coding-interview-offer/) 做专题刷题和巩固。
5. 最后使用 [冲刺与速记](/408-exam-questions/sprint/) 做考前压缩复习。

## 章节导航

| 模块 | 核心内容 | 入口 |
|------|----------|------|
| 第1章 绪论 | 数据结构三要素、时间复杂度、空间复杂度 | [开始阅读](/data-structure-fundamentals/ch01-intro/) |
| 第2章 线性表 | 顺序表、单链表、双链表、循环链表、静态链表 | [开始阅读](/data-structure-fundamentals/ch02-linear/) |
| 第3章 栈与队列 | 顺序栈、链栈、循环队列、栈的典型应用 | [开始阅读](/data-structure-fundamentals/ch03-stack-queue/) |
| 第4章 串 | 朴素模式匹配、KMP、next 与 nextval | [开始阅读](/data-structure-fundamentals/ch04-string/) |
| 第5章 树与二叉树 | 遍历、线索化、哈夫曼树、并查集 | [开始阅读](/data-structure-fundamentals/ch05-tree/) |
| 第6章 图 | 存储结构、遍历、最小生成树、最短路径、拓扑排序 | [开始阅读](/data-structure-fundamentals/ch06-graph/) |
| 第7章 查找 | 顺序查找、折半查找、BST、AVL、散列表 | [开始阅读](/data-structure-fundamentals/ch07-search/) |
| 第8章 排序 | 九类排序算法、手写过程、稳定性与复杂度对比 | [开始阅读](/data-structure-fundamentals/ch08-sort/) |
| 408 大题真题 | 2009-2024 年真题考点、题源判定与相似题映射 | [开始回顾](/408-exam-questions/) |
| 剑指 Offer | 67 道经典题按专题归类，适合复习后强化训练 | [开始刷题](/coding-interview-offer/) |
| 冲刺与速记 | 高频考点、手写模板、易错点、30 天路线与一页纸总结 | [开始冲刺](/408-exam-questions/sprint/) |

## 适合怎么用

### 考研复习

- 先看每章开头的概念与考点总结。
- 再关注代码实现中的边界条件和复杂度分析。
- 最后把表格类结论单独摘出来，形成自己的速记清单。

### 面试准备

- 主线章节优先看链表、栈队列、树、图和查找。
- 再结合 [408 大题真题](/408-exam-questions/) 和 [剑指 Offer](/coding-interview-offer/) 做专题训练。
- 临考阶段切换到 [冲刺与速记](/408-exam-questions/sprint/) 做高频回顾。
- 建议重点手写链表操作、树遍历、KMP、最短路径和几类排序算法。

### 代码练习

- 先阅读文档里的“手写过程”部分，再自己默写一版。
- 运行仓库 `code/` 目录中的示例，对照输出排查理解偏差。

## 仓库结构

```text
code/                      Python 示例代码
docs/
  package.json             文档站点依赖与脚本
  content/                 VitePress 文档源目录
    .vitepress/            站点配置
    guide/                 使用说明
    data-structure-fundamentals/
      ch01-intro/ ...      第1章到第8章基础知识
    coding-interview-offer/  剑指 Offer 专题
    408-exam-questions/      408 大题真题专题
      sprint/                冲刺与速记专题
```

## 使用建议

- GitHub Pages 部署时，站点 `base` 必须和仓库名保持一致。
- 顶部导航中的站内链接应始终使用完整绝对路径，例如 `/data-structure-fundamentals/ch03-stack-queue/` 或 `/coding-interview-offer/01`，避免在子页面里被拼成错误地址。
- 如果你准备继续补内容，优先完善每章的“易错点”“复杂度总结”和“手写过程”三部分，这三块最适合复习场景。
