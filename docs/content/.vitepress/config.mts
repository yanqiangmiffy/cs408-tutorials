import { defineConfig, type DefaultTheme } from 'vitepress'
import { defineTeekConfig } from 'vitepress-theme-teek/config'

const siteBase = '/cs408-tutorials/'
const teekConfig = defineTeekConfig({
  codeBlock: {
    collapseHeight: false,
  },
})

const chapterNav: DefaultTheme.NavItemWithLink[] = [
  { text: '第1章 绪论', link: '/data-structure-fundamentals/ch01-intro/' },
  { text: '第2章 线性表', link: '/data-structure-fundamentals/ch02-linear/' },
  { text: '第3章 栈与队列', link: '/data-structure-fundamentals/ch03-stack-queue/' },
  { text: '第4章 串', link: '/data-structure-fundamentals/ch04-string/' },
  { text: '第5章 树与二叉树', link: '/data-structure-fundamentals/ch05-tree/' },
  { text: '第6章 图', link: '/data-structure-fundamentals/ch06-graph/' },
  { text: '第7章 查找', link: '/data-structure-fundamentals/ch07-search/' },
  { text: '第8章 排序', link: '/data-structure-fundamentals/ch08-sort/' },
  { text: '剑指 Offer', link: '/coding-interview-offer/' },
  { text: '408 真题', link: '/408-exam-questions/' },
  { text: '冲刺速记', link: '/408-exam-questions/sprint/' },
]

export default defineConfig({
  extends: teekConfig,
  base: siteBase,
  lang: 'zh-CN',
  title: '408数据结构 · Python实现',
  description: '王道408数据结构全部章节Python代码实现，含原理讲解、复杂度分析与考研要点',

  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: `${siteBase}logo.svg` }],
    ['meta', { name: 'theme-color', content: '#3c8772' }],
  ],

  themeConfig: {
    logo: '/logo.svg',
    siteTitle: '408数据结构',

    nav: [
      { text: '首页', link: '/' },
      { text: '快速开始', link: '/guide/getting-started' },
      { text: '基础知识', link: '/data-structure-fundamentals/' },
      { text: '章节', items: chapterNav },
      { text: '剑指 Offer', link: '/coding-interview-offer/' },
      { text: '408 真题', link: '/408-exam-questions/' },
    ],

    sidebar: {
      '/data-structure-fundamentals/': [{
        text: '数据结构基础',
        items: [
          { text: '总目录', link: '/data-structure-fundamentals/' },
          { text: '第1章 绪论', link: '/data-structure-fundamentals/ch01-intro/' },
          { text: '第2章 线性表', link: '/data-structure-fundamentals/ch02-linear/' },
          { text: '第3章 栈与队列', link: '/data-structure-fundamentals/ch03-stack-queue/' },
          { text: '第4章 串', link: '/data-structure-fundamentals/ch04-string/' },
          { text: '第5章 树与二叉树', link: '/data-structure-fundamentals/ch05-tree/' },
          { text: '第6章 图', link: '/data-structure-fundamentals/ch06-graph/' },
          { text: '第7章 查找', link: '/data-structure-fundamentals/ch07-search/' },
          { text: '第8章 排序', link: '/data-structure-fundamentals/ch08-sort/' },
        ],
      }],
      '/data-structure-fundamentals/ch01-intro/': [{
        text: '第1章 绪论',
        items: [
          { text: '基本概念与三要素', link: '/data-structure-fundamentals/ch01-intro/#concepts' },
          { text: '时间复杂度', link: '/data-structure-fundamentals/ch01-intro/#time-complexity' },
          { text: '空间复杂度', link: '/data-structure-fundamentals/ch01-intro/#space-complexity' },
        ],
      }],
      '/data-structure-fundamentals/ch02-linear/': [{
        text: '第2章 线性表',
        items: [
          { text: '顺序表', link: '/data-structure-fundamentals/ch02-linear/#sequential' },
          { text: '单链表', link: '/data-structure-fundamentals/ch02-linear/#singly-linked' },
          { text: '双链表', link: '/data-structure-fundamentals/ch02-linear/#doubly-linked' },
          { text: '循环链表', link: '/data-structure-fundamentals/ch02-linear/#circular' },
          { text: '静态链表', link: '/data-structure-fundamentals/ch02-linear/#static' },
        ],
      }],
      '/data-structure-fundamentals/ch03-stack-queue/': [{
        text: '第3章 栈与队列',
        items: [
          { text: '栈', link: '/data-structure-fundamentals/ch03-stack-queue/#stack' },
          { text: '队列', link: '/data-structure-fundamentals/ch03-stack-queue/#queue' },
          { text: '栈的应用', link: '/data-structure-fundamentals/ch03-stack-queue/#applications' },
          { text: '矩阵压缩', link: '/data-structure-fundamentals/ch03-stack-queue/#matrix' },
        ],
      }],
      '/data-structure-fundamentals/ch04-string/': [{
        text: '第4章 串',
        items: [
          { text: '朴素匹配', link: '/data-structure-fundamentals/ch04-string/#naive' },
          { text: 'KMP算法', link: '/data-structure-fundamentals/ch04-string/#kmp' },
        ],
      }],
      '/data-structure-fundamentals/ch05-tree/': [{
        text: '第5章 树与二叉树',
        items: [
          { text: '二叉树遍历', link: '/data-structure-fundamentals/ch05-tree/#traversal' },
          { text: '线索二叉树', link: '/data-structure-fundamentals/ch05-tree/#threaded' },
          { text: '哈夫曼树', link: '/data-structure-fundamentals/ch05-tree/#huffman' },
          { text: '并查集', link: '/data-structure-fundamentals/ch05-tree/#union-find' },
        ],
      }],
      '/data-structure-fundamentals/ch06-graph/': [{
        text: '第6章 图',
        items: [
          { text: '图的存储', link: '/data-structure-fundamentals/ch06-graph/#storage' },
          { text: 'BFS / DFS', link: '/data-structure-fundamentals/ch06-graph/#traversal' },
          { text: '最小生成树', link: '/data-structure-fundamentals/ch06-graph/#mst' },
          { text: '最短路径', link: '/data-structure-fundamentals/ch06-graph/#shortest-path' },
          { text: '拓扑排序与关键路径', link: '/data-structure-fundamentals/ch06-graph/#topo' },
        ],
      }],
      '/data-structure-fundamentals/ch07-search/': [{
        text: '第7章 查找',
        items: [
          { text: '顺序查找', link: '/data-structure-fundamentals/ch07-search/#sequential' },
          { text: '折半查找', link: '/data-structure-fundamentals/ch07-search/#binary' },
          { text: '分块查找', link: '/data-structure-fundamentals/ch07-search/#block' },
          { text: 'BST 二叉排序树', link: '/data-structure-fundamentals/ch07-search/#bst' },
          { text: 'AVL 平衡二叉树', link: '/data-structure-fundamentals/ch07-search/#avl' },
          { text: 'B树', link: '/data-structure-fundamentals/ch07-search/#btree' },
          { text: 'B+树', link: '/data-structure-fundamentals/ch07-search/#bplustree' },
          { text: '红黑树', link: '/data-structure-fundamentals/ch07-search/#redblack' },
          { text: '散列表', link: '/data-structure-fundamentals/ch07-search/#hash' },
          { text: '复杂度总结', link: '/data-structure-fundamentals/ch07-search/#summary' },
        ],
      }],
      '/data-structure-fundamentals/ch08-sort/': [{
        text: '第8章 排序',
        items: [
          { text: '插入排序类', link: '/data-structure-fundamentals/ch08-sort/#insertion' },
          { text: '交换排序类', link: '/data-structure-fundamentals/ch08-sort/#exchange' },
          { text: '选择排序类', link: '/data-structure-fundamentals/ch08-sort/#selection' },
          { text: '归并与基数排序', link: '/data-structure-fundamentals/ch08-sort/#merge-radix' },
          { text: '排序算法比较', link: '/data-structure-fundamentals/ch08-sort/#comparison' },
        ],
      }],
      '/coding-interview-offer/': [{
        text: '剑指 Offer',
        items: [
          { text: '总目录', link: '/coding-interview-offer/' },
          {
            text: '数组',
            collapsed: true,
            items: [
              { text: '01 二维数组中的查找', link: '/coding-interview-offer/01' },
              { text: '06 旋转数组的最小数字', link: '/coding-interview-offer/06' },
              { text: '13 调整数组顺序', link: '/coding-interview-offer/13' },
              { text: '28 数组中出现次数超过一半的数字', link: '/coding-interview-offer/28' },
              { text: '29 最小的K个数', link: '/coding-interview-offer/29' },
              { text: '30 连续子数组的最大和', link: '/coding-interview-offer/30' },
              { text: '32 把数组排成最小的数', link: '/coding-interview-offer/32' },
              { text: '35 数组中的逆序对', link: '/coding-interview-offer/35' },
              { text: '37 数字在排序数组中出现的次数', link: '/coding-interview-offer/37' },
              { text: '50 数组中重复的数字', link: '/coding-interview-offer/50' },
              { text: '51 构建乘积数组', link: '/coding-interview-offer/51' },
              { text: '64 滑动窗口的最大值', link: '/coding-interview-offer/64' },
            ],
          },
          {
            text: '链表',
            collapsed: true,
            items: [
              { text: '03 从尾到头打印链表', link: '/coding-interview-offer/03' },
              { text: '14 链表中倒数第k个结点', link: '/coding-interview-offer/14' },
              { text: '15 反转链表', link: '/coding-interview-offer/15' },
              { text: '16 合并两个排序的链表', link: '/coding-interview-offer/16' },
              { text: '25 复杂链表的复制', link: '/coding-interview-offer/25' },
              { text: '36 两个链表的第一个公共结点', link: '/coding-interview-offer/36' },
              { text: '55 链表中环的入口结点', link: '/coding-interview-offer/55' },
              { text: '56 删除链表中重复的结点', link: '/coding-interview-offer/56' },
            ],
          },
          {
            text: '树',
            collapsed: true,
            items: [
              { text: '04 重建二叉树', link: '/coding-interview-offer/04' },
              { text: '17 树的子结构', link: '/coding-interview-offer/17' },
              { text: '18 二叉树的镜像', link: '/coding-interview-offer/18' },
              { text: '22 从上往下打印二叉树', link: '/coding-interview-offer/22' },
              { text: '23 二叉搜索树的后序遍历序列', link: '/coding-interview-offer/23' },
              { text: '24 二叉树中和为某一值的路径', link: '/coding-interview-offer/24' },
              { text: '26 二叉搜索树与双向链表', link: '/coding-interview-offer/26' },
              { text: '38 二叉树的深度', link: '/coding-interview-offer/38' },
              { text: '39 平衡二叉树', link: '/coding-interview-offer/39' },
              { text: '57 二叉树的下一个结点', link: '/coding-interview-offer/57' },
              { text: '58 对称的二叉树', link: '/coding-interview-offer/58' },
              { text: '59 按之字形顺序打印二叉树', link: '/coding-interview-offer/59' },
              { text: '60 把二叉树打印成多行', link: '/coding-interview-offer/60' },
              { text: '61 序列化二叉树', link: '/coding-interview-offer/61' },
              { text: '62 二叉搜索树的第k个结点', link: '/coding-interview-offer/62' },
            ],
          },
          {
            text: '栈/队列',
            collapsed: true,
            items: [
              { text: '05 用两个栈实现队列', link: '/coding-interview-offer/05' },
              { text: '20 包含min函数的栈', link: '/coding-interview-offer/20' },
              { text: '21 栈的压入、弹出序列', link: '/coding-interview-offer/21' },
              { text: '63 数据流中的中位数', link: '/coding-interview-offer/63' },
            ],
          },
          {
            text: '字符串',
            collapsed: true,
            items: [
              { text: '02 替换空格', link: '/coding-interview-offer/02' },
              { text: '27 字符串的排列', link: '/coding-interview-offer/27' },
              { text: '34 第一个只出现一次的字符', link: '/coding-interview-offer/34' },
              { text: '42 和为S的连续正数序列', link: '/coding-interview-offer/42' },
              { text: '43 左旋转字符串', link: '/coding-interview-offer/43' },
              { text: '44 翻转单词顺序列', link: '/coding-interview-offer/44' },
              { text: '49 把字符串转换成整数', link: '/coding-interview-offer/49' },
              { text: '52 正则表达式匹配', link: '/coding-interview-offer/52' },
              { text: '53 表示数值的字符串', link: '/coding-interview-offer/53' },
              { text: '54 字符流中第一个不重复的字符', link: '/coding-interview-offer/54' },
            ],
          },
          {
            text: '动态规划',
            collapsed: true,
            items: [
              { text: '07 斐波那契数列', link: '/coding-interview-offer/07' },
              { text: '08 跳台阶', link: '/coding-interview-offer/08' },
              { text: '09 变态跳台阶', link: '/coding-interview-offer/09' },
              { text: '10 矩形覆盖', link: '/coding-interview-offer/10' },
              { text: '31 整数中1出现的次数', link: '/coding-interview-offer/31' },
              { text: '33 丑数', link: '/coding-interview-offer/33' },
              { text: '46 孩子们的游戏', link: '/coding-interview-offer/46' },
              { text: '47 求1+2+3+...+n', link: '/coding-interview-offer/47' },
              { text: '67 剪绳子', link: '/coding-interview-offer/67' },
            ],
          },
          {
            text: '其他',
            collapsed: true,
            items: [
              { text: '11 二进制中1的个数', link: '/coding-interview-offer/11' },
              { text: '12 数值的整数次方', link: '/coding-interview-offer/12' },
              { text: '19 顺时针打印矩阵', link: '/coding-interview-offer/19' },
              { text: '40 数组中只出现一次的数字', link: '/coding-interview-offer/40' },
              { text: '41 和为S的两个数字', link: '/coding-interview-offer/41' },
              { text: '45 扑克牌顺子', link: '/coding-interview-offer/45' },
              { text: '48 不用加减乘除做加法', link: '/coding-interview-offer/48' },
              { text: '65 矩阵中的路径', link: '/coding-interview-offer/65' },
              { text: '66 机器人的运动范围', link: '/coding-interview-offer/66' },
            ],
          },
        ],
      }],
      '/408-exam-questions/': [{
        text: '第10章 408 大题真题',
        items: [
          { text: '总目录', link: '/408-exam-questions/' },
          {
            text: '2009-2016',
            collapsed: true,
            items: [
              { text: '2009 第42题', link: '/408-exam-questions/2009' },
              { text: '2010 第42题', link: '/408-exam-questions/2010' },
              { text: '2011 第42题', link: '/408-exam-questions/2011' },
              { text: '2012 第42题', link: '/408-exam-questions/2012' },
              { text: '2013 第41题', link: '/408-exam-questions/2013' },
              { text: '2014 第41题', link: '/408-exam-questions/2014' },
              { text: '2015 第41题', link: '/408-exam-questions/2015' },
              { text: '2016 第43题', link: '/408-exam-questions/2016' },
            ],
          },
          {
            text: '2017-2024',
            collapsed: true,
            items: [
              { text: '2017 第41题', link: '/408-exam-questions/2017' },
              { text: '2018 第41题', link: '/408-exam-questions/2018' },
              { text: '2019 第41题', link: '/408-exam-questions/2019' },
              { text: '2020 第41题', link: '/408-exam-questions/2020' },
              { text: '2021 第41题', link: '/408-exam-questions/2021' },
              { text: '2022 第41题', link: '/408-exam-questions/2022' },
              { text: '2023 第41题', link: '/408-exam-questions/2023' },
              { text: '2024 第41题', link: '/408-exam-questions/2024' },
            ],
          },
        ],
      }],
      '/408-exam-questions/sprint/': [{
        text: '第11章 冲刺与速记',
        items: [
          { text: '总目录', link: '/408-exam-questions/sprint/' },
          { text: '高频考点速记', link: '/408-exam-questions/sprint/01-high-frequency' },
          { text: '手写模板库', link: '/408-exam-questions/sprint/02-handwriting-templates' },
          { text: '易错点总表', link: '/408-exam-questions/sprint/03-mistakes' },
          { text: '复杂度对比总表', link: '/408-exam-questions/sprint/04-complexity-comparison' },
          { text: '真题题型索引', link: '/408-exam-questions/sprint/05-qa-taxonomy' },
          { text: '大题答题模板', link: '/408-exam-questions/sprint/06-answer-templates' },
          { text: '30 天复习路线', link: '/408-exam-questions/sprint/07-roadmap-30days' },
          { text: '术语对照表', link: '/408-exam-questions/sprint/08-terminology' },
          { text: '章节自测题', link: '/408-exam-questions/sprint/09-self-test' },
          { text: '错题复盘模板', link: '/408-exam-questions/sprint/10-review-template' },
          { text: '一页纸总结', link: '/408-exam-questions/sprint/11-cheatsheets' },
        ],
      }],
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/yanqiangmiffy/cs408-tutorials' },
    ],

    footer: {
      message: '基于 MIT 许可发布',
      copyright: 'Copyright © 2026 · 408数据结构 Python 实现',
    },

    search: {
      provider: 'local',
    },

    editLink: {
      pattern: 'https://github.com/yanqiangmiffy/cs408-tutorials/edit/main/docs/content/:path',
      text: '在 GitHub 上编辑此页',
    },

    lastUpdated: {
      text: '最后更新于',
      formatOptions: { dateStyle: 'short' },
    },
  },

  markdown: {
    theme: {
      light: 'github-light',
      dark: 'one-dark-pro',
    },
    lineNumbers: true,
  },
})
