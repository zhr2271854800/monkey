# 钠电正极结构学与晶体场理论交互指南
### Sodium-ion Battery Cathode Structures, Crystal Field Theory & Jahn-Teller Distortion

[![GitHub Pages](https://img.shields.io/badge/Live_Demo-GitHub_Pages-2d6a4f?style=flat-square&logo=github)](https://zhr2271854800.github.io/monkey/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](LICENSE)
[![Topic](https://img.shields.io/badge/Domain-Energy_Storage_%7C_Solid_State_Chemistry-b8860b?style=flat-square)](#)

> 本项目为钠离子电池层状过渡金属氧化物（$\mathrm{Na}_x\mathrm{TMO}_2$）正极材料的结构学、晶体场理论（CFT）与姜-泰勒（Jahn-Teller）效应的交互式可视化教学与研究指南。

---

## 📖 核心知识架构与模块导览

本项目通过学术图文、配位多面体剖析及三维轨道劈裂示意图，系统解构了钠电正极的微观化学机制：

| 模块序号 | 章节主题 | 核心化学概念与物理图像 |
| :---: | :--- | :--- |
| **01 - 04** | **层状骨架与配位多面体** | $\mathrm{Na}_x\mathrm{TMO}_2$ 结构、八面体（Octahedron）vs 三棱柱（Prism）、共面/共棱跳跃势垒 |
| **05 - 08** | **Delmas 命名法与晶体相变** | 字母（O/P）与数字周期（2/3/1）的本质含义、O3 相密堆积（$\mathrm{ABCABC}$）与 P2 相密堆积（$\mathrm{ABBA}$） |
| **09 - 10** | **综合对比与速记图谱** | O3 vs P2 综合电化学性能对比（初始容量、倍率性能、空穴稳定性、相变复杂性） |
| **11** | **晶体场理论（CFT）** | $\mathrm{ML_6}$ 八面体场中的 $d$ 轨道劈裂、$e_g$ 轴向迎头排斥 vs $t_{2g}$ 45°夹缝避让、高自旋（HS）与低自旋（LS） |
| **12 - 13** | **姜-泰勒畸变（Jahn-Teller）** | $e_g^1$ 单电子简并解除机制、八面体轴向拉长/压扁、$\mathrm{Mn^{3+}}$ 出生畸变 vs $\mathrm{Fe^{4+}}$ 高电位氧化与协同相变 |
| **14** | **元素掺杂调控机制** | 稀释效应、价态钉扎、$\mathrm{Ti/Al}$ 强键钉氧、离子半径失配与微观协同相变阻断 |
| **15** | **代码与可视化工程** | 基于 Python (`numpy` + `matplotlib`) 的晶体多面体顶点映射与高清图谱自动化绘制 |
| **16** | **2026 层状正极化学** | 电荷补偿阶梯、高电压 c 轴坍塌、构型熵、O3@P2 外延、双相互锁、Al/Ti 钉氧、阴离子双参数、氧氧化还原 |

---

## 🎨 视觉风格与工程特色

- **学术论文级排版美学**：采用定制暖色羊皮纸底色（Warm Paper: `#f7f4ee`）、内敛典雅的深青/铜金学术色彩体系（`#1d4e89` / `#b8860b` / `#2d6a4f`）。
- **完全解耦与纯净静态**：零前端打包工具依赖（无需 node_modules），纯原生 HTML5 + CSS3 Flex/Grid 弹性网格排版，移动端与 PC 端无缝自适应。
- **全套原创学术插图**：包含 29 张高精度结构机理图谱（八面体群、d 轨道空间分布、Delmas 堆叠序列、协同相变模拟等）。

---

## 🌐 在线体验与本地部署

### 1. 在线浏览 (GitHub Pages)
直接访问已部署的全球 CDN 页面：
👉 **[https://zhr2271854800.github.io/monkey/](https://zhr2271854800.github.io/monkey/)**

### 2. 本地即开即用
克隆本仓库到本地后，直接用任意现代浏览器双击打开 `index.html` 即可：
```bash
git clone https://github.com/zhr2271854800/monkey.git
cd monkey
# 浏览器打开 index.html 即可浏览全部交互内容
start index.html
```

---

## 📂 项目文件清单

```text
monkey/
├── index.html            # 核心交互式多章节学术指南单页
├── sib-2026.html         # 2026 年层状正极化学视角文献图文页
├── scripts/
│   ├── draw_sib_structures.py  # 结构学 / 晶体场 / 姜-泰勒 29 图
│   └── draw_sib_2026.py        # 2026 文献化学视角 14 图
├── style.css             # 顶刊学术风排版样式表 (CSS Grid, 卡片化排版)
├── README.md             # 项目架构与学术说明文档
├── .gitignore            # Git 忽略配置
└── images/               # 29 张高清晰度学术机理矢量/位图资产
    ├── 01_polyhedra.png        # 八面体 vs 三棱柱配位
    ├── ...
    ├── 25_ml6_octahedron.png   # ML6 八面体配位场
    ├── 26_d_orbitals.png       # 5 条 d 轨道空间取向
    ├── 27_pointing.png         # dx2-y2 与 dxy 对准效应
    ├── 28_octahedral_split.png # 八面体晶体场轨道分裂 (10 Dq)
    └── 29_hs_ls.png            # 高自旋与低自旋电子排布
```

---

## 📜 许可证 (License)

本项目基于 [MIT 许可证](LICENSE) 开源发布。
