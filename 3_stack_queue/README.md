# 第3章 栈、队列和数组

> 408考研数据结构 · 第3章

## 知识点

| 编号 | 内容 | 文件 |
|------|------|------|
| 3.1 | 栈(顺序栈/链栈/共享栈) | `3_1_stack.py` |
| 3.2 | 队列(循环队列/链队列/双端队列) | `3_2_queue.py` |
| 3.3 | 栈的应用(括号匹配/表达式求值) | `3_3_stack_applications.py` |
| 3.4 | 特殊矩阵的压缩存储 | `3_4_matrix_compression.py` |

## 运行

```bash
python 3_stack_queue/3_1_stack.py
python 3_stack_queue/3_2_queue.py
python 3_stack_queue/3_3_stack_applications.py
python 3_stack_queue/3_4_matrix_compression.py
```

## 考研要点

- **栈**: LIFO, top 初始值影响代码, 卡特兰数
- **队列**: FIFO, 循环队列判空满三种方法
- **中缀转后缀**: 操作数直输出, 运算符比较优先级
- **矩阵压缩**: 对称矩阵 k=i(i-1)/2+j-1, 三对角 k=2i+j-3
