# 第6章 图

> 408考研数据结构 · 第6章

## 知识点

| 编号 | 内容 | 文件 |
|------|------|------|
| 6.2 | 图的存储结构(邻接矩阵/邻接表) | `6_2_graph_storage.py` |
| 6.3 | 图的BFS和DFS遍历 | `6_3_bfs_dfs.py` |
| 6.4.1 | 最小生成树(Prim/Kruskal) | `6_4_mst.py` |
| 6.4.2 | 最短路径(Dijkstra/Floyd) | `6_4_shortest_path.py` |
| 6.4.4-6.4.5 | 拓扑排序与关键路径 | `6_4_topo_critical_path.py` |

## 运行

```bash
python 6_graph/6_2_graph_storage.py
python 6_graph/6_3_bfs_dfs.py
python 6_graph/6_4_mst.py
python 6_graph/6_4_shortest_path.py
python 6_graph/6_4_topo_critical_path.py
```

## 考研要点

- **存储**: 邻接矩阵 O(V²) 适合稠密图, 邻接表 O(V+E) 适合稀疏图
- **MST**: Prim 从顶点扩展, Kruskal 从最小边选
- **最短路**: Dijkstra 不能负权, Floyd O(V³) 多源
- **拓扑排序**: 每次选入度为0的顶点
- **关键路径**: ve/vl/e/l 四个数组, e==l 是关键
