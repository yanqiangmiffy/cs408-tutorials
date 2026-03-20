import { defineConfig } from 'vitepress'
import { defineTeekConfig } from "vitepress-theme-teek/config";

const teekConfig = defineTeekConfig({});

export default defineConfig({
  extends: teekConfig,
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
          { text: '第1章 绪论', link: 'ch01-intro/' },
          { text: '第2章 线性表', link: 'ch02-linear/' },
          { text: '第3章 栈与队列', link: 'ch03-stack-queue/' },
          { text: '第4章 串', link: 'ch04-string/' },
          { text: '第5章 树与二叉树', link: 'ch05-tree/' },
          { text: '第6章 图', link: 'ch06-graph/' },
          { text: '第7章 查找', link: 'ch07-search/' },
          { text: '第8章 排序', link: 'ch08-sort/' },
          { text: '剑指Offer', link: 'ch09-offer/' },
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
          { text: '顺序查找', link: '/ch07-search/#sequential' },
          { text: '折半查找', link: '/ch07-search/#binary' },
          { text: '分块查找', link: '/ch07-search/#block' },
          { text: 'BST 二叉排序树', link: '/ch07-search/#bst' },
          { text: 'AVL 平衡二叉树', link: '/ch07-search/#avl' },
          { text: 'B树', link: '/ch07-search/#btree' },
          { text: 'B+树', link: '/ch07-search/#bplustree' },
          { text: '红黑树', link: '/ch07-search/#redblack' },
          { text: '散列表', link: '/ch07-search/#hash' },
          { text: '复杂度总结', link: '/ch07-search/#summary' },
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
      '/ch09-offer/': [{
        text: '剑指Offer', items: [
          { text: '总目录', link: '/ch09-offer/' },
          { text: '数组', collapsed: true, items: [
            { text: '01 二维数组中的查找', link: '/ch09-offer/01' },
            { text: '06 旋转数组的最小数字', link: '/ch09-offer/06' },
            { text: '13 调整数组顺序', link: '/ch09-offer/13' },
            { text: '28 数组中出现次数超过一半的数字', link: '/ch09-offer/28' },
            { text: '29 最小的K个数', link: '/ch09-offer/29' },
            { text: '30 连续子数组的最大和', link: '/ch09-offer/30' },
            { text: '32 把数组排成最小的数', link: '/ch09-offer/32' },
            { text: '35 数组中的逆序对', link: '/ch09-offer/35' },
            { text: '37 数字在排序数组中出现的次数', link: '/ch09-offer/37' },
            { text: '50 数组中重复的数字', link: '/ch09-offer/50' },
            { text: '51 构建乘积数组', link: '/ch09-offer/51' },
            { text: '64 滑动窗口的最大值', link: '/ch09-offer/64' },
          ]},
          { text: '链表', collapsed: true, items: [
            { text: '03 从尾到头打印链表', link: '/ch09-offer/03' },
            { text: '14 链表中倒数第k个结点', link: '/ch09-offer/14' },
            { text: '15 反转链表', link: '/ch09-offer/15' },
            { text: '16 合并两个排序的链表', link: '/ch09-offer/16' },
            { text: '25 复杂链表的复制', link: '/ch09-offer/25' },
            { text: '36 两个链表的第一个公共结点', link: '/ch09-offer/36' },
            { text: '55 链表中环的入口结点', link: '/ch09-offer/55' },
            { text: '56 删除链表中重复的结点', link: '/ch09-offer/56' },
          ]},
          { text: '树', collapsed: true, items: [
            { text: '04 重建二叉树', link: '/ch09-offer/04' },
            { text: '17 树的子结构', link: '/ch09-offer/17' },
            { text: '18 二叉树的镜像', link: '/ch09-offer/18' },
            { text: '22 从上往下打印二叉树', link: '/ch09-offer/22' },
            { text: '23 二叉搜索树的后序遍历序列', link: '/ch09-offer/23' },
            { text: '24 二叉树中和为某一值的路径', link: '/ch09-offer/24' },
            { text: '26 二叉搜索树与双向链表', link: '/ch09-offer/26' },
            { text: '38 二叉树的深度', link: '/ch09-offer/38' },
            { text: '39 平衡二叉树', link: '/ch09-offer/39' },
            { text: '57 二叉树的下一个结点', link: '/ch09-offer/57' },
            { text: '58 对称的二叉树', link: '/ch09-offer/58' },
            { text: '59 按之字形顺序打印二叉树', link: '/ch09-offer/59' },
            { text: '60 把二叉树打印成多行', link: '/ch09-offer/60' },
            { text: '61 序列化二叉树', link: '/ch09-offer/61' },
            { text: '62 二叉搜索树的第k个结点', link: '/ch09-offer/62' },
          ]},
          { text: '栈/队列', collapsed: true, items: [
            { text: '05 用两个栈实现队列', link: '/ch09-offer/05' },
            { text: '20 包含min函数的栈', link: '/ch09-offer/20' },
            { text: '21 栈的压入、弹出序列', link: '/ch09-offer/21' },
            { text: '63 数据流中的中位数', link: '/ch09-offer/63' },
          ]},
          { text: '字符串', collapsed: true, items: [
            { text: '02 替换空格', link: '/ch09-offer/02' },
            { text: '27 字符串的排列', link: '/ch09-offer/27' },
            { text: '34 第一个只出现一次的字符', link: '/ch09-offer/34' },
            { text: '42 和为S的连续正数序列', link: '/ch09-offer/42' },
            { text: '43 左旋转字符串', link: '/ch09-offer/43' },
            { text: '44 翻转单词顺序列', link: '/ch09-offer/44' },
            { text: '49 把字符串转换成整数', link: '/ch09-offer/49' },
            { text: '52 正则表达式匹配', link: '/ch09-offer/52' },
            { text: '53 表示数值的字符串', link: '/ch09-offer/53' },
            { text: '54 字符流中第一个不重复的字符', link: '/ch09-offer/54' },
          ]},
          { text: '动态规划', collapsed: true, items: [
            { text: '07 斐波那契数列', link: '/ch09-offer/07' },
            { text: '08 跳台阶', link: '/ch09-offer/08' },
            { text: '09 变态跳台阶', link: '/ch09-offer/09' },
            { text: '10 矩形覆盖', link: '/ch09-offer/10' },
            { text: '31 整数中1出现的次数', link: '/ch09-offer/31' },
            { text: '33 丑数', link: '/ch09-offer/33' },
            { text: '46 孩子们的游戏', link: '/ch09-offer/46' },
            { text: '47 求1+2+3+...+n', link: '/ch09-offer/47' },
            { text: '67 剪绳子', link: '/ch09-offer/67' },
          ]},
          { text: '其他', collapsed: true, items: [
            { text: '11 二进制中1的个数', link: '/ch09-offer/11' },
            { text: '12 数值的整数次方', link: '/ch09-offer/12' },
            { text: '19 顺时针打印矩阵', link: '/ch09-offer/19' },
            { text: '40 数组中只出现一次的数字', link: '/ch09-offer/40' },
            { text: '41 和为S的两个数字', link: '/ch09-offer/41' },
            { text: '45 扑克牌顺子', link: '/ch09-offer/45' },
            { text: '48 不用加减乘除做加法', link: '/ch09-offer/48' },
            { text: '65 矩阵中的路径', link: '/ch09-offer/65' },
            { text: '66 机器人的运动范围', link: '/ch09-offer/66' },
          ]},
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
      pattern: 'https://github.com/yanqiangmiffy/cs408-tutorials/edit/main/docs/content/:path',
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
