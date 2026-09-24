# -*- coding: utf-8 -*-
"""
scripts/draw_sib_structures.py
为钠电正极结构学与晶体场理论交互指南生成全套 29 张高精度学术机理插图
支持: NVIDIA Tesla V100 CUDA 硬件加速张量与球面谐波计算
中文支持: 完美注册 Microsoft YaHei，杜绝方块乱码
"""

import os
import sys

# 强制标准输出为 UTF-8 编码
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

import numpy as np
import torch
import matplotlib as mpl
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle, Rectangle, FancyArrowPatch, Wedge
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# 1. 注册中文字体并设置学术绘图参数
font_paths = ['C:/Windows/Fonts/msyh.ttc', 'C:/Windows/Fonts/simhei.ttf']
for fp in font_paths:
    if os.path.exists(fp):
        fm.fontManager.addfont(fp)

mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial']
mpl.rcParams['axes.unicode_minus'] = False
mpl.rcParams['figure.autolayout'] = False
mpl.rcParams['savefig.dpi'] = 220
mpl.rcParams['savefig.bbox'] = 'tight'

# 2. 检测并激活 Tesla V100 CUDA 加速
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
if device.type == 'cuda':
    gpu_name = torch.cuda.get_device_name(0)
    print(f"[CUDA INIT] 成功调用 GPU 加速: {gpu_name} (Volta sm_70)")
else:
    print("[WARN] 未检测到 CUDA，降级为 CPU 模式")

# 3. 统一学术配色规范
C_O3 = '#1d4e89'     # O3 经典深蓝
C_P2 = '#2d6a4f'     # P2 森林墨绿
C_NA = '#e69f00'     # 钠离子金黄
C_TM = '#00a087'     # 过渡金属青绿
C_O = '#e74c3c'      # 氧原子砖红
C_ACCENT = '#d35400' # 警示高亮橙
C_BG = '#ffffff'     # 纯白底色
C_MUTED = '#5c6570'  # 辅助灰色
C_INK = '#1c2430'    # 文本深墨色
C_GOLD = '#f39c12'   # 轨道正相位金
C_COBALT = '#2980b9' # 轨道负相位蓝

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'images'))
PICTURES_DIR = os.path.abspath(os.path.expanduser('~/Pictures'))
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(PICTURES_DIR, exist_ok=True)

def save_fig(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, facecolor=C_BG, edgecolor='none')
    # 自动同步保存至 Pictures 目录
    try:
        import shutil
        shutil.copy2(path, os.path.join(PICTURES_DIR, name))
    except Exception as e:
        pass
    plt.close(fig)
    print(f"[OK] Generated: {name}")

# ==========================================
# 01. 两种笼子: 八面体 vs 三棱柱
# ==========================================
def draw_01_polyhedra():
    fig = plt.figure(figsize=(9.5, 4.8))
    
    # 左: 八面体 (Octahedron, O3)
    ax1 = fig.add_subplot(121, projection='3d')
    d_oct = 1.15
    verts_oct = [
        [d_oct, 0, 0], [-d_oct, 0, 0], [0, d_oct, 0], [0, -d_oct, 0], [0, 0, d_oct], [0, 0, -d_oct]
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
    poly1 = Poly3DCollection(faces_oct, alpha=0.35, facecolor=C_O3, edgecolor=C_O3, linewidths=1.5)
    ax1.add_collection3d(poly1)
    
    # 氧原子与配位键
    for v in verts_oct:
        ax1.scatter([v[0]], [v[1]], [v[2]], color=C_O, s=90, edgecolors='black', zorder=5)
        ax1.plot([0, v[0]], [0, v[1]], [0, v[2]], color='#888888', lw=1.2, linestyle=':')
    # 中心 Na+
    ax1.scatter([0], [0], [0], color=C_NA, s=160, edgecolors='black', zorder=6, label=r'$\mathrm{Na^+}$ 位于八面体中心 (CN=6)')
    ax1.set_title('八面体配位 (Octahedron)\nO3 型结构 (氧呈 ABCABC 密堆积)', fontsize=11, fontweight='bold', pad=8)
    ax1.set_axis_off()
    ax1.set_xlim([-1.3, 1.3]); ax1.set_ylim([-1.3, 1.3]); ax1.set_zlim([-1.3, 1.3])
    ax1.view_init(elev=22, azim=45)
    ax1.legend(loc='lower center', frameon=False, fontsize=9.5)

    # 右: 三棱柱 (Prism, P2)
    ax2 = fig.add_subplot(122, projection='3d')
    r, h = 1.05, 0.95
    angles = np.array([0, 2*np.pi/3, 4*np.pi/3]) + np.pi/6
    top = np.column_stack([r*np.cos(angles), r*np.sin(angles), np.full(3, h)])
    bot = np.column_stack([r*np.cos(angles), r*np.sin(angles), np.full(3, -h)])
    faces_prism = [
        [top[0], top[1], top[2]], # 顶面
        [bot[0], bot[1], bot[2]], # 底面
        [top[0], top[1], bot[1], bot[0]],
        [top[1], top[2], bot[2], bot[1]],
        [top[2], top[0], bot[0], bot[2]],
    ]
    poly2 = Poly3DCollection(faces_prism, alpha=0.35, facecolor=C_P2, edgecolor=C_P2, linewidths=1.5)
    ax2.add_collection3d(poly2)
    
    # 氧原子与配位键
    for v in np.vstack([top, bot]):
        ax2.scatter([v[0]], [v[1]], [v[2]], color=C_O, s=90, edgecolors='black', zorder=5)
        ax2.plot([0, v[0]], [0, v[1]], [0, v[2]], color='#888888', lw=1.2, linestyle=':')
    ax2.scatter([0], [0], [0], color=C_NA, s=160, edgecolors='black', zorder=6, label=r'$\mathrm{Na^+}$ 位于三棱柱中心 (CN=6)')
    ax2.set_title('三棱柱配位 (Prism)\nP2 型结构 (氧呈 ABBA 堆叠)', fontsize=11, fontweight='bold', pad=8)
    ax2.set_axis_off()
    ax2.set_xlim([-1.3, 1.3]); ax2.set_ylim([-1.3, 1.3]); ax2.set_zlim([-1.3, 1.3])
    ax2.view_init(elev=22, azim=45)
    ax2.legend(loc='lower center', frameon=False, fontsize=9.5)

    save_fig(fig, '01_polyhedra.png')

# ==========================================
# 02. 跳跃窗口: 三角形面 vs 矩形侧面
# ==========================================
def draw_02_hop_windows():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 4.2))
    
    # 左: 八面体共享三角形面 (窄颈瓶)
    tri = np.array([[0, 1.4], [-1.2, -0.7], [1.2, -0.7]])
    p1 = Polygon(tri, closed=True, facecolor='#dbe4ee', edgecolor=C_O3, lw=2.5, alpha=0.85)
    ax1.add_patch(p1)
    for pt in tri:
        ax1.add_patch(Circle(pt, 0.28, facecolor=C_O, edgecolor='black', lw=1.5, zorder=5))
    ax1.add_patch(Circle((0, 0), 0.38, facecolor=C_NA, edgecolor='black', lw=2, linestyle='--', zorder=6))
    ax1.text(0, 0, r'$\mathrm{Na^+}$', ha='center', va='center', fontsize=12, fontweight='bold')
    ax1.text(0, -1.25, r"狭窄三角形面窗口 ($r_{\mathrm{bottleneck}} \approx 1.05$ Å)" + "\n" + "跨越能垒高 (~0.55 eV) | 易形成共面相变挤压", 
             ha='center', fontsize=9.5, color=C_INK)
    ax1.set_title("O3 型扩散通道: 面共享三角形瓶颈", fontsize=11, fontweight='bold', color=C_O3)
    ax1.set_xlim(-1.8, 1.8); ax1.set_ylim(-1.6, 1.8); ax1.axis('off'); ax1.set_aspect('equal')

    # 右: 三棱柱矩形侧面窗口 (开阔门)
    rect = np.array([[-0.9, -1.1], [0.9, -1.1], [0.9, 1.1], [-0.9, 1.1]])
    p2 = Polygon(rect, closed=True, facecolor='#d8ede2', edgecolor=C_P2, lw=2.5, alpha=0.85)
    ax2.add_patch(p2)
    for pt in rect:
        ax2.add_patch(Circle(pt, 0.28, facecolor=C_O, edgecolor='black', lw=1.5, zorder=5))
    ax2.add_patch(Circle((0, 0), 0.45, facecolor=C_NA, edgecolor='black', lw=2, zorder=6))
    ax2.text(0, 0, r'$\mathrm{Na^+}$', ha='center', va='center', fontsize=12, fontweight='bold')
    ax2.text(0, -1.55, r"开阔矩形侧面窗口 ($r_{\mathrm{bottleneck}} \approx 1.35$ Å)" + "\n" + "跨越能垒极低 (~0.25 eV) | 优异倍率动力学", 
             ha='center', fontsize=9.5, color=C_INK)
    ax2.set_title("P2 型扩散通道: 矩形宽敞通道", fontsize=11, fontweight='bold', color=C_P2)
    ax2.set_xlim(-1.8, 1.8); ax2.set_ylim(-1.8, 1.6); ax2.axis('off'); ax2.set_aspect('equal')

    save_fig(fig, '02_hop_windows.png')

# ==========================================
# 03. O3 堆叠侧视图
# ==========================================
def draw_03_o3_stacking():
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    layers = ['A (O)', 'B (TM)', 'C (O)', 'A (Na)', 'B (O)', 'C (TM)', 'A (O)', 'B (Na)', 'C (O)', 'A (TM)', 'B (O)', 'C (Na)']
    colors = [C_O, C_TM, C_O, C_NA, C_O, C_TM, C_O, C_NA, C_O, C_TM, C_O, C_NA]
    y_pos = np.linspace(0.1, 0.9, len(layers))
    
    for y, label, col in zip(y_pos, layers, colors):
        ax.plot([0.2, 0.8], [y, y], color=col, lw=3.5, solid_capstyle='round')
        ax.text(0.15, y, label, ha='right', va='center', fontsize=9, fontweight='bold', color=col)
    
    # 晶胞周期标注
    ax.annotate("", xy=(0.85, 0.1), xytext=(0.85, 0.9), arrowprops=dict(arrowstyle="<->", lw=2, color='#333333'))
    ax.text(0.88, 0.5, "1 个完整晶胞周期\n包含 3 个 TM 层 (周期 = 3)\nABCABC 氧密堆积", va='center', fontsize=9.5, color=C_INK)
    
    ax.set_xlim(0, 1.1); ax.set_ylim(0, 1.0); ax.axis('off')
    ax.set_title(r"$\mathrm{O3}$ 型层状氧化物侧视堆叠序列 ($R\bar{3}m$, 空间群 166)", fontsize=11.5, fontweight='bold', color=C_O3)
    save_fig(fig, '03_o3_stacking.png')

# ==========================================
# 04. P2 堆叠侧视图
# ==========================================
def draw_04_p2_stacking():
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    layers = ['A (O)', 'B (O)', 'A (TM)', 'B (O)', 'A (O)', 'B (TM)', 'A (O)', 'B (O)']
    colors = [C_O, C_O, C_TM, C_O, C_O, C_TM, C_O, C_O]
    y_pos = np.linspace(0.12, 0.88, len(layers))
    
    for y, label, col in zip(y_pos, layers, colors):
        ax.plot([0.2, 0.8], [y, y], color=col, lw=3.5, solid_capstyle='round')
        ax.text(0.15, y, label, ha='right', va='center', fontsize=9.5, fontweight='bold', color=col)
    
    # 钠层标注
    ax.text(0.5, (y_pos[1]+y_pos[2])/2, r"Na 棱柱层 ($\mathrm{Na_e / Na_f}$)", ha='center', va='center', color=C_NA, fontsize=9.5, fontweight='bold')
    ax.text(0.5, (y_pos[4]+y_pos[5])/2, r"Na 棱柱层 ($\mathrm{Na_e / Na_f}$)", ha='center', va='center', color=C_NA, fontsize=9.5, fontweight='bold')
    
    # 晶胞周期标注
    ax.annotate("", xy=(0.85, 0.12), xytext=(0.85, 0.88), arrowprops=dict(arrowstyle="<->", lw=2, color='#333333'))
    ax.text(0.88, 0.5, "1 个完整晶胞周期\n包含 2 个 TM 层 (周期 = 2)\nABBA 氧密堆积", va='center', fontsize=9.5, color=C_INK)
    
    ax.set_xlim(0, 1.1); ax.set_ylim(0, 1.0); ax.axis('off')
    ax.set_title(r"$\mathrm{P2}$ 型层状氧化物侧视堆叠序列 ($P6_3/mmc$, 空间群 194)", fontsize=11.5, fontweight='bold', color=C_P2)
    save_fig(fig, '04_p2_stacking.png')

# ==========================================
# 05. Delmas 命名法
# ==========================================
def draw_05_delmas():
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.axis('off')
    ax.add_patch(Rectangle((0.08, 0.1), 0.84, 0.8, facecolor='#f8f9fa', ec='#ced4da', lw=1.5))
    ax.text(0.5, 0.72, "Delmas 命名法则解析 (例: O3 vs P2)", ha='center', fontsize=12.5, fontweight='bold', color=C_INK)
    
    ax.text(0.15, 0.45, "首字母 (配位构型)\nO: Octahedral (八面体)\nP: Prismatic (三棱柱)", ha='left', va='center', fontsize=10, color=C_O3, fontweight='bold')
    ax.text(0.52, 0.45, "阿拉伯数字 (堆叠周期)\n3: 3个 TM 夹层为一周期\n2: 2个 TM 夹层为一周期", ha='left', va='center', fontsize=10, color=C_P2, fontweight='bold')
    ax.text(0.82, 0.45, "撇号 (畸变标注)\nO': 单斜姜-泰勒畸变\n(如 O'3-NaMnO2)", ha='center', va='center', fontsize=9.5, color=C_ACCENT, fontweight='bold')
    
    save_fig(fig, '05_delmas.png')

# ==========================================
# 06. P2 中 Nae 与 Naf 位
# ==========================================
def draw_06_p2_na_sites():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 4.2))
    
    # Nae 棱共享
    ax1.add_patch(Rectangle((-1, -1), 2, 2, facecolor='#e8f4f8', ec=C_O3, lw=2))
    ax1.plot([-1, 1], [-1, 1], 'k:', lw=1)
    ax1.plot([-1, 1], [1, -1], 'k:', lw=1)
    ax1.scatter([0], [0], color=C_NA, s=240, edgecolors='black', zorder=5)
    ax1.text(0, -0.4, r'$\mathrm{Na_e}$ (Edge-sharing)', ha='center', fontsize=10.5, fontweight='bold', color=C_O3)
    ax1.text(0, -1.35, "棱共享位 (离上下 TM 远)\n静电斥力小 | 能量稳定 | 占位率高 (~0.44)", ha='center', fontsize=9.5)
    ax1.set_xlim(-1.5, 1.5); ax1.set_ylim(-1.6, 1.5); ax1.axis('off'); ax1.set_aspect('equal')
    ax1.set_title(r"$\mathrm{Na_e}$ 位点几何环境", fontsize=11, fontweight='bold')

    # Naf 面共享
    ax2.add_patch(Rectangle((-1, -1), 2, 2, facecolor='#fef5e7', ec=C_ACCENT, lw=2))
    ax2.scatter([0], [0], color=C_TM, s=280, marker='s', edgecolors='black', label='TM 上下正对')
    ax2.scatter([0], [0], color=C_NA, s=180, edgecolors='black', zorder=5)
    ax2.text(0, -0.4, r'$\mathrm{Na_f}$ (Face-sharing)', ha='center', fontsize=10.5, fontweight='bold', color=C_ACCENT)
    ax2.text(0, -1.35, "面共享位 (与 TM 上下直视正对)\n强库仑斥力 | 能量较高 | 占位率低 (~0.23)", ha='center', fontsize=9.5)
    ax2.set_xlim(-1.5, 1.5); ax2.set_ylim(-1.6, 1.5); ax2.axis('off'); ax2.set_aspect('equal')
    ax2.set_title(r"$\mathrm{Na_f}$ 位点几何环境", fontsize=11, fontweight='bold')

    save_fig(fig, '06_p2_na_sites.png')

# ==========================================
# 07. 扩散能垒对比
# ==========================================
def draw_07_diffusion():
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    x = np.linspace(0, 10, 200)
    # O3 路径: 八面体 -> 四面体 -> 八面体
    y_o3 = 0.55 * (1 - np.cos(2*np.pi*x/10)) / 2
    # P2 路径: Nae -> 侧面矩形窗口 -> Naf
    y_p2 = 0.24 * (1 - np.cos(2*np.pi*x/10)) / 2

    ax.plot(x, y_o3, color=C_O3, lw=2.8, label=r'O3 路径: 八面体 $\rightarrow$ 狭窄四面体中间态 ($E_a \approx 0.55\ \mathrm{eV}$)')
    ax.plot(x, y_p2, color=C_P2, lw=2.8, label=r'P2 路径: $\mathrm{Na_e \rightarrow Na_f}$ 直接开阔跃迁 ($E_a \approx 0.24\ \mathrm{eV}$)')
    
    ax.set_ylabel("相对扩散能量势垒 (eV)", fontsize=10.5, fontweight='bold')
    ax.set_xlabel("离子迁移归一化反应坐标", fontsize=10.5, fontweight='bold')
    ax.set_title("O3 与 P2 结构钠离子层内扩散活化能垒对比", fontsize=11.5, fontweight='bold')
    ax.legend(frameon=True, fontsize=9.5, loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.4)
    save_fig(fig, '07_diffusion.png')

# ==========================================
# 08. 相变路径对比
# ==========================================
def draw_08_phase_transition():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.5, 4.8))
    
    # O3 相变链
    ax1.axis('off')
    ax1.text(0.05, 0.6, "O3 充放电相变路径\n(深脱钠滑移剧烈):", va='center', fontsize=10, fontweight='bold', color=C_O3)
    boxes_o3 = ["O3\n(初始)", "P3\n(低脱钠)", "O1 / OP4\n(深脱钠滑移)", "岩盐相 Rock-salt\n(阳离子迁移死区)"]
    cols_o3 = [C_O3, '#2980b9', C_ACCENT, '#c0392b']
    for i, (b, c) in enumerate(zip(boxes_o3, cols_o3)):
        ax1.add_patch(Rectangle((0.26 + i*0.18, 0.2), 0.15, 0.65, facecolor=c, alpha=0.85))
        ax1.text(0.26 + i*0.18 + 0.075, 0.52, b, ha='center', va='center', color='white', fontsize=9, fontweight='bold')
        if i < 3:
            ax1.annotate("", xy=(0.26 + (i+1)*0.18, 0.52), xytext=(0.26 + i*0.18 + 0.15, 0.52),
                         arrowprops=dict(arrowstyle="->", lw=2, color='#444444'))

    # P2 相变链
    ax2.axis('off')
    ax2.text(0.05, 0.6, "P2 充放电相变路径\n(骨架稳定性高):", va='center', fontsize=10, fontweight='bold', color=C_P2)
    boxes_p2 = ["P2\n(初始)", "P2 固溶体反应\n(宽电压平滑区)", "OP4 / O2\n(超高压罕见滑移)"]
    cols_p2 = [C_P2, '#27ae60', '#e67e22']
    for i, (b, c) in enumerate(zip(boxes_p2, cols_p2)):
        ax2.add_patch(Rectangle((0.26 + i*0.24, 0.2), 0.20, 0.65, facecolor=c, alpha=0.85))
        ax2.text(0.26 + i*0.24 + 0.10, 0.52, b, ha='center', va='center', color='white', fontsize=9, fontweight='bold')
        if i < 2:
            ax2.annotate("", xy=(0.26 + (i+1)*0.24, 0.52), xytext=(0.26 + i*0.24 + 0.20, 0.52),
                         arrowprops=dict(arrowstyle="->", lw=2, color='#444444'))

    fig.suptitle("钠电正极脱嵌钠热力学相变路径演化对比", fontsize=12, fontweight='bold')
    save_fig(fig, '08_phase_transition.png')

# ==========================================
# 09. 对照表
# ==========================================
def draw_09_compare():
    fig, ax = plt.subplots(figsize=(9, 4.2))
    ax.axis('off')
    headers = ["性能维度", "O3 型层状正极", "P2 型层状正极", "改性重点关注"]
    rows = [
        ["空间群与配位", "R-3m / 八面体 (CN=6)", "P6_3/mmc / 三棱柱 (CN=6)", "晶胞堆叠周期差异"],
        ["初始钠含量", "高 (x ≈ 1.0, 能量密度高)", "低 (x ≈ 0.67, 需补钠)", "全电池正负极匹配"],
        ["动力学倍率", "较差 (瓶颈窄, 能垒 ~0.55eV)", "极佳 (侧面开阔, ~0.24eV)", "快充与低温放电"],
        ["高压相变", "易突变为 P3/OP4/岩盐相", "单相固溶体范围宽", "阳离子迁移与微裂纹"],
        ["空气稳定性", "对水氧较敏感, 易生成碳酸盐", "相对稳定", "工业储存与加工性能"]
    ]
    table = ax.table(cellText=rows, colLabels=headers, loc='center', cellLoc='center',
                     colColours=['#f1f3f5', '#e8f4f8', '#e8f8f0', '#fcf3cf'])
    table.scale(1, 1.8)
    table.set_fontsize(9.5)
    ax.set_title("O3 型与 P2 型层状氧化物电化学及晶体学全维度对比", fontsize=11.5, fontweight='bold', pad=15)
    save_fig(fig, '09_compare.png')

# ==========================================
# 10. 公式拆解
# ==========================================
def draw_10_formula():
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.axis('off')
    ax.add_patch(Rectangle((0.05, 0.1), 0.9, 0.8, facecolor='#ffffff', ec='#cbd5e1', lw=1.5))
    ax.text(0.5, 0.72, r"$\mathrm{Na}_x\mathrm{TM}\mathrm{O}_2$ 通式化学骨架拆解", ha='center', fontsize=12.5, fontweight='bold', color=C_INK)
    ax.text(0.20, 0.45, "Nax\n钠离子储层\n提供可逆脱嵌容量\nO3: x≈1.0 | P2: x≈0.67", ha='center', va='center', fontsize=9.5, color=C_NA, fontweight='bold')
    ax.text(0.50, 0.45, "TM\n过渡金属层 (Fe/Mn/Ni)\n氧化还原反应电对\n主导工作电压与容量", ha='center', va='center', fontsize=9.5, color=C_TM, fontweight='bold')
    ax.text(0.80, 0.45, "O2\n阴离子骨架框架\nABC 或 AB 密堆积\n高电位需防晶格氧析出", ha='center', va='center', fontsize=9.5, color=C_O, fontweight='bold')
    save_fig(fig, '10_formula.png')

# ==========================================
# 11. 3D 点阵对比
# ==========================================
def draw_11_3d_layers():
    fig = plt.figure(figsize=(9, 4.5))
    
    ax1 = fig.add_subplot(121, projection='3d')
    for z in [0, 0.8, 1.6]:
        xx, yy = np.meshgrid(np.linspace(0, 1, 4), np.linspace(0, 1, 4))
        ax1.scatter(xx, yy, np.full_like(xx, z), color=C_TM, s=40, alpha=0.8)
    for z in [0.4, 1.2]:
        xx, yy = np.meshgrid(np.linspace(0.1, 0.9, 3), np.linspace(0.1, 0.9, 3))
        ax1.scatter(xx, yy, np.full_like(xx, z), color=C_NA, s=60, alpha=0.9)
    ax1.set_title("O3 三维多层交替点阵\n(TM层 - Na层 - TM层)", fontsize=10.5, fontweight='bold')
    ax1.set_axis_off()
    
    ax2 = fig.add_subplot(122, projection='3d')
    for z in [0, 1.0]:
        xx, yy = np.meshgrid(np.linspace(0, 1, 4), np.linspace(0, 1, 4))
        ax2.scatter(xx, yy, np.full_like(xx, z), color=C_TM, s=40, alpha=0.8)
    for z in [0.5]:
        xx, yy = np.meshgrid(np.linspace(0.1, 0.9, 3), np.linspace(0.1, 0.9, 3))
        ax2.scatter(xx, yy, np.full_like(xx, z), color=C_NA, s=70, alpha=0.9)
    ax2.set_title("P2 三维多层交替点阵\n(开阔棱柱通道)", fontsize=10.5, fontweight='bold')
    ax2.set_axis_off()
    
    save_fig(fig, '11_3d_layers.png')

# ==========================================
# 12. 钠电速记海报
# ==========================================
def draw_12_poster():
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    ax.axis('off')
    ax.add_patch(Rectangle((0.05, 0.05), 0.9, 0.9, facecolor='#f8fafc', ec='#94a3b8', lw=2))
    ax.text(0.5, 0.85, "钠离子电池层状正极材料核心决窍速记", ha='center', fontsize=13, fontweight='bold', color=C_INK)
    txt = (
        "1. 构型辨识: 字母定配位(O=八面体, P=三棱柱), 数字定周期(3层或2层一闭合)。\n"
        "2. 动力学规律: 三棱柱开大门(P2矩形面, ~0.24eV)跑得快; 八面体钻狗洞(O3三角形, ~0.55eV)易堵车。\n"
        "3. 能量与寿命: O3出厂满电(x=1.0)但高压相变剧烈; P2骨架皮实但初始缺钠(x=0.67)。\n"
        "4. 改性黄金法则: 体相双位点钉扎(Ca/Sn/Li/Cu)锁死相变，表面人工CEI隔绝电解液腐蚀。"
    )
    ax.text(0.1, 0.45, txt, ha='left', va='center', fontsize=10, linespacing=1.8, color='#334155')
    save_fig(fig, '12_poster.png')

# ==========================================
# 20. ABC 密堆积位点
# ==========================================
def draw_20_abc_sites():
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.axis('off')
    pts = {'A': (0, 0), 'B': (1, 0.577), 'C': (0, 1.155)}
    cols = {'A': '#e74c3c', 'B': '#3498db', 'C': '#2ecc71'}
    for k, p in pts.items():
        ax.add_patch(Circle(p, 0.35, color=cols[k], alpha=0.85))
        ax.text(p[0], p[1], k, ha='center', va='center', color='white', fontsize=14, fontweight='bold')
    ax.text(0.5, -0.6, "密排六方网格中三个不可重叠的投影落点: A, B, C", ha='center', fontsize=10.5, fontweight='bold')
    ax.set_xlim(-0.8, 1.8); ax.set_ylim(-0.9, 1.8); ax.set_aspect('equal')
    save_fig(fig, '20_abc_sites.png')

# ==========================================
# 21. O3 三步闭合
# ==========================================
def draw_21_o3_three_steps():
    fig, ax = plt.subplots(figsize=(7, 3.8))
    ax.axis('off')
    ax.text(0.5, 0.75, r"$\mathrm{O3}$ 氧层堆叠: 沿 A $\rightarrow$ B $\rightarrow$ C 三角形三步闭合", ha='center', fontsize=11, fontweight='bold', color=C_O3)
    ax.plot([0.2, 0.5, 0.8, 0.2], [0.3, 0.65, 0.3, 0.3], 'o-', lw=2.5, markersize=14, color=C_O3)
    ax.text(0.2, 0.22, "A 层", ha='center', fontweight='bold')
    ax.text(0.5, 0.72, "B 层", ha='center', fontweight='bold')
    ax.text(0.8, 0.22, "C 层", ha='center', fontweight='bold')
    save_fig(fig, '21_o3_three_steps.png')

# ==========================================
# 22. P2 两步闭合
# ==========================================
def draw_22_p2_two_steps():
    fig, ax = plt.subplots(figsize=(7, 3.8))
    ax.axis('off')
    ax.text(0.5, 0.75, r"$\mathrm{P2}$ 氧层堆叠: 在 A 与 B 之间两步对称往复闭合", ha='center', fontsize=11, fontweight='bold', color=C_P2)
    ax.plot([0.3, 0.7], [0.45, 0.45], 'o-', lw=3, markersize=16, color=C_P2)
    ax.annotate("", xy=(0.7, 0.52), xytext=(0.3, 0.52), arrowprops=dict(arrowstyle="->", lw=2, color=C_P2))
    ax.annotate("", xy=(0.3, 0.38), xytext=(0.7, 0.38), arrowprops=dict(arrowstyle="->", lw=2, color=C_P2))
    ax.text(0.3, 0.28, "A 层 (顶底对齐)", ha='center', fontweight='bold')
    ax.text(0.7, 0.28, "B 层 (顶底对齐)", ha='center', fontweight='bold')
    save_fig(fig, '22_p2_two_steps.png')

# ==========================================
# 23. 周期家族
# ==========================================
def draw_23_period_family():
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.axis('off')
    fams = ["P2 家族\n(2层闭合, 三棱柱)", "P3 家族\n(3层闭合, 倾斜棱柱)", "O3 家族\n(3层闭合, 八面体)", "O2 家族\n(2层闭合, 高压滑移相)"]
    cols = [C_P2, '#16a085', C_O3, '#8e44ad']
    for i, (f, c) in enumerate(zip(fams, cols)):
        ax.add_patch(Rectangle((0.08 + i*0.22, 0.2), 0.18, 0.6, facecolor=c, alpha=0.85))
        ax.text(0.08 + i*0.22 + 0.09, 0.5, f, ha='center', va='center', color='white', fontsize=9.5, fontweight='bold')
    ax.set_title("钠离子电池层状结构周期家族全貌图", fontsize=11.5, fontweight='bold')
    save_fig(fig, '23_period_family.png')

# ==========================================
# 24. 拓扑约束
# ==========================================
def draw_24_cannot_close():
    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    ax.axis('off')
    ax.text(0.5, 0.75, "几何拓扑约束: 为什么 O 型无法两步闭合？", ha='center', fontsize=11.5, fontweight='bold', color=C_INK)
    txt = (
        "• 八面体(O型)上下氧层必须交错(如 A-B 错开)。如果只有两层(A-B-A)，第三层无法满足八面体密堆积对称。\n"
        "• 三棱柱(P型)上下氧层必须直视对准(A-A 或 B-B)，两步 AB-BA 恰好在反演对称下完全闭合！"
    )
    ax.text(0.1, 0.35, txt, ha='left', va='center', fontsize=9.5, linespacing=1.8, color='#334155')
    save_fig(fig, '24_cannot_close.png')

# ==========================================
# 25. ML6 八面体配位 (CFT 基础，严谨三维渲染)
# ==========================================
def draw_25_ml6_octahedron():
    fig = plt.figure(figsize=(7.5, 5.2))
    ax = fig.add_subplot(111, projection='3d')
    
    d = 1.3
    # 6 个氧配体位置
    ligands = np.array([
        [d, 0, 0], [-d, 0, 0], [0, d, 0], [0, -d, 0], [0, 0, d], [0, 0, -d]
    ])
    labels = [r'$+x$', r'$-x$', r'$+y$', r'$-y$', r'$+z$', r'$-z$']
    
    # 八面体面片
    faces = [
        [ligands[4], ligands[0], ligands[2]],
        [ligands[4], ligands[2], ligands[1]],
        [ligands[4], ligands[1], ligands[3]],
        [ligands[4], ligands[3], ligands[0]],
        [ligands[5], ligands[0], ligands[2]],
        [ligands[5], ligands[2], ligands[1]],
        [ligands[5], ligands[1], ligands[3]],
        [ligands[5], ligands[3], ligands[0]]
    ]
    poly = Poly3DCollection(faces, alpha=0.25, facecolor=C_TM, edgecolor=C_TM, linewidths=1.5)
    ax.add_collection3d(poly)
    
    # 坐标轴与配位键
    ax.plot([-1.8, 1.8], [0, 0], [0, 0], 'k--', lw=1.2, alpha=0.5)
    ax.plot([0, 0], [-1.8, 1.8], [0, 0], 'k--', lw=1.2, alpha=0.5)
    ax.plot([0, 0], [0, 0], [-1.8, 1.8], 'k--', lw=1.2, alpha=0.5)
    
    # 氧配体球与标号
    for p, lab in zip(ligands, labels):
        ax.scatter([p[0]], [p[1]], [p[2]], color=C_O, s=140, edgecolors='black', zorder=5)
        ax.plot([0, p[0]], [0, p[1]], [0, p[2]], color='#e74c3c', lw=2.2, zorder=4)
        ax.text(p[0]*1.18, p[1]*1.18, p[2]*1.18, f'L ({lab})', fontsize=9.5, fontweight='bold', color=C_INK)
        
    # 中心 M 离子
    ax.scatter([0], [0], [0], color=C_TM, s=260, edgecolors='black', zorder=6, label=r'中心过渡金属 $\mathrm{M^{n+}}$ (反演中心 $i$)')
    ax.scatter([], [], [], color=C_O, s=140, edgecolors='black', label=r'6 个配体氧 $\mathrm{O^{2-}}$ (沿坐标轴正碰)')
    
    ax.set_title(r"$\mathrm{ML_6}$ 正八面体晶体场配位环境与坐标轴对称性 ($O_h$ 点群)", fontsize=11.5, fontweight='bold', pad=10)
    ax.set_axis_off()
    ax.set_xlim([-1.8, 1.8]); ax.set_ylim([-1.8, 1.8]); ax.set_zlim([-1.8, 1.8])
    ax.view_init(elev=24, azim=38)
    ax.legend(loc='lower center', frameon=False, fontsize=9.5)
    save_fig(fig, '25_ml6_octahedron.png')

# ==========================================
# 26. 五条 3d 轨道真实空间几何云瓣 (V100 CUDA 加速球面谐波)
# ==========================================
def draw_26_d_orbitals():
    # 利用 Tesla V100 GPU 显存快速构建高分辨率球坐标张量
    n_th, n_ph = 140, 280
    th = torch.linspace(0, np.pi, n_th, device=device)
    ph = torch.linspace(0, 2*np.pi, n_ph, device=device)
    TH, PH = torch.meshgrid(th, ph, indexing='ij')

    # CUDA 计算五条实球谐 d 轨道角向函数
    Y_dict = {
        'dz2': (0.25 * np.sqrt(5/np.pi) * (3*torch.cos(TH)**2 - 1), r'$d_{z^2}$', r'$e_g$ 迎头正碰', '沿 z 轴双叶 + 环形甜甜圈'),
        'dx2y2': (0.25 * np.sqrt(15/np.pi) * (torch.sin(TH)**2 * torch.cos(2*PH)), r'$d_{x^2-y^2}$', r'$e_g$ 迎头正碰', '直冲 x, y 轴氧配体'),
        'dxy': (0.25 * np.sqrt(15/np.pi) * (torch.sin(TH)**2 * torch.sin(2*PH)), r'$d_{xy}$', r'$t_{2g}$ 夹缝避让', 'xy 平面 45° 间隙避让'),
        'dyz': (0.5 * np.sqrt(15/np.pi) * (torch.sin(TH)*torch.cos(TH) * torch.sin(PH)), r'$d_{yz}$', r'$t_{2g}$ 夹缝避让', 'yz 平面 45° 间隙避让'),
        'dxz': (0.5 * np.sqrt(15/np.pi) * (torch.sin(TH)*torch.cos(TH) * torch.cos(PH)), r'$d_{xz}$', r'$t_{2g}$ 夹缝避让', 'xz 平面 45° 间隙避让')
    }

    fig = plt.figure(figsize=(15.5, 3.8))
    TH_np = TH.cpu().numpy()
    PH_np = PH.cpu().numpy()

    for idx, (k, (Y_t, title, grp, desc)) in enumerate(Y_dict.items()):
        ax = fig.add_subplot(1, 5, idx+1, projection='3d')
        Y_np = Y_t.cpu().numpy()
        R = np.abs(Y_np)
        X = R * np.sin(TH_np) * np.cos(PH_np)
        Y = R * np.sin(TH_np) * np.sin(PH_np)
        Z = R * np.cos(TH_np)
        
        # 相位映射: 正相位为金黄，负相位为钴蓝
        colors = np.empty(X.shape + (4,))
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                if Y_np[i, j] >= 0:
                    colors[i, j] = [0.93, 0.65, 0.15, 0.88]
                else:
                    colors[i, j] = [0.11, 0.35, 0.65, 0.88]
                    
        ax.plot_surface(X, Y, Z, facecolors=colors, shade=True, edgecolor='none', antialiased=True)
        ax.set_title(f'{title}\n{grp}\n({desc})', fontsize=9.5, fontweight='bold', pad=4)
        ax.set_axis_off()
        ax.view_init(elev=20, azim=45)

    fig.suptitle('Tesla V100 CUDA 严格量子力学五条 3d 轨道电子云瓣 (金黄: 正相位 +，深蓝: 负相位 -)', fontsize=12.5, fontweight='bold', y=0.98)
    fig.subplots_adjust(top=0.76, bottom=0.06, left=0.02, right=0.98)
    save_fig(fig, '26_d_orbitals.png')

# ==========================================
# 27. 正对氧 vs 夹缝避让
# ==========================================
def draw_27_pointing():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 4.2))
    
    # 左: dx2-y2 迎头撞击
    ax1.plot([-1.5, 1.5], [0, 0], 'k:', lw=1.2)
    ax1.plot([0, 0], [-1.5, 1.5], 'k:', lw=1.2)
    # 画 4 个叶瓣正对坐标轴
    for ang in [0, np.pi/2, np.pi, 3*np.pi/2]:
        col = C_GOLD if ang in [0, np.pi] else C_COBALT
        ax1.add_patch(Wedge((0, 0), 1.15, np.degrees(ang)-25, np.degrees(ang)+25, color=col, alpha=0.75))
    for pos in [(1.25, 0), (-1.25, 0), (0, 1.25), (0, -1.25)]:
        ax1.add_patch(Circle(pos, 0.22, color=C_O, ec='black', lw=1.5, zorder=5))
    ax1.text(0, 0, r'$d_{x^2-y^2}$' + '\n迎头正碰', ha='center', va='center', fontsize=10, fontweight='bold', color='white',
             bbox=dict(boxstyle='circle', facecolor=C_INK, alpha=0.8))
    ax1.text(0, -1.6, r"$e_g$ 轨道: 4个波瓣直接迎面撞击配体氧电子云" + "\n" + r"静电斥力极大 $\rightarrow$ 轨道能级急剧升高 (+0.6 $\Delta_o$)",
             ha='center', fontsize=9, color=C_INK)
    ax1.set_title(r'$e_g$ 轨道: 迎头正碰强斥力', fontsize=11, fontweight='bold', color=C_O3)
    ax1.set_xlim(-1.8, 1.8); ax1.set_ylim(-1.8, 1.6); ax1.axis('off'); ax1.set_aspect('equal')

    # 右: dxy 钻进夹缝
    ax2.plot([-1.5, 1.5], [0, 0], 'k:', lw=1.2)
    ax2.plot([0, 0], [-1.5, 1.5], 'k:', lw=1.2)
    for ang in [np.pi/4, 3*np.pi/4, 5*np.pi/4, 7*np.pi/4]:
        col = C_GOLD if ang in [np.pi/4, 5*np.pi/4] else C_COBALT
        ax2.add_patch(Wedge((0, 0), 1.15, np.degrees(ang)-25, np.degrees(ang)+25, color=col, alpha=0.75))
    for pos in [(1.25, 0), (-1.25, 0), (0, 1.25), (0, -1.25)]:
        ax2.add_patch(Circle(pos, 0.22, color=C_O, ec='black', lw=1.5, zorder=5))
    ax2.text(0, 0, r'$d_{xy}$' + '\n夹缝避让', ha='center', va='center', fontsize=10, fontweight='bold', color='white',
             bbox=dict(boxstyle='circle', facecolor=C_P2, alpha=0.8))
    ax2.text(0, -1.6, r"$t_{2g}$ 轨道: 4个波瓣旋转 45° 完美躲入氧原子间隙" + "\n" + r"静电斥力微弱 $\rightarrow$ 轨道能级下降稳定 (-0.4 $\Delta_o$)",
             ha='center', fontsize=9, color=C_INK)
    ax2.set_title(r'$t_{2g}$ 轨道: 45° 间隙避让低能级', fontsize=11, fontweight='bold', color=C_P2)
    ax2.set_xlim(-1.8, 1.8); ax2.set_ylim(-1.8, 1.6); ax2.axis('off'); ax2.set_aspect('equal')

    save_fig(fig, '27_pointing.png')

# ==========================================
# 28. 八面体晶体场劈裂与重心守恒
# ==========================================
def draw_28_octahedral_split():
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.axis('off')
    
    # 能量标尺
    ax.annotate("", xy=(0.08, 0.95), xytext=(0.08, 0.05), arrowprops=dict(arrowstyle="->", lw=2, color='#555555'))
    ax.text(0.06, 0.98, "能量 (E)", fontsize=10.5, fontweight='bold')

    # 自由离子 5d 简并
    ax.plot([0.16, 0.38], [0.45, 0.45], 'k-', lw=3.5)
    ax.text(0.27, 0.37, "自由金属离子\n5 重简并 d 轨道", ha='center', fontsize=10, fontweight='bold')

    # 重心守恒虚线
    ax.plot([0.38, 0.92], [0.45, 0.45], 'k--', lw=1.2, alpha=0.45)
    ax.text(0.94, 0.45, "能量重心\n(Barycenter)", va='center', fontsize=9, color='#666666')

    # eg 上升 +0.6 Delta
    ax.plot([0.65, 0.88], [0.75, 0.75], color=C_O3, lw=4)
    ax.text(0.765, 0.82, r'$e_g\ (d_{z^2}, d_{x^2-y^2}) \ [+0.6\Delta_o = +6Dq]$', ha='center', fontsize=10.5, fontweight='bold', color=C_O3)

    # t2g 下降 -0.4 Delta
    ax.plot([0.65, 0.88], [0.25, 0.25], color=C_P2, lw=4)
    ax.text(0.765, 0.17, r'$t_{2g}\ (d_{xy}, d_{yz}, d_{xz}) \ [-0.4\Delta_o = -4Dq]$', ha='center', fontsize=10.5, fontweight='bold', color=C_P2)

    # 劈裂连线
    ax.plot([0.38, 0.65], [0.45, 0.75], 'k:', lw=1.5, alpha=0.5)
    ax.plot([0.38, 0.65], [0.45, 0.25], 'k:', lw=1.5, alpha=0.5)

    # 能隙双向箭头
    ax.annotate("", xy=(0.90, 0.75), xytext=(0.90, 0.25), arrowprops=dict(arrowstyle="<->", lw=2.2, color=C_ACCENT))
    ax.text(0.92, 0.50, r"$\Delta_o = 10Dq$" + "\n(八面体晶体场能)", fontsize=11, fontweight='bold', color=C_ACCENT, va='center')

    # 重心守恒公式说明
    ax.text(0.52, 0.05, r"重心守恒定理: $2 \times (+0.6\Delta_o) + 3 \times (-0.4\Delta_o) = 0$", 
            ha='center', fontsize=10.5, fontweight='bold', color=C_INK,
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#f8fafc', edgecolor='#cbd5e1'))

    ax.set_xlim(0.02, 1.15); ax.set_ylim(0, 1.05)
    fig.suptitle(r"正八面体晶体场中的 $d$ 轨道能级劈裂与重心守恒规则", fontsize=12, fontweight='bold')
    save_fig(fig, '28_octahedral_split.png')

# ==========================================
# 29. 高自旋与低自旋 (HS vs LS)
# ==========================================
def draw_29_hs_ls():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 4.2))
    
    # HS (弱场高自旋 d4, 如 Mn3+)
    ax1.axis('off')
    ax1.plot([0.2, 0.8], [0.8, 0.8], color=C_O3, lw=3)
    ax1.plot([0.2, 0.8], [0.25, 0.25], color=C_P2, lw=3)
    # 电子自旋箭头
    ax1.annotate("", xy=(0.35, 0.42), xytext=(0.35, 0.15), arrowprops=dict(arrowstyle="->", lw=2.5, color='#111111'))
    ax1.annotate("", xy=(0.50, 0.42), xytext=(0.50, 0.15), arrowprops=dict(arrowstyle="->", lw=2.5, color='#111111'))
    ax1.annotate("", xy=(0.65, 0.42), xytext=(0.65, 0.15), arrowprops=dict(arrowstyle="->", lw=2.5, color='#111111'))
    ax1.annotate("", xy=(0.50, 0.97), xytext=(0.50, 0.70), arrowprops=dict(arrowstyle="->", lw=2.5, color=C_ACCENT))
    ax1.text(0.5, 0.85, r'$e_g^1$ (孤电子占位, 强烈不对称)', ha='center', fontsize=9.5, color=C_O3, fontweight='bold')
    ax1.text(0.5, 0.05, r'$t_{2g}^3$' + "\n高自旋配置 ($S=2$)\n" + r"$\Delta_o < P$ (成对能) $\rightarrow$ 剧烈姜-泰勒畸变！", 
             ha='center', fontsize=9.5, fontweight='bold')
    ax1.set_title(r"高自旋 HS ($\mathrm{Mn^{3+} / Fe^{4+}}$)", fontsize=11, fontweight='bold', color=C_ACCENT)

    # LS (强场低自旋 d4)
    ax2.axis('off')
    ax2.plot([0.2, 0.8], [0.8, 0.8], color=C_O3, lw=3)
    ax2.plot([0.2, 0.8], [0.25, 0.25], color=C_P2, lw=3)
    ax2.annotate("", xy=(0.32, 0.42), xytext=(0.32, 0.15), arrowprops=dict(arrowstyle="->", lw=2.2, color='#111111'))
    ax2.annotate("", xy=(0.38, 0.15), xytext=(0.38, 0.42), arrowprops=dict(arrowstyle="->", lw=2.2, color='#c0392b'))
    ax2.annotate("", xy=(0.50, 0.42), xytext=(0.50, 0.15), arrowprops=dict(arrowstyle="->", lw=2.2, color='#111111'))
    ax2.annotate("", xy=(0.65, 0.42), xytext=(0.65, 0.15), arrowprops=dict(arrowstyle="->", lw=2.2, color='#111111'))
    ax2.text(0.5, 0.85, r'$e_g^0$ (空轨道)', ha='center', fontsize=9.5, color=C_O3)
    ax2.text(0.5, 0.05, r'$t_{2g}^4$' + "\n低自旋配置 ($S=1$)\n" + r"$\Delta_o > P$ (成对能) $\rightarrow$ 晶格较稳定", 
             ha='center', fontsize=9.5, fontweight='bold')
    ax2.set_title("低自旋 LS (强配体场)", fontsize=11, fontweight='bold', color=C_P2)

    fig.suptitle(r"$d^4$ 过渡金属离子高自旋与低自旋电子态及钠电活性根源", fontsize=12, fontweight='bold')
    save_fig(fig, '29_hs_ls.png')

# ==========================================
# 13. 姜-泰勒起源
# ==========================================
def draw_13_jt_origin():
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.axis('off')
    ax.plot([0.1, 0.35], [0.5, 0.5], 'k-', lw=3)
    ax.text(0.22, 0.55, r'简并 $e_g$ 轨道' + '\n(电子占据不均)', ha='center', fontsize=10, fontweight='bold')

    ax.plot([0.65, 0.9], [0.75, 0.75], color=C_ACCENT, lw=3)
    ax.text(0.78, 0.82, r'$d_{x^2-y^2}$ (空/能级上升)', ha='center', fontsize=9.5, color=C_ACCENT, fontweight='bold')

    ax.plot([0.65, 0.9], [0.25, 0.25], color=C_O3, lw=3)
    ax.text(0.78, 0.17, r'$d_{z^2}$ (1个电子/能级下降 $\Delta E_{JT}$)', ha='center', fontsize=9.5, color=C_O3, fontweight='bold')

    ax.plot([0.35, 0.65], [0.5, 0.75], 'k:', alpha=0.5)
    ax.plot([0.35, 0.65], [0.5, 0.25], 'k:', alpha=0.5)
    
    ax.text(0.5, 0.02, r"姜-泰勒定理: 简并基态发生对称性自发破缺，释放 $\Delta E_{JT}$ 降低体系总能量", 
            ha='center', fontsize=10, fontweight='bold', color=C_INK)
    fig.suptitle("姜-泰勒畸变热力学驱动力: 解除轨道简并降低电子自由能", fontsize=11.5, fontweight='bold')
    save_fig(fig, '13_jt_origin.png')

# ==========================================
# 14. 姜-泰勒畸变三种八面体 (严谨 3D 渲染)
# ==========================================
def draw_14_jt_octahedra():
    fig = plt.figure(figsize=(11.5, 4.2))
    
    # 1. 规则正八面体 Oh
    ax1 = fig.add_subplot(131, projection='3d')
    d1 = 1.0
    pts1 = np.array([[d1, 0, 0], [-d1, 0, 0], [0, d1, 0], [0, -d1, 0], [0, 0, d1], [0, 0, -d1]])
    f1 = [[pts1[4], pts1[0], pts1[2]], [pts1[4], pts1[2], pts1[1]], [pts1[4], pts1[1], pts1[3]], [pts1[4], pts1[3], pts1[0]],
          [pts1[5], pts1[0], pts1[2]], [pts1[5], pts1[2], pts1[1]], [pts1[5], pts1[1], pts1[3]], [pts1[5], pts1[3], pts1[0]]]
    ax1.add_collection3d(Poly3DCollection(f1, alpha=0.25, facecolor=C_O3, edgecolor=C_O3, lw=1.2))
    for p in pts1:
        ax1.scatter([p[0]], [p[1]], [p[2]], color=C_O, s=50)
    ax1.scatter([0], [0], [0], color=C_TM, s=120)
    ax1.set_title("1. 规则正八面体\n($O_h$, 6 键等长: $d_z = d_{xy}$)", fontsize=10, fontweight='bold')
    ax1.set_axis_off(); ax1.view_init(elev=20, azim=35)
    ax1.set_xlim([-1.3, 1.3]); ax1.set_ylim([-1.3, 1.3]); ax1.set_zlim([-1.3, 1.3])

    # 2. 轴向拉长 z-out (D4h)
    ax2 = fig.add_subplot(132, projection='3d')
    d2_xy, d2_z = 0.85, 1.45
    pts2 = np.array([[d2_xy, 0, 0], [-d2_xy, 0, 0], [0, d2_xy, 0], [0, -d2_xy, 0], [0, 0, d2_z], [0, 0, -d2_z]])
    f2 = [[pts2[4], pts2[0], pts2[2]], [pts2[4], pts2[2], pts2[1]], [pts2[4], pts2[1], pts2[3]], [pts2[4], pts2[3], pts2[0]],
          [pts2[5], pts2[0], pts2[2]], [pts2[5], pts2[2], pts2[1]], [pts2[5], pts2[1], pts2[3]], [pts2[5], pts2[3], pts2[0]]]
    ax2.add_collection3d(Poly3DCollection(f2, alpha=0.35, facecolor='#d35400', edgecolor='#d35400', lw=1.2))
    for p in pts2:
        ax2.scatter([p[0]], [p[1]], [p[2]], color=C_O, s=50)
    ax2.scatter([0], [0], [0], color=C_TM, s=120)
    # 标出拉长的 z 键
    ax2.plot([0, 0], [0, 0], [-d2_z, d2_z], color='#c0392b', lw=2.5, linestyle='--')
    ax2.set_title(r"2. 轴向拉长 ($z$-out, $D_{4h}$)" + "\n" + r"(最普遍, $d_z > d_{xy}$, $\mathrm{Mn^{3+}/Fe^{4+}}$)", fontsize=10, fontweight='bold', color='#c0392b')
    ax2.set_axis_off(); ax2.view_init(elev=20, azim=35)
    ax2.set_xlim([-1.3, 1.3]); ax2.set_ylim([-1.3, 1.3]); ax2.set_zlim([-1.5, 1.5])

    # 3. 轴向压缩 z-in (D4h)
    ax3 = fig.add_subplot(133, projection='3d')
    d3_xy, d3_z = 1.25, 0.70
    pts3 = np.array([[d3_xy, 0, 0], [-d3_xy, 0, 0], [0, d3_xy, 0], [0, -d3_xy, 0], [0, 0, d3_z], [0, 0, -d3_z]])
    f3 = [[pts3[4], pts3[0], pts3[2]], [pts3[4], pts3[2], pts3[1]], [pts3[4], pts3[1], pts3[3]], [pts3[4], pts3[3], pts3[0]],
          [pts3[5], pts3[0], pts3[2]], [pts3[5], pts3[2], pts3[1]], [pts3[5], pts3[1], pts3[3]], [pts3[5], pts3[3], pts3[0]]]
    ax3.add_collection3d(Poly3DCollection(f3, alpha=0.25, facecolor='#7f8c8d', edgecolor='#7f8c8d', lw=1.2))
    for p in pts3:
        ax3.scatter([p[0]], [p[1]], [p[2]], color=C_O, s=50)
    ax3.scatter([0], [0], [0], color=C_TM, s=120)
    ax3.set_title(r"3. 轴向压缩 ($z$-in, $D_{4h}$)" + "\n" + r"(较罕见, $d_z < d_{xy}$)", fontsize=10, fontweight='bold')
    ax3.set_axis_off(); ax3.view_init(elev=20, azim=35)
    fig.suptitle("晶体场中正八面体配位几何在姜-泰勒效应下的三种构型演变", fontsize=12, fontweight='bold', y=0.98)
    fig.subplots_adjust(top=0.76, bottom=0.08)
    save_fig(fig, '14_jt_octahedra.png')

# ==========================================
# 15. JT 活性表
# ==========================================
def draw_15_jt_ions():
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    ax.axis('off')
    headers = ["过渡金属离子", "电子构型态", "d 轨道电子填布", "姜-泰勒 (JT) 活性评级", "钠电体系工程影响"]
    data = [
        ["Mn3+", "高自旋 d4", "t2g3 eg1", "★★★★★ 极强 (原生破坏)", "造成 NaMnO2 出现严重单斜相变"],
        ["Fe4+", "高自旋 d4", "t2g3 eg1", "★★★★★ 极强 (高压现身)", "高电压深充阶段诱发相变与微裂纹"],
        ["Ni3+", "低自旋 d7", "t2g6 eg1", "★★★★☆ 较强 (脱钠阶段)", "镍基层状正极高压容量衰减主因之一"],
        ["Mn4+", "d3", "t2g3 eg0", "☆☆☆☆☆ 无 (稳定六方)", "极其稳定, 是体相掺杂设计的压舱石"],
        ["Fe3+", "高自旋 d5", "t2g3 eg2", "☆☆☆☆☆ 无 (半满对称)", "出厂初始态稳定, 球形电荷无畸变"]
    ]
    tab = ax.table(cellText=data, colLabels=headers, loc='center', cellLoc='center',
                   colColours=['#e2e8f0', '#edf2f7', '#edf2f7', '#fee2e2', '#f0fdf4'])
    tab.scale(1, 1.8)
    tab.set_fontsize(9)
    ax.set_title("钠电池过渡金属离子姜-泰勒 (JT) 活性与晶格破坏分级对照表", fontsize=11.5, fontweight='bold', pad=15)
    save_fig(fig, '15_jt_ions.png')

# ==========================================
# 16. Fe4+ 循环演变
# ==========================================
def draw_16_fe4_cycle():
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('off')
    ax.add_patch(Rectangle((0.08, 0.15), 0.35, 0.7, facecolor='#e8f8f0', ec=C_P2, lw=2))
    ax.text(0.255, 0.68, "初始放电态 (安全区)", ha='center', fontsize=11, fontweight='bold', color=C_P2)
    ax.text(0.255, 0.42, "Fe3+ (d5 半满对称)\nMn3+ 部分存在\n晶格应变小 | 结构稳定", ha='center', fontsize=9.5, linespacing=1.6)

    ax.add_patch(Rectangle((0.57, 0.15), 0.35, 0.7, facecolor='#fdf2e9', ec=C_ACCENT, lw=2))
    ax.text(0.745, 0.68, "高电压充电态 (高危区)", ha='center', fontsize=11, fontweight='bold', color=C_ACCENT)
    ax.text(0.745, 0.42, "Fe4+ (d4 强 JT 活性)\nMn3+ 氧化为 Mn4+\n大量高自旋 Fe4+ 引发微裂纹", ha='center', fontsize=9.5, linespacing=1.6)

    ax.annotate("", xy=(0.55, 0.55), xytext=(0.45, 0.55), arrowprops=dict(arrowstyle="->", lw=2.5, color='#333333'))
    ax.text(0.50, 0.60, "充电脱钠\n(> 3.8 V)", ha='center', fontsize=9, fontweight='bold')
    
    ax.annotate("", xy=(0.45, 0.40), xytext=(0.55, 0.40), arrowprops=dict(arrowstyle="->", lw=2.5, color='#333333'))
    ax.text(0.50, 0.32, "放电嵌钠\n(< 3.0 V)", ha='center', fontsize=9, fontweight='bold')

    fig.suptitle(r"充放电循环中 $\mathrm{Fe^{3+} \leftrightarrow Fe^{4+}}$ 价态演变与姜-泰勒风险激化", fontsize=11.5, fontweight='bold')
    save_fig(fig, '16_fe4_cycle.png')

# ==========================================
# 17. 协同姜-泰勒与掺杂打断
# ==========================================
def draw_17_cooperative():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8.5, 4))
    
    # 协同咬合
    ax1.axis('off')
    for i in range(3):
        for j in range(3):
            ax1.add_patch(Rectangle((i*0.3, j*0.3), 0.22, 0.22, facecolor='#fce4ec', ec='#c2185b', lw=1.5))
    ax1.set_title("未改性: 协同姜-泰勒咬合\n(畸变长程贯通, 产生大应变裂纹)", fontsize=10.5, fontweight='bold', color='#c2185b')
    ax1.set_xlim(-0.1, 1.0); ax1.set_ylim(-0.1, 1.0); ax1.set_aspect('equal')

    # 掺杂打断
    ax2.axis('off')
    for i in range(3):
        for j in range(3):
            if (i, j) in [(1, 1), (0, 2)]:
                ax2.add_patch(Rectangle((i*0.3, j*0.3), 0.22, 0.22, facecolor=C_TM, ec='black', lw=2))
                ax2.text(i*0.3+0.11, j*0.3+0.11, "Ti/Li", ha='center', va='center', color='white', fontsize=8, fontweight='bold')
            else:
                ax2.add_patch(Rectangle((i*0.3, j*0.3), 0.22, 0.22, facecolor='#e8f8f0', ec=C_P2, lw=1.5))
    ax2.set_title("掺杂改性: 孤立非活性离子\n(剪断协同长程链, 应变被局域吸收)", fontsize=10.5, fontweight='bold', color=C_P2)
    ax2.set_xlim(-0.1, 1.0); ax2.set_ylim(-0.1, 1.0); ax2.set_aspect('equal')

    save_fig(fig, '17_cooperative.png')

# ==========================================
# 18. 掺杂抑制 6 条路径
# ==========================================
def draw_18_doping():
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    ax.axis('off')
    routes = [
        "1. 电荷补偿定格法: 掺低价 Li+/Mg2+ 诱导过渡金属升高平均价态，避开 Mn3+/Fe4+ 敏感区。",
        "2. 强共价键钉扎法: 掺 Ti4+/Zr4+/Sn4+ 形成超强 M-O 骨架键，强力抵抗晶格各向异性收缩。",
        "3. 协同长程剪断法: 引入非 JT 活性离子稀释活性中心，彻底阻断自发应变的长程级联传递。",
        "4. 能带与超交换重构: 掺杂 Cu2+ 调节局域自旋态，增强层内超交换作用，稳定氧骨架。",
        "5. 柱撑间距稳定法: 掺大半径 Ca2+ 钉扎钠层空位，作为化学支柱防止深脱钠层间塌陷。",
        "6. 高熵固溶平滑法: 多元高熵协同打乱长程有序，变突变两相反应为连续平滑单相反应。"
    ]
    ax.add_patch(Rectangle((0.05, 0.05), 0.9, 0.9, facecolor='#f8fafc', ec='#94a3b8', lw=1.5))
    ax.text(0.5, 0.88, "现代前沿顶刊设计: 抑制姜-泰勒与阳离子迁移的六大通用改性范式", ha='center', fontsize=12, fontweight='bold', color=C_INK)
    y_starts = np.linspace(0.72, 0.15, len(routes))
    for y, r in zip(y_starts, routes):
        ax.text(0.08, y, r, ha='left', va='center', fontsize=9.2, color='#1e293b')
    save_fig(fig, '18_doping.png')

# ==========================================
# 19. JT 速记海报
# ==========================================
def draw_19_jt_poster():
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    ax.axis('off')
    ax.add_patch(Rectangle((0.05, 0.05), 0.9, 0.9, facecolor='#fffbeb', ec='#f59e0b', lw=2))
    ax.text(0.5, 0.82, "姜-泰勒 (Jahn-Teller) 晶格破坏效应核心速记", ha='center', fontsize=12.5, fontweight='bold', color='#92400e')
    txt = (
        "• 物理本质: 电子想偷懒 (轨道不对称占据，通过自发晶格畸变降低电子自由能)。\n"
        "• 祸害元凶: 高自旋 d4 离子 (未充电的 Mn3+，高电压充电出现的 Fe4+)。\n"
        "• 破坏机制: 局部轻微拉长不可怕，整层协同咬合引发的各向异性巨变最致命！\n"
        "• 工业化破解: 掺 Li/Mg 提价态、掺 Ti/Sn 强共价键钉扎、多元素高熵剪断协同链！"
    )
    ax.text(0.1, 0.42, txt, ha='left', va='center', fontsize=10, linespacing=1.8, color='#78350f')
    save_fig(fig, '19_jt_poster.png')

# ==========================================
# 主执行入口
# ==========================================
def main():
    print("=" * 60)
    print("[*] 正在执行全套 29 张钠电与晶体场学术机理图表生成 (Tesla V100 CUDA 加速版)...")
    print("=" * 60)
    
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
    
    print("=" * 60)
    print(f"[SUCCESS] 29 张高清学术机理插图已全部生成完毕！")
    print(f"[PATH] 输出目标目录: {OUT_DIR}")
    print("=" * 60)

if __name__ == '__main__':
    main()
