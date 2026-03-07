# 第4章 串

> 408考研数据结构 · 第4章

## 知识点

| 编号 | 内容 | 文件 |
|------|------|------|
| 4.1-4.2 | 串的模式匹配(朴素/KMP/next/nextval) | `4_1_pattern_matching.py` |

## 运行

```bash
python 4_string/4_1_pattern_matching.py
```

## 考研要点

- **朴素匹配**: O(mn), 每次失败主串回溯
- **KMP**: O(m+n), 主串不回溯, 模式按 next 跳转
- **next 数组**: pattern[0..j-1] 最长公共前后缀长度
- **nextval 优化**: 避免跳转后还是失败的情况
- **手算 next/nextval**: 考研必考, 务必熟练!
