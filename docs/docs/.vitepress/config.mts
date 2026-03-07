import { defineConfig } from 'vitepress'

export default defineConfig({
  base: '/cs408-tutorials/',
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
      '/ch01-intro/': [{
        text: '第1章 绪论', items: [
          { text: '基本概念与三要素', link: '/ch01-intro/#concepts' },
          { text: '时间复杂度', link: '/ch01-intro/#time-complexity' },
          { text: '空间复杂度', link: '/ch01-intro/#space-complexity' },
        ]
      }],
      '/ch02-linear/': [{
        text: '第2章 线性表', items: [
          { text: '顺序表', link: '/ch02-linear/#sequential' },
          { text: '单链表', link: '/ch02-linear/#singly-linked' },
          { text: '双链表', link: '/ch02-linear/#doubly-linked' },
          { text: '循环链表', link: '/ch02-linear/#circular' },
          { text: '静态链表', link: '/ch02-linear/#static' },
        ]
      }],
      '/ch03-stack-queue/': [{
        text: '第3章 栈与队列', items: [
          { text: '栈', link: '/ch03-stack-queue/#stack' },
          { text: '队列', link: '/ch03-stack-queue/#queue' },
          { text: '栈的应用', link: '/ch03-stack-queue/#applications' },
          { text: '矩阵压缩', link: '/ch03-stack-queue/#matrix' },
        ]
      }],
      '/ch04-string/': [{
        text: '第4章 串', items: [
          { text: '朴素匹配', link: '/ch04-string/#naive' },
          { text: 'KMP算法', link: '/ch04-string/#kmp' },
        ]
      }],
      '/ch05-tree/': [{
        text: '第5章 树与二叉树', items: [
          { text: '二叉树遍历', link: '/ch05-tree/#traversal' },
          { text: '线索二叉树', link: '/ch05-tree/#threaded' },
          { text: '哈夫曼树', link: '/ch05-tree/#huffman' },
          { text: '并查集', link: '/ch05-tree/#union-find' },
        ]
      }],
      '/ch06-graph/': [{
        text: '第6章 图', items: [
          { text: '图的存储', link: '/ch06-graph/#storage' },
          { text: 'BFS / DFS', link: '/ch06-graph/#traversal' },
          { text: '最小生成树', link: '/ch06-graph/#mst' },
          { text: '最短路径', link: '/ch06-graph/#shortest-path' },
          { text: '拓扑排序 & 关键路径', link: '/ch06-graph/#topo' },
        ]
      }],
      '/ch07-search/': [{
        text: '第7章 查找', items: [
          { text: '顺序/折半/分块查找', link: '/ch07-search/#basic' },
          { text: 'BST & AVL树', link: '/ch07-search/#bst-avl' },
          { text: '散列表', link: '/ch07-search/#hash' },
        ]
      }],
      '/ch08-sort/': [{
        text: '第8章 排序', items: [
          { text: '插入排序类', link: '/ch08-sort/#insertion' },
          { text: '交换排序类', link: '/ch08-sort/#exchange' },
          { text: '选择排序类', link: '/ch08-sort/#selection' },
          { text: '归并 & 基数排序', link: '/ch08-sort/#merge-radix' },
          { text: '排序算法比较', link: '/ch08-sort/#comparison' },
        ]
      }],
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/yanqiangmiffy/cs408-tutorials' }
    ],

    footer: {
      message: '基于 MIT 许可发布',
      copyright: 'Copyright © 2026 · 408数据结构Python实现'
    },

    search: {
      provider: 'local'
    },

    editLink: {
      pattern: 'https://github.com/yanqiangmiffy/cs408-tutorials/edit/main/docs/docs/:path',
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
