# -*- coding: utf-8 -*-
"""
scripts/draw_sib_structures.py
为钠电正极结构学与晶体场理论交互指南自动生成全套 29 张高精度学术机理插图
技术栈: Python 3 + NumPy + Matplotlib
输出目标: web/images/ 或 images/
"""

import os
import sys
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Rectangle, FancyArrowPatch, Wedge
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# 全局学术出版绘图配置
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial', 'DejaVu Sans']
mpl.rcParams['axes.unicode_minus'] = False
mpl.rcParams['figure.autolayout'] = True
mpl.rcParams['savefig.dpi'] = 200
mpl.rcParams['savefig.bbox'] = 'tight'

# 配色规范
C_O3 = '#1d4e89'     # O3 经典深蓝
C_P2 = '#2d6a4f'     # P2 森林墨绿
C_NA = '#e69f00'     # 钠离子金黄
C_TM = '#00a087'     # 过渡金属青绿
C_O = '#e74c3c'      # 氧原子砖红
C_ACCENT = '#b8860b' # 铜金高亮
C_BG = '#ffffff'     # 纯白底色
C_MUTED = '#5c6570'  # 辅助灰色
C_INK = '#1c2430'    # 深黑墨色

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'images'))
os.makedirs(OUT_DIR, exist_ok=True)

def save_fig(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, facecolor=C_BG, edgecolor='none')
    plt.close(fig)
    print(f"[OK] Generated: {name}")

# ==========================================
# 01. 两种笼子: 八面体 vs 三棱柱
# ==========================================
def draw_01_polyhedra():
    fig = plt.figure(figsize=(9, 4.5))
    
    # 左: 八面体 (Octahedron)
    ax1 = fig.add_subplot(121, projection='3d')
    verts_oct = [
        [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1.2], [0, 0, -1.2]
    ]
    faces_oct = [
        [verts_oct[4], verts_oct[0], verts_oct[2]],
        [verts_oct[4], verts_oct[2], verts_oct[1]],
        [verts_oct[4], verts_oct[1], verts_oct[3]],
        [verts_oct[4], verts_oct[3], verts_oct[0]],
        [verts_oct[5], verts_oct[0], verts_oct[2]],
        [verts_oct[5], verts_oct[2], verts_oct[1]],
        [verts_oct[5], verts_oct[1], verts_oct[3]],
        [verts_oct[5], verts_oct[3], verts_oct[0]],
    ]
    poly1 = Poly3DCollection(faces_oct, alpha=0.45, facecolor=C_O3, edgecolor=C_O3, linewidths=1.5)
    ax1.add_collection3d(poly1)
    # 中心 Na+
    ax1.scatter([0], [0], [0], color=C_NA, s=120, edgecolors='black', label=r'$\mathrm{Na^+}$ 位于八面体中心')
    ax1.set_title('八面体配位 (Octahedron)\nO3 型结构 (CN = 6)', fontsize=12, fontweight='bold', pad=10)
    ax1.set_axis_off()
    ax1.set_xlim([-1.2, 1.2]); ax1.set_ylim([-1.2, 1.2]); ax1.set_zlim([-1.4, 1.4])
    ax1.legend(loc='lower center', frameon=False)

    # 右: 三棱柱 (Prism)
    ax2 = fig.add_subplot(122, projection='3d')
    r, h = 1.0, 1.0
    angles = np.array([0, 2*np.pi/3, 4*np.pi/3])
    top = np.column_stack([r*np.cos(angles), r*np.sin(angles), np.full(3, h)])
    bot = np.column_stack([r*np.cos(angles), r*np.sin(angles), np.full(3, -h)])
    faces_prism = [
        [top[0], top[1], top[2]], # 顶面
        [bot[0], bot[1], bot[2]], # 底面
        [top[0], top[1], bot[1], bot[0]], # 侧面1
        [top[1], top[2], bot[2], bot[1]], # 侧面2
        [top[2], top[0], bot[0], bot[2]], # 侧面3
    ]
    poly2 = Poly3DCollection(faces_prism, alpha=0.45, facecolor=C_P2, edgecolor=C_P2, linewidths=1.5)
    ax2.add_collection3d(poly2)
    ax2.scatter([0], [0], [0], color=C_NA, s=120, edgecolors='black', label=r'$\mathrm{Na^+}$ 位于三棱柱中心')
    ax2.set_title('三棱柱配位 (Prism)\nP2 型结构 (CN = 6)', fontsize=12, fontweight='bold', pad=10)
    ax2.set_axis_off()
    ax2.set_xlim([-1.2, 1.2]); ax2.set_ylim([-1.2, 1.2]); ax2.set_zlim([-1.4, 1.4])
    ax2.legend(loc='lower center', frameon=False)

    save_fig(fig, '01_polyhedra.png')

# ==========================================
# 02. 跳跃窗口: 三角形面 vs 矩形侧面
# ==========================================
def draw_02_hop_windows():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 4.2))
    
    # 左: 八面体共享三角形面 (窄小 bottleneck)
    tri = np.array([[0, 0], [2, 0], [1, np.sqrt(3)]])
    poly1 = Polygon(tri, facecolor='#f8d7da', edgecolor=C_O, linewidth=2, alpha=0.6)
    ax1.add_patch(poly1)
    for p in tri:
        ax1.add_patch(Circle(p, 0.18, color=C_O, zorder=5))
        ax1.text(p[0], p[1], r'$\mathrm{O^{2-}}$', color='white', ha='center', va='center', fontsize=9, fontweight='bold')
    # Na 穿过中间
    ax1.add_patch(Circle([1, np.sqrt(3)/3], 0.22, color=C_NA, ec='black', zorder=6))
    ax1.text(1, np.sqrt(3)/3, r'$\mathrm{Na^+}$', color='black', ha='center', va='center', fontsize=9, fontweight='bold')
    ax1.set_xlim(-0.5, 2.5); ax1.set_ylim(-0.5, 2.2)
    ax1.set_title('八面体跳跃: 面共享三角形窗口\n(窄小瓶颈，需越过四面体中间态，能垒高)', fontsize=11, fontweight='bold')
    ax1.set_aspect('equal')
    ax1.axis('off')

    # 右: 三棱柱共享矩形侧面 (宽阔 direct hop)
    rect = np.array([[0, 0], [2.2, 0], [2.2, 1.6], [0, 1.6]])
    poly2 = Polygon(rect, facecolor='#d4edda', edgecolor=C_P2, linewidth=2, alpha=0.6)
    ax2.add_patch(poly2)
    for p in rect:
        ax2.add_patch(Circle(p, 0.18, color=C_O, zorder=5))
        ax2.text(p[0], p[1], r'$\mathrm{O^{2-}}$', color='white', ha='center', va='center', fontsize=9, fontweight='bold')
    ax2.add_patch(Circle([1.1, 0.8], 0.22, color=C_NA, ec='black', zorder=6))
    ax2.text(1.1, 0.8, r'$\mathrm{Na^+}$', color='black', ha='center', va='center', fontsize=9, fontweight='bold')
    ax2.set_xlim(-0.5, 2.7); ax2.set_ylim(-0.5, 2.2)
    ax2.set_title('三棱柱跳跃: 矩形共面窗口\n(开放开阔，直接在棱柱间滑移，能垒低)', fontsize=11, fontweight='bold')
    ax2.set_aspect('equal')
    ax2.axis('off')

    save_fig(fig, '02_hop_windows.png')

# ==========================================
# 05. Delmas 命名法示意图
# ==========================================
def draw_05_delmas():
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.axis('off')
    
    # 标题卡片
    ax.text(0.5, 0.90, "Delmas 晶体学命名法解构 (O3 / P2 / P3 / O2)", ha='center', va='center', fontsize=14, fontweight='bold', color='#1c2430')
    
    # 左方块: 字母代表配位环境
    ax.add_patch(Rectangle((0.08, 0.25), 0.38, 0.52, facecolor='#e8f4fd', edgecolor=C_O3, lw=2))
    ax.text(0.27, 0.68, "第一个字母: 钠配位多面体", ha='center', va='center', fontsize=12, fontweight='bold', color=C_O3)
    ax.text(0.27, 0.52, "• O = Octahedral (八面体, CN=6)\n• P = Prismatic (三棱柱, CN=6)\n• T = Tetrahedral (四面体, CN=4)", ha='center', va='center', fontsize=10.5, color='#333333')

    # 右方块: 数字代表周期数
    ax.add_patch(Rectangle((0.54, 0.25), 0.38, 0.52, facecolor='#eafaf1', edgecolor=C_P2, lw=2))
    ax.text(0.73, 0.68, "后接数字: 晶胞层重复周期", ha='center', va='center', fontsize=12, fontweight='bold', color=C_P2)
    ax.text(0.73, 0.52, "• 3 = 穿过 3 层 TMO2 回到原位 (如 ABCABC)\n• 2 = 穿过 2 层 TMO2 回到原位 (如 ABBA)\n• 1 = 穿过 1 层 TMO2 即复位 (单层)", ha='center', va='center', fontsize=10.5, color='#333333')

    ax.text(0.5, 0.12, "核心要旨: 字母看钠坐在什么笼子里，数字看过渡金属层重复几次才闭合！", ha='center', va='center', fontsize=11, fontweight='bold', color=C_ACCENT, bbox=dict(facecolor='#fffaf3', edgecolor=C_ACCENT, pad=5, boxstyle='round,pad=0.5'))
    
    save_fig(fig, '05_delmas.png')

# ==========================================
# 03 & 04. O3 与 P2 侧视堆叠序列
# ==========================================
def draw_03_o3_stacking():
    fig, ax = plt.subplots(figsize=(7.5, 5))
    layers = ['A (O)', 'B (TM)', 'C (O)', 'A (Na)', 'B (O)', 'C (TM)', 'A (O)', 'B (Na)', 'C (O)', 'A (TM)', 'B (O)', 'C (Na)']
    colors = [C_O, C_TM, C_O, C_NA, C_O, C_TM, C_O, C_NA, C_O, C_TM, C_O, C_NA]
    
    y = np.linspace(0, 4.4, len(layers))
    for i, (l, c) in enumerate(zip(layers, colors)):
        ax.axhline(y[i], color=c, lw=3, alpha=0.7)
        ax.text(-0.2, y[i], l, ha='right', va='center', fontsize=10, fontweight='bold', color=c)
        # 点状原子
        xs = np.linspace(0.2, 3.8, 7)
        ax.scatter(xs, np.full_like(xs, y[i]), color=c, s=50, zorder=4)

    ax.set_xlim(-1.0, 4.2); ax.set_ylim(-0.3, 4.8)
    ax.set_title("O3 侧视堆叠: ABCABC 氧骨架与 3 层周期", fontsize=12, fontweight='bold')
    ax.axis('off')
    save_fig(fig, '03_o3_stacking.png')

def draw_04_p2_stacking():
    fig, ax = plt.subplots(figsize=(7.5, 5))
    layers = ['A (O)', 'B (TM)', 'B (O)', 'B/A (Na)', 'B (O)', 'A (TM)', 'A (O)', 'A/B (Na)']
    colors = [C_O, C_TM, C_O, C_NA, C_O, C_TM, C_O, C_NA]
    
    y = np.linspace(0, 4.2, len(layers))
    for i, (l, c) in enumerate(zip(layers, colors)):
        ax.axhline(y[i], color=c, lw=3, alpha=0.7)
        ax.text(-0.2, y[i], l, ha='right', va='center', fontsize=10, fontweight='bold', color=c)
        xs = np.linspace(0.2, 3.8, 7)
        ax.scatter(xs, np.full_like(xs, y[i]), color=c, s=50, zorder=4)

    ax.set_xlim(-1.0, 4.2); ax.set_ylim(-0.3, 4.6)
    ax.set_title("P2 侧视堆叠: ABBA 氧骨架与 2 层周期", fontsize=12, fontweight='bold')
    ax.axis('off')
    save_fig(fig, '04_p2_stacking.png')

# ==========================================
# 06. P2 中 Nae 与 Naf 两种钠位
# ==========================================
def draw_06_p2_na_sites():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 4.2))
    
    # Nae: 与 TMO6 共棱 (Edge-sharing)
    ax1.add_patch(Rectangle((0.2, 0.2), 0.6, 0.6, facecolor='#d4edda', edgecolor=C_P2, lw=2))
    ax1.scatter([0.2, 0.8], [0.5, 0.5], color=C_NA, s=120, ec='black', zorder=5)
    ax1.text(0.5, 0.5, "TMO6 棱", ha='center', va='center', fontsize=10, color=C_P2, fontweight='bold')
    ax1.text(0.5, 0.08, "Nae (与 TMO6 共棱)\n静电排斥小，能量更低，优先占据", ha='center', va='center', fontsize=10)
    ax1.set_xlim(0, 1); ax1.set_ylim(0, 1); ax1.axis('off')

    # Naf: 与 TMO6 共面 (Face-sharing)
    ax2.add_patch(Circle((0.5, 0.5), 0.35, facecolor='#f8d7da', edgecolor=C_O, lw=2))
    ax2.scatter([0.5], [0.5], color=C_NA, s=150, ec='black', zorder=5)
    ax2.text(0.5, 0.5, "TM 正对面", ha='center', va='center', fontsize=9, color='white', fontweight='bold')
    ax2.text(0.5, 0.08, "Naf (与 TMO6 共面)\n正对 TM3+/4+，静电强排斥，高钠态才被逼占满", ha='center', va='center', fontsize=10)
    ax2.set_xlim(0, 1); ax2.set_ylim(0, 1); ax2.axis('off')

    fig.suptitle("P2 相中两种特征钠位点: Nae vs Naf", fontsize=12, fontweight='bold')
    save_fig(fig, '06_p2_na_sites.png')

# ==========================================
# 07. 扩散能垒对比曲线
# ==========================================
def draw_07_diffusion():
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    x = np.linspace(0, 1, 100)
    # O3 路径 (能垒约 0.45 eV，有双峰/四面体中间态)
    e_o3 = 0.48 * np.sin(np.pi * x)**2 + 0.12 * np.sin(2 * np.pi * x)**2
    # P2 路径 (平滑单峰，能垒约 0.22 eV)
    e_p2 = 0.22 * np.sin(np.pi * x)**2

    ax.plot(x, e_o3, color=C_O3, lw=2.5, label='O3 扩散路径 (Oct-Tet-Oct): 能垒 ~0.45 eV')
    ax.plot(x, e_p2, color=C_P2, lw=2.5, linestyle='--', label='P2 扩散路径 (Nae-Naf-Nae): 能垒 ~0.22 eV')
    ax.fill_between(x, e_o3, alpha=0.15, color=C_O3)
    ax.fill_between(x, e_p2, alpha=0.15, color=C_P2)

    ax.set_title("O3 与 P2 钠离子迁移能垒对比 (DFT 典型势能面)", fontsize=11, fontweight='bold')
    ax.set_xlabel("反应坐标 (Diffusion Coordinate)")
    ax.set_ylabel("相对能量势垒 (Energy Barrier / eV)")
    ax.legend(frameon=True, facecolor='#ffffff')
    save_fig(fig, '07_diffusion.png')

# ==========================================
# 08. 充电相变路径
# ==========================================
def draw_08_phase_transition():
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.axis('off')
    
    # O3 相变链
    ax.text(0.1, 0.75, "O3 家族相变路径:", fontsize=11, fontweight='bold', color=C_O3)
    steps_o3 = ["O3\n(初始纯相)", "P3\n(层滑移)", "O1 / OP4\n(深度去钠相变)"]
    for i, st in enumerate(steps_o3):
        ax.add_patch(Rectangle((0.15 + i*0.28, 0.65), 0.20, 0.18, facecolor='#e8f4fd', edgecolor=C_O3, lw=1.5))
        ax.text(0.25 + i*0.28, 0.74, st, ha='center', va='center', fontsize=9.5, fontweight='bold')
        if i < 2:
            ax.annotate("", xy=(0.38 + i*0.28, 0.74), xytext=(0.35 + i*0.28, 0.74), arrowprops=dict(arrowstyle="->", lw=2, color=C_O3))

    # P2 相变链
    ax.text(0.1, 0.35, "P2 家族相变路径:", fontsize=11, fontweight='bold', color=C_P2)
    steps_p2 = ["P2\n(结构稳定)", "P2 (局部畸变)\n(宽泛单相区)", "O2 / OP4\n(高电位滑移)"]
    for i, st in enumerate(steps_p2):
        ax.add_patch(Rectangle((0.15 + i*0.28, 0.25), 0.20, 0.18, facecolor='#eafaf1', edgecolor=C_P2, lw=1.5))
        ax.text(0.25 + i*0.28, 0.34, st, ha='center', va='center', fontsize=9.5, fontweight='bold')
        if i < 2:
            ax.annotate("", xy=(0.38 + i*0.28, 0.34), xytext=(0.35 + i*0.28, 0.34), arrowprops=dict(arrowstyle="->", lw=2, color=C_P2))

    fig.suptitle("充放电过程中的晶体相变退化路径 (去钠态剪切与相变开裂)", fontsize=12, fontweight='bold')
    save_fig(fig, '08_phase_transition.png')

# ==========================================
# 09. O3 与 P2 综合对照图表
# ==========================================
def draw_09_compare():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    metrics = ['初始钠含量', '理论比容量', '离子电导率', '倍率性能', '空穴稳定性', '抗相变开裂']
    o3_scores = [95, 90, 60, 65, 55, 60]
    p2_scores = [65, 70, 95, 90, 85, 80]

    x = np.arange(len(metrics))
    width = 0.35
    ax.bar(x - width/2, o3_scores, width, label='O3 型层状正极', color=C_O3, alpha=0.85)
    ax.bar(x + width/2, p2_scores, width, label='P2 型层状正极', color=C_P2, alpha=0.85)

    ax.set_ylabel('综合性能评分 (Score / 100)')
    ax.set_title('O3 型与 P2 型电化学核心性能雷达成像直方图', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=10, fontweight='bold')
    ax.set_ylim(0, 110)
    ax.legend(frameon=True, facecolor='#ffffff')
    save_fig(fig, '09_compare.png')

# ==========================================
# 10. NaxTMO2 层状骨架示意
# ==========================================
def draw_10_formula():
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.axis('off')
    ax.text(0.5, 0.85, r"$\mathrm{Na}_x\mathrm{TM}\mathrm{O}_2$ 核心化学式与晶体层状解构", ha='center', va='center', fontsize=14, fontweight='bold', color=C_INK)
    
    # 结构分解三块
    boxes = [
        (0.08, r"$\mathrm{Na}_x$", "层间钠离子\n(工作工质，充放电进出脱嵌)", C_NA),
        (0.38, r"$\mathrm{TM}$", "过渡金属 (Ni/Fe/Mn/Cu)\n(氧化还原活性中心，提供电容)", C_TM),
        (0.68, r"$\mathrm{O}_2$", "阴离子氧骨架\n(构建八面体/三棱柱骨架配位)", C_O)
    ]
    for x0, title, desc, col in boxes:
        ax.add_patch(Rectangle((x0, 0.25), 0.24, 0.45, facecolor='#f8f9fa', edgecolor=col, lw=2))
        ax.text(x0 + 0.12, 0.58, title, ha='center', va='center', fontsize=16, fontweight='bold', color=col)
        ax.text(x0 + 0.12, 0.40, desc, ha='center', va='center', fontsize=9.5, color='#444444')

    save_fig(fig, '10_formula.png')

# ==========================================
# 11. O3 与 P2 三维点阵对比
# ==========================================
def draw_11_3d_layers():
    fig = plt.figure(figsize=(9, 4.5))
    ax1 = fig.add_subplot(121, projection='3d')
    # O3
    xs, ys = np.meshgrid(np.linspace(0, 2, 3), np.linspace(0, 2, 3))
    for z, col, label in [(0, C_O, 'O'), (0.5, C_TM, 'TM'), (1.0, C_O, 'O'), (1.5, C_NA, 'Na')]:
        ax1.scatter(xs, ys, np.full_like(xs, z), color=col, s=60, alpha=0.8)
    ax1.set_title("O3 三维晶格交替点阵", fontsize=11, fontweight='bold')
    ax1.set_axis_off()

    # P2
    ax2 = fig.add_subplot(122, projection='3d')
    for z, col, label in [(0, C_O, 'O'), (0.5, C_TM, 'TM'), (1.0, C_O, 'O'), (1.7, C_NA, 'Na')]:
        ax2.scatter(xs, ys, np.full_like(xs, z), color=col, s=60, alpha=0.8)
    ax2.set_title("P2 三维晶格交替点阵", fontsize=11, fontweight='bold')
    ax2.set_axis_off()

    save_fig(fig, '11_3d_layers.png')

# ==========================================
# 12. 钠电层状正极速记海报
# ==========================================
def draw_12_poster():
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.axis('off')
    ax.add_patch(Rectangle((0.02, 0.02), 0.96, 0.96, facecolor='#fffaf3', edgecolor=C_ACCENT, lw=2.5))
    ax.text(0.5, 0.88, "钠离子电池层状正极 (Delmas 体系速查表)", ha='center', va='center', fontsize=14, fontweight='bold', color=C_O3)
    
    text = (
        "【字母看配位】\n"
        " • O 型: 钠处于八面体中 (ABC 堆积，能垒较高，高钠容量大)\n"
        " • P 型: 钠处于三棱柱中 (ABBA 堆积，开放通道，快充倍率好)\n\n"
        "【数字看周期】\n"
        " • 2 = 穿过 2 层 TMO2 晶胞闭合； 3 = 穿过 3 层 TMO2 晶胞闭合\n\n"
        "【设计共识】\n"
        " • O3: 高能量密度首选 (如 NaNi1/3Fe1/3Mn1/3O2)；\n"
        " • P2: 高倍率长循环首选 (如 Na2/3Fe1/2Mn1/2O2)。"
    )
    ax.text(0.10, 0.45, text, ha='left', va='center', fontsize=10.5, color='#2c3848', linespacing=1.6)
    save_fig(fig, '12_poster.png')

# ==========================================
# 20. 氧层 A B C 三个横向落点
# ==========================================
def draw_20_abc_sites():
    fig, ax = plt.subplots(figsize=(6.5, 5))
    # 俯视密堆积 A, B, C 位置
    ax.scatter([0, 1, 0.5], [0, 0, np.sqrt(3)/2], color='#e74c3c', s=200, label='A 氧位点', zorder=5)
    ax.scatter([0.5, 1.5, 1.0], [np.sqrt(3)/6, np.sqrt(3)/6, 2*np.sqrt(3)/3], color='#3498db', s=200, label='B 氧位点', zorder=5)
    ax.scatter([0.5, 1.0, 1.5], [-np.sqrt(3)/6, np.sqrt(3)/3, np.sqrt(3)/3], color='#2ecc71', s=200, label='C 氧位点', zorder=5)

    ax.set_title("密排六方氧层中 A、B、C 三个不同二维落点", fontsize=11, fontweight='bold')
    ax.set_xlim(-0.3, 1.8); ax.set_ylim(-0.5, 1.4)
    ax.set_aspect('equal')
    ax.legend(loc='lower center', ncol=3, frameon=True)
    ax.axis('off')
    save_fig(fig, '20_abc_sites.png')

# ==========================================
# 21, 22, 23, 24: 周期路径与闭合
# ==========================================
def draw_21_o3_three_steps():
    fig, ax = plt.subplots(figsize=(6, 4.5))
    # 三角形闭合 A -> B -> C -> A
    pts = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2], [0, 0]])
    ax.plot(pts[:,0], pts[:,1], color=C_O3, lw=2.5, marker='o', markersize=10)
    labels = ['A', 'B', 'C', 'A']
    for p, l in zip(pts[:-1], labels[:-1]):
        ax.text(p[0], p[1]-0.1, l, fontsize=12, fontweight='bold', ha='center', color=C_O3)
    ax.set_title("O3 的 ABC 三步闭合三角环 (需跨越 3 层 TMO2)", fontsize=11, fontweight='bold')
    ax.set_xlim(-0.3, 1.3); ax.set_ylim(-0.3, 1.1)
    ax.set_aspect('equal'); ax.axis('off')
    save_fig(fig, '21_o3_three_steps.png')

def draw_22_p2_two_steps():
    fig, ax = plt.subplots(figsize=(6, 3.5))
    ax.plot([0, 1], [0.5, 0.5], color=C_P2, lw=3, marker='s', markersize=12)
    ax.text(0, 0.35, "A 氧位", fontsize=11, fontweight='bold', ha='center', color=C_P2)
    ax.text(1, 0.35, "B 氧位", fontsize=11, fontweight='bold', ha='center', color=C_P2)
    ax.annotate("", xy=(0.8, 0.6), xytext=(0.2, 0.6), arrowprops=dict(arrowstyle="<->", lw=2.5, color=C_P2))
    ax.text(0.5, 0.72, "折返振荡闭合 (2 步即可复位)", fontsize=10.5, ha='center', color=C_P2)
    ax.set_xlim(-0.3, 1.3); ax.set_ylim(0, 1); ax.axis('off')
    ax.set_title("P2 在 A 与 B 之间两步闭合", fontsize=11, fontweight='bold')
    save_fig(fig, '22_p2_two_steps.png')

def draw_23_period_family():
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('off')
    fams = [
        ("P2", "AB BA", "棱柱配位 / 2层周期"),
        ("P3", "AB BC CA", "棱柱配位 / 3层周期"),
        ("O3", "AB BC CA", "八面体配位 / 3层周期"),
        ("O2", "AB AC", "八面体配位 / 2层周期 (去钠形成)")
    ]
    for i, (name, stack, desc) in enumerate(fams):
        ax.add_patch(Rectangle((0.05 + i*0.23, 0.2), 0.20, 0.6, facecolor='#f8f9fa', edgecolor=C_O3 if 'O' in name else C_P2, lw=2))
        ax.text(0.15 + i*0.23, 0.65, name, ha='center', va='center', fontsize=14, fontweight='bold', color=C_O3 if 'O' in name else C_P2)
        ax.text(0.15 + i*0.23, 0.50, stack, ha='center', va='center', fontsize=10, fontweight='bold')
        ax.text(0.15 + i*0.23, 0.32, desc, ha='center', va='center', fontsize=8.5, color=C_MUTED)
    fig.suptitle("Delmas 周期家族: P2, P3, O3, O2 构型谱系", fontsize=12, fontweight='bold')
    save_fig(fig, '23_period_family.png')

def draw_24_cannot_close():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
    ax1.plot([0, 1, 0.5], [0, 0, 0.8], 'o--', color=C_O3, markersize=8)
    ax1.text(0.5, 0.9, "缺 C->A 边 (2步无法闭合)", color=C_O3, ha='center', fontsize=9.5, fontweight='bold')
    ax1.set_title("八面体 O 型: 2 步无法复位", fontsize=10.5, fontweight='bold')
    ax1.axis('off')

    ax2.plot([0, 1], [0.4, 0.4], 's-', color=C_P2, markersize=10)
    ax2.text(0.5, 0.6, "A-B 折返刚好闭合", color=C_P2, ha='center', fontsize=9.5, fontweight='bold')
    ax2.set_title("三棱柱 P 型: 2 步完美闭合", fontsize=10.5, fontweight='bold')
    ax2.axis('off')
    save_fig(fig, '24_cannot_close.png')

# ==========================================
# 25. ML6 八面体配位 (CFT 基础)
# ==========================================
def draw_25_ml6_octahedron():
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(111, projection='3d')
    # 坐标轴中心 M
    ax.scatter([0], [0], [0], color=C_TM, s=200, label='M (过渡金属离子)')
    # 6 个 L (配体氧)
    coords = np.array([[1.2, 0, 0], [-1.2, 0, 0], [0, 1.2, 0], [0, -1.2, 0], [0, 0, 1.2], [0, 0, -1.2]])
    ax.scatter(coords[:,0], coords[:,1], coords[:,2], color=C_O, s=140, label=r'L ($\mathrm{O^{2-}}$ 配体)')
    
    # 连线
    for c in coords:
        ax.plot([0, c[0]], [0, c[1]], [0, c[2]], color='#888888', lw=1.5, linestyle=':')

    ax.set_title(r"$\mathrm{ML_6}$ 正八面体配位环境与坐标轴取向 ($O_h$ 点群)", fontsize=11, fontweight='bold')
    ax.set_axis_off()
    ax.legend(loc='lower center', frameon=False)
    save_fig(fig, '25_ml6_octahedron.png')

# ==========================================
# 26. 五条 d 轨道空间形状
# ==========================================
def draw_26_d_orbitals():
    fig, axes = plt.subplots(1, 5, figsize=(11, 3))
    orbitals = [
        (r'$d_{z^2}$', C_O3, 'eg (迎头)'),
        (r'$d_{x^2-y^2}$', C_O3, 'eg (迎头)'),
        (r'$d_{xy}$', C_P2, 't2g (夹缝)'),
        (r'$d_{yz}$', C_P2, 't2g (夹缝)'),
        (r'$d_{xz}$', C_P2, 't2g (夹缝)')
    ]
    t = np.linspace(0, 2*np.pi, 200)
    for ax, (name, col, group) in zip(axes, orbitals):
        # 极坐标画四叶草形状示意
        r = np.abs(np.sin(2*t))
        ax.plot(r*np.cos(t), r*np.sin(t), color=col, lw=2)
        ax.fill(r*np.cos(t), r*np.sin(t), color=col, alpha=0.3)
        ax.set_title(f"{name}\n{group}", fontsize=10, fontweight='bold')
        ax.axis('off'); ax.set_aspect('equal')
    fig.suptitle("五条 3d 轨道几何取向: eg (轴向对准) vs t2g (轴间夹缝)", fontsize=11, fontweight='bold')
    save_fig(fig, '26_d_orbitals.png')

# ==========================================
# 27. dx2-y2 正对氧 vs dxy 躲进夹缝
# ==========================================
def draw_27_pointing():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
    
    # 左: dx2-y2 迎头撞击
    ax1.plot([-1.5, 1.5], [0, 0], 'k:', lw=1)
    ax1.plot([0, 0], [-1.5, 1.5], 'k:', lw=1)
    for pos in [(1.2, 0), (-1.2, 0), (0, 1.2), (0, -1.2)]:
        ax1.add_patch(Circle(pos, 0.22, color=C_O, zorder=5))
    ax1.text(0, 0, r'$d_{x^2-y^2}$' + '\n迎头强排斥', ha='center', va='center', fontsize=9.5, fontweight='bold', color=C_O3)
    ax1.set_title(r'$e_g$ 轨道: 四叶瓣直冲氧原子 (能量骤升)', fontsize=10.5, fontweight='bold')
    ax1.set_xlim(-1.8, 1.8); ax1.set_ylim(-1.8, 1.8); ax1.axis('off')

    # 右: dxy 钻进夹缝
    ax2.plot([-1.5, 1.5], [0, 0], 'k:', lw=1)
    ax2.plot([0, 0], [-1.5, 1.5], 'k:', lw=1)
    for pos in [(1.2, 0), (-1.2, 0), (0, 1.2), (0, -1.2)]:
        ax2.add_patch(Circle(pos, 0.22, color=C_O, zorder=5))
    ax2.text(0, 0, r'$d_{xy}$' + '\n躲进夹缝', ha='center', va='center', fontsize=9.5, fontweight='bold', color=C_P2)
    ax2.set_title(r'$t_{2g}$ 轨道: 四叶瓣转 45° 避开氧 (能量下降)', fontsize=10.5, fontweight='bold')
    ax2.set_xlim(-1.8, 1.8); ax2.set_ylim(-1.8, 1.8); ax2.axis('off')

    save_fig(fig, '27_pointing.png')

# ==========================================
# 28. 八面体晶体场轨道分裂图 (10 Dq)
# ==========================================
def draw_28_octahedral_split():
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.axis('off')
    
    # 自由离子 5条简并
    ax.plot([0.1, 0.3], [0, 0], 'k-', lw=3)
    ax.text(0.2, -0.2, "自由离子 5d 简并", ha='center', fontsize=10)

    # 八面体劈裂
    # eg 上升 +0.6 Delta
    ax.plot([0.65, 0.85], [0.6, 0.6], color=C_O3, lw=3)
    ax.text(0.75, 0.72, r'$e_g\ (d_{z^2}, d_{x^2-y^2}) \ [+0.6\Delta_o]$', ha='center', fontsize=10.5, fontweight='bold', color=C_O3)

    # t2g 下降 -0.4 Delta
    ax.plot([0.65, 0.85], [-0.4, -0.4], color=C_P2, lw=3)
    ax.text(0.75, -0.55, r'$t_{2g}\ (d_{xy}, d_{yz}, d_{xz}) \ [-0.4\Delta_o]$', ha='center', fontsize=10.5, fontweight='bold', color=C_P2)

    # 虚线能级连线与能隙箭头
    ax.plot([0.3, 0.65], [0, 0.6], 'k:', alpha=0.5)
    ax.plot([0.3, 0.65], [0, -0.4], 'k:', alpha=0.5)
    ax.annotate("", xy=(0.9, 0.6), xytext=(0.9, -0.4), arrowprops=dict(arrowstyle="<->", lw=2, color=C_ACCENT))
    ax.text(0.93, 0.1, r"$\Delta_o = 10Dq$", fontsize=11, fontweight='bold', color=C_ACCENT, va='center')

    ax.set_xlim(0, 1.1); ax.set_ylim(-0.8, 1.0)
    fig.suptitle(r"正八面体晶体场中的 $d$ 轨道能级劈裂与重心守恒规则", fontsize=12, fontweight='bold')
    save_fig(fig, '28_octahedral_split.png')

# ==========================================
# 29. 高自旋与低自旋电子排布 (HS vs LS)
# ==========================================
def draw_29_hs_ls():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4))
    
    # HS (高自旋 d4, 如 Mn3+)
    ax1.plot([0.2, 0.8], [1, 1], color=C_O3, lw=2.5, label='eg')
    ax1.plot([0.2, 0.8], [0, 0], color=C_P2, lw=2.5, label='t2g')
    ax1.arrow(0.4, 0.8, 0, 0.3, head_width=0.08, color='black', lw=2) # 1 in eg
    ax1.arrow(0.3, -0.2, 0, 0.3, head_width=0.08, color='black', lw=2)
    ax1.arrow(0.5, -0.2, 0, 0.3, head_width=0.08, color='black', lw=2)
    ax1.arrow(0.7, -0.2, 0, 0.3, head_width=0.08, color='black', lw=2)
    ax1.set_title(r"高自旋 HS $d^4$ ($\mathrm{Mn^{3+}}$)" + "\n" + r"$t_{2g}^3 e_g^1$ (具有强 JT 畸变活性)", fontsize=10.5, fontweight='bold')
    ax1.set_ylim(-0.5, 1.5); ax1.axis('off')

    # LS (低自旋 d4)
    ax2.plot([0.2, 0.8], [1, 1], color=C_O3, lw=2.5)
    ax2.plot([0.2, 0.8], [0, 0], color=C_P2, lw=2.5)
    ax2.arrow(0.35, -0.2, 0, 0.3, head_width=0.06, color='black', lw=2)
    ax2.arrow(0.40, 0.1, 0, -0.3, head_width=0.06, color='black', lw=2) # paired
    ax2.arrow(0.6, -0.2, 0, 0.3, head_width=0.06, color='black', lw=2)
    ax2.arrow(0.75, -0.2, 0, 0.3, head_width=0.06, color='black', lw=2)
    ax2.set_title(r"低自旋 LS $d^4$ (强场配体)" + "\n" + r"$t_{2g}^4 e_g^0$ (无 JT 畸变驱动力)", fontsize=10.5, fontweight='bold')
    ax2.set_ylim(-0.5, 1.5); ax2.axis('off')

    save_fig(fig, '29_hs_ls.png')

# ==========================================
# 13, 14, 15: 姜-泰勒畸变起源与离子表
# ==========================================
def draw_13_jt_origin():
    fig, ax = plt.subplots(figsize=(7.5, 4))
    ax.axis('off')
    # 简并 eg
    ax.plot([0.1, 0.35], [0.5, 0.5], color=C_O3, lw=3)
    ax.text(0.22, 0.65, "简并 eg (1个电子)", ha='center', fontsize=10, fontweight='bold')
    # z轴拉长后，dz2 下降，dx2-y2 上升
    ax.plot([0.65, 0.9], [0.8, 0.8], color='#c0392b', lw=2.5)
    ax.text(0.77, 0.9, r'$d_{x^2-y^2}$ (空)', ha='center', fontsize=9.5)
    ax.plot([0.65, 0.9], [0.2, 0.2], color='#27ae60', lw=2.5)
    ax.text(0.77, 0.05, r'$d_{z^2}$ (占据单电子, 体系能量下降)', ha='center', fontsize=9.5, fontweight='bold')
    ax.arrow(0.77, 0.1, 0, 0.2, head_width=0.04, color='black', lw=2)

    ax.plot([0.35, 0.65], [0.5, 0.8], 'k:', alpha=0.5)
    ax.plot([0.35, 0.65], [0.5, 0.2], 'k:', alpha=0.5)
    fig.suptitle("姜-泰勒畸变热力学起源: 解除 eg 简并，体系总能量降低", fontsize=11, fontweight='bold')
    save_fig(fig, '13_jt_origin.png')

def draw_14_jt_octahedra():
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(9, 3.8))
    # 1. 规则
    ax1.add_patch(Rectangle((0.2, 0.2), 0.6, 0.6, facecolor='#f0f4f8', ec=C_O3, lw=2))
    ax1.set_title("规则正八面体\n(Oh, 6 键等长)", fontsize=10, fontweight='bold'); ax1.axis('off')
    # 2. z轴拉长
    ax2.add_patch(Rectangle((0.25, 0.05), 0.5, 0.9, facecolor='#fdf2e9', ec='#d35400', lw=2))
    ax2.set_title("轴向拉长 (Elongated)\n(最常见, Mn3+/Fe4+)", fontsize=10, fontweight='bold'); ax2.axis('off')
    # 3. z轴压缩
    ax3.add_patch(Rectangle((0.1, 0.25), 0.8, 0.5, facecolor='#f4f6f7', ec='#7f8c8d', lw=2))
    ax3.set_title("轴向压缩 (Compressed)\n(较少见)", fontsize=10, fontweight='bold'); ax3.axis('off')
    save_fig(fig, '14_jt_octahedra.png')

def draw_15_jt_ions():
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('off')
    ions = [
        ("Mn3+", "高自旋 d4", "t2g3 eg1", "★★★★★ 极强 (出生自带)"),
        ("Fe4+", "高自旋 d4", "t2g3 eg1", "★★★★★ 极强 (高压充电现身)"),
        ("Ni3+", "低自旋 d7", "t2g6 eg1", "★★★★☆ 较强 (脱钠相变)"),
        ("Mn4+", "d3", "t2g3 eg0", "☆☆☆☆☆ 无 (稳定六方)")
    ]
    ax.add_patch(Rectangle((0.05, 0.1), 0.9, 0.8, facecolor='#ffffff', ec='#cccccc', lw=1.5))
    ax.text(0.5, 0.82, "钠电过渡金属离子姜-泰勒 (JT) 活性对照表", ha='center', fontsize=12, fontweight='bold', color=C_INK)
    for i, (ion, d_state, conf, act) in enumerate(ions):
        y = 0.65 - i*0.14
        ax.text(0.12, y, ion, fontsize=11, fontweight='bold', color=C_O3)
        ax.text(0.28, y, d_state, fontsize=10)
        ax.text(0.48, y, conf, fontsize=10, fontweight='bold')
        ax.text(0.72, y, act, fontsize=10, color=C_O if '★' in act[:3] else C_P2)
    save_fig(fig, '15_jt_ions.png')

# ==========================================
# 16, 17, 18, 19: 姜-泰勒充放电、协同与掺杂抑制
# ==========================================
def draw_16_fe4_cycle():
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    v = np.linspace(2.0, 4.2, 100)
    # Fe4+ 浓度随充放电电压升高而骤增
    fe4_frac = 1 / (1 + np.exp(-10 * (v - 3.5)))
    ax.plot(v, fe4_frac * 100, color=C_O, lw=2.8, label=r'$\mathrm{Fe^{4+}}$ 比例 (JT 危险区)')
    ax.axvspan(3.6, 4.2, color='#f8d7da', alpha=0.4, label='高电压强 JT 晶格畸变失稳区')
    ax.set_xlabel("充电截止电压 / V (vs. Na/Na+)")
    ax.set_ylabel(r"$\mathrm{Fe^{4+}}$ 积累占比 (%)")
    ax.set_title(r"充电高电位诱发 $\mathrm{Fe^{3+} \to Fe^{4+}}$ 姜-泰勒突变", fontsize=11, fontweight='bold')
    ax.legend(loc='upper left', frameon=True, facecolor='#ffffff')
    save_fig(fig, '16_fe4_cycle.png')

def draw_17_cooperative():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 4))
    # 左: 协同畸变长程锁死
    ax1.plot([0, 1, 2], [0, 0.5, 1], 'ro-', lw=2)
    ax1.plot([0, 1, 2], [1, 1.5, 2], 'ro-', lw=2)
    ax1.text(1, -0.4, "协同长程锁死 (六方转单斜，开裂)", ha='center', color=C_O, fontsize=10, fontweight='bold')
    ax1.set_xlim(-0.5, 2.5); ax1.set_ylim(-0.8, 2.5); ax1.axis('off')

    # 右: 掺杂打断协同链
    ax2.plot([0, 0.8], [0, 0.2], 'bo-', lw=2)
    ax2.scatter([1], [0.8], color=C_TM, s=150, zorder=5, label='Ti/Mg 掺杂钉扎')
    ax2.plot([1.2, 2], [1.2, 1.4], 'bo-', lw=2)
    ax2.text(1, -0.4, "掺杂打断协同链 (宏观保持六方稳定)", ha='center', color=C_P2, fontsize=10, fontweight='bold')
    ax2.set_xlim(-0.5, 2.5); ax2.set_ylim(-0.8, 2.5); ax2.axis('off')
    fig.suptitle("微观局域畸变 vs 宏观协同姜-泰勒晶格应变剪切", fontsize=11, fontweight='bold')
    save_fig(fig, '17_cooperative.png')

def draw_18_doping():
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    ax.axis('off')
    paths = [
        "1. 浓度稀释: 压低 Mn3+/Fe4+ 密度至协同阈值以下",
        "2. 价态钉扎: 掺低价 Mg2+/Li+ 迫使锰保持非畸变 Mn4+",
        "3. 强键钉氧: Ti-O/Al-O 强共价键死死拉紧氧骨架",
        "4. 半径失配: 破坏长程应力波对齐，阻止宏观相变",
        "5. 电荷无序: 多元混排产生势能涨落，打碎电荷有序",
        "6. 堵截迁移: 抑制高价过渡金属向四面体间隙不可逆跑位"
    ]
    ax.add_patch(Rectangle((0.05, 0.05), 0.9, 0.9, facecolor='#f7fbf8', ec=C_P2, lw=2))
    ax.text(0.5, 0.88, "元素掺杂与体相工程抑制姜-泰勒畸变的 6 大前沿范式", ha='center', fontsize=12, fontweight='bold', color=C_P2)
    for i, p in enumerate(paths):
        ax.text(0.12, 0.74 - i*0.11, p, fontsize=10, color='#2c3848')
    save_fig(fig, '18_doping.png')

def draw_19_jt_poster():
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    ax.axis('off')
    ax.add_patch(Rectangle((0.04, 0.04), 0.92, 0.92, facecolor='#fffaf3', ec=C_ACCENT, lw=2.5))
    ax.text(0.5, 0.85, "姜-泰勒 (Jahn-Teller) 效应极简速记海报", ha='center', fontsize=13, fontweight='bold', color=C_O3)
    content = (
        "• 开关条件: eg 轨道只要有单电子 (eg1) 或单空穴 (eg3)，八面体必变形！\n"
        "• 致命元凶: 锰(Mn3+)出生自带畸变，铁(Fe4+)充电高压突现！\n"
        "• 破坏机制: 局部变形不可怕，整层‘协同咬合’撕裂晶格最致命！\n"
        "• 破解绝招: 掺 Ti/Mg/Li 强共价钉扎、电中性提价、剪断协同链！"
    )
    ax.text(0.12, 0.45, content, ha='left', va='center', fontsize=10.5, linespacing=1.8, color='#1c2430')
    save_fig(fig, '19_jt_poster.png')

# ==========================================
# 主执行入口
# ==========================================
def main():
    print("[*] 正在执行全套 29 张钠电与晶体场学术机理图表生成...")
    draw_01_polyhedra()
    draw_02_hop_windows()
    draw_05_delmas()
    draw_03_o3_stacking()
    draw_04_p2_stacking()
    draw_06_p2_na_sites()
    draw_07_diffusion()
    draw_08_phase_transition()
    draw_09_compare()
    draw_10_formula()
    draw_11_3d_layers()
    draw_12_poster()
    draw_20_abc_sites()
    draw_21_o3_three_steps()
    draw_22_p2_two_steps()
    draw_23_period_family()
    draw_24_cannot_close()
    draw_25_ml6_octahedron()
    draw_26_d_orbitals()
    draw_27_pointing()
    draw_28_octahedral_split()
    draw_29_hs_ls()
    draw_13_jt_origin()
    draw_14_jt_octahedra()
    draw_15_jt_ions()
    draw_16_fe4_cycle()
    draw_17_cooperative()
    draw_18_doping()
    draw_19_jt_poster()
    print("[SUCCESS] 29 张高清学术机理插图已全部绘制完成！")

if __name__ == '__main__':
    main()
