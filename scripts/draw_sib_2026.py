# -*- coding: utf-8 -*-
"""
scripts/draw_sib_2026.py
2026 年钠电层状正极发展：化学视角学术插图
基于 2026 年 JES / Chem. Sci. / ACS AMI / Adv. Mater. / JEC 等文献
"""

import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import numpy as np
import matplotlib as mpl
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.patches import (
    FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Polygon,
    Wedge, Arc, Ellipse, PathPatch,
)
from matplotlib.path import Path
from matplotlib.lines import Line2D
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
]
for fp in FONT_CANDIDATES:
    if os.path.exists(fp):
        fm.fontManager.addfont(fp)

mpl.rcParams["font.sans-serif"] = ["WenQuanYi Micro Hei", "WenQuanYi Zen Hei", "DejaVu Sans"]
mpl.rcParams["axes.unicode_minus"] = False
mpl.rcParams["figure.autolayout"] = False
mpl.rcParams["savefig.dpi"] = 220
mpl.rcParams["savefig.bbox"] = "tight"
mpl.rcParams["mathtext.fontset"] = "dejavusans"

C_O3 = "#1d4e89"
C_P2 = "#2d6a4f"
C_NA = "#e69f00"
C_TM = "#00a087"
C_O = "#e74c3c"
C_ACCENT = "#d35400"
C_BG = "#ffffff"
C_PAPER = "#f7f4ee"
C_CARD = "#fffaf3"
C_MUTED = "#5c6570"
C_INK = "#1c2430"
C_GOLD = "#b8860b"
C_LINE = "#e2d8c8"
C_FE = "#c0392b"
C_MN = "#8e44ad"
C_NI = "#2980b9"
C_TI = "#16a085"
C_AL = "#7f8c8d"
C_F = "#27ae60"
C_N = "#8e44ad"

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images"))
os.makedirs(OUT_DIR, exist_ok=True)


def save_fig(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, facecolor=C_BG, edgecolor="none")
    plt.close(fig)
    print(f"[OK] {name}")


def rounded(ax, x, y, w, h, fc, ec, lw=1.4, r=0.04, z=2, alpha=1.0):
    p = FancyBboxPatch(
        (x, y), w, h, boxstyle=f"round,pad={r}",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z, alpha=alpha,
        mutation_aspect=1,
    )
    ax.add_patch(p)
    return p


def arrow(ax, x1, y1, x2, y2, color=C_INK, lw=1.6, style="-|>", rad=0.0):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle=style, mutation_scale=12, lw=lw, color=color,
        connectionstyle=f"arc3,rad={rad}", zorder=4,
    ))


# ============================================================
# 30. 2026 文献地图
# ============================================================
def draw_30_map():
    fig, ax = plt.subplots(figsize=(11.2, 6.4))
    ax.set_xlim(0, 11.2)
    ax.set_ylim(0, 6.4)
    ax.axis("off")
    ax.set_title("2026 钠电层状正极：化学问题与文献坐标", fontsize=14,
                 color=C_INK, pad=8)

    pillars = [
        (0.25, 4.55, 2.5, 1.55, C_O3, "高电压结构化学",
         "4.0 V O/P 杂化\nc 轴坍塌"),
        (3.0, 4.55, 2.5, 1.55, C_P2, "熵与局域化学",
         "O3@P2 外延\n高熵 O3"),
        (5.75, 4.55, 2.5, 1.55, C_GOLD, "双相互锁",
         "P2/O3 互锁\nO3 相 < 20%"),
        (8.5, 4.55, 2.45, 1.55, C_ACCENT, "键合与阴离子",
         "Al/Ti 共掺\nF/N 双参数"),
    ]
    for x, y, w, h, c, title, body in pillars:
        rounded(ax, x, y, w, h, "#fff", c, lw=2.0, r=0.03)
        ax.add_patch(Rectangle((x, y + h - 0.38), w, 0.38, facecolor=c, zorder=3))
        ax.text(x + w / 2, y + h - 0.19, title, ha="center", va="center",
                color="white", fontsize=10.5, zorder=4)
        ax.text(x + w / 2, y + 0.58, body, ha="center", va="center",
                fontsize=8.4, color=C_INK, linespacing=1.45, zorder=4)

    lower = [
        (0.25, 2.55, 3.4, 1.7, "#1a5276", "氧阴离子氧化还原",
         "调 O 2p 价带\n应变 1.23% → 0.45%"),
        (3.85, 2.55, 3.5, 1.7, "#1e8449", "表面与空气化学",
         "丙二酸中和残碱\n120 圈 79% → 89%"),
        (7.55, 2.55, 3.4, 1.7, "#6c3483", "尖晶石异质结",
         "抑相变 · 抗空气\n加速 Na$^+$ 扩散"),
    ]
    for x, y, w, h, c, title, body in lower:
        rounded(ax, x, y, w, h, "#fff", c, lw=2.0, r=0.03)
        ax.add_patch(Rectangle((x, y + h - 0.38), w, 0.38, facecolor=c, zorder=3))
        ax.text(x + w / 2, y + h - 0.19, title, ha="center", va="center",
                color="white", fontsize=10.5, zorder=4)
        ax.text(x + w / 2, y + 0.66, body, ha="center", va="center",
                fontsize=8.6, color=C_INK, linespacing=1.45, zorder=4)

    rounded(ax, 0.25, 1.15, 10.7, 0.95, "#f4f0e6", C_GOLD, lw=1.6, r=0.02)
    ax.text(5.6, 1.62, "主线：改写电荷补偿、键合与层滑移的耦合",
            ha="center", va="center", fontsize=11, color=C_INK)

    save_fig(fig, "30_lit_map_2026.png")


# ============================================================
# 31. 氧化还原阶梯
# ============================================================
def draw_31_redox():
    fig, ax = plt.subplots(figsize=(10.6, 5.6))
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 5.6)
    ax.axis("off")
    ax.set_title(r"层状正极的电荷补偿阶梯：谁在给电子，谁在拆骨架",
                 fontsize=13.5, color=C_INK, pad=6)

    ax.annotate("", xy=(0.7, 4.85), xytext=(0.7, 0.55),
                arrowprops=dict(arrowstyle="<|-|>", lw=2.2, color=C_INK))
    ax.text(0.38, 2.7, "电压 / V vs Na$^+$/Na", rotation=90, ha="center", va="center",
            fontsize=9, color=C_MUTED)

    rungs = [
        (4.62, 4.5, C_O, r"O$^{2-}$ / O$^{n-}$  晶格氧", "额外容量 · O$_2$ 逸出入口"),
        (3.68, 3.8, C_FE, r"Fe$^{3+}$ / Fe$^{4+}$", "开 JT · 抽氧电子"),
        (2.74, 3.3, C_NI, r"Ni$^{2+}$ / Ni$^{3+}$ / Ni$^{4+}$", "主力容量平台"),
        (1.80, 2.6, C_MN, r"Mn$^{3+}$ / Mn$^{4+}$", "骨架 · Mn$^{4+}$ 稳定"),
        (0.86, 0.0, C_MUTED, r"结构离子  Ti$^{4+}$  Al$^{3+}$  Mg$^{2+}$  Zr$^{4+}$", "钉氧 · 撑层"),
    ]
    for y, v, c, title, note in rungs:
        ax.plot([0.85, 1.15], [y, y], color=c, lw=3)
        vlabel = f"{v:.1f}" if v > 0.1 else "—"
        ax.text(1.22, y, vlabel, ha="left", va="center", fontsize=9, color=c)
        rounded(ax, 1.85, y - 0.38, 8.4, 0.76, "#fff", c, lw=1.6, r=0.02)
        ax.text(2.05, y + 0.14, title, ha="left", va="center", fontsize=10.2,
                color=c)
        ax.text(2.05, y - 0.16, note, ha="left", va="center", fontsize=8.2, color=C_INK, linespacing=1.25)

    save_fig(fig, "31_redox_ladder.png")


# ============================================================
# 32. 高电压 c 轴坍塌 (Ye 2026 JES)
# ============================================================
def draw_32_collapse():
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 5.0))

    ax = axes[0]
    ax.set_xlim(-0.2, 4.2)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    ax.set_title("截止电压 3.8 V：O3 骨架可逆", fontsize=11, color=C_O3)

    def slabs(ax, c_span, stagger, alpha_na=0.95):
        ys = np.linspace(0.6, 0.6 + c_span, 7)
        for i, y in enumerate(ys):
            if i % 2 == 0:
                xs = np.linspace(0.5, 3.5, 8) + (0.12 if stagger and (i // 2) % 2 else 0)
                ax.scatter(xs, [y] * len(xs), s=70, c=C_O, edgecolors="k", lw=0.4, zorder=3)
            else:
                xs = np.linspace(0.7, 3.3, 6)
                ax.scatter(xs, [y] * len(xs), s=90, c=C_TM, edgecolors="k", lw=0.4, zorder=4)
                mid = (ys[i - 1] + y) / 2 if i else y
        for i in range(3):
            yna = 0.6 + c_span * (0.18 + i * 0.28)
            xs = np.linspace(0.8, 3.2, 5)
            ax.scatter(xs, [yna] * len(xs), s=110, c=C_NA, edgecolors="k", lw=0.5,
                       alpha=alpha_na, zorder=5)
        ax.annotate("", xy=(3.9, 0.6), xytext=(3.9, 0.6 + c_span),
                    arrowprops=dict(arrowstyle="<->", color=C_INK, lw=1.5))
        ax.text(4.05, 0.6 + c_span / 2, "c", ha="left", va="center", fontsize=11)

    slabs(ax, 4.0, True, 0.95)
    ax.text(2.0, 0.22, r"Na$_x$MO$_2$", ha="center", va="center",
            fontsize=9, color=C_MUTED)

    ax = axes[1]
    ax.set_xlim(-0.2, 4.2)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    ax.set_title("截止电压 4.0 V：O/P 杂化 + c 坍塌", fontsize=11, color=C_ACCENT)
    slabs(ax, 2.55, True, 0.35)
    ax.add_patch(Polygon([[0.4, 2.3], [3.6, 2.55], [3.6, 3.15], [0.4, 2.9]],
                         closed=True, facecolor="#fdebd0", edgecolor=C_ACCENT, lw=1.6, alpha=0.7))
    ax.text(2.0, 2.72, "O/P 杂化层", ha="center", va="center",
            fontsize=9.5, color=C_ACCENT)

    fig.suptitle("4.0 V 多出来的容量，买的是一次不可逆的层间重构",
                 fontsize=12, color=C_INK, y=0.02)
    plt.tight_layout(rect=[0, 0.06, 1, 1])
    save_fig(fig, "32_highV_collapse.png")


# ============================================================
# 33. 高熵 / 中熵 TM 混排
# ============================================================
def draw_33_entropy():
    fig, ax = plt.subplots(figsize=(10.4, 5.4))
    ax.set_xlim(0, 10.4)
    ax.set_ylim(0, 5.4)
    ax.axis("off")
    ax.set_title(r"构型熵：把 TM 层从“有序条纹”改写成“化学噪声”",
                 fontsize=13.2, color=C_INK, pad=6)

    rng = np.random.default_rng(7)
    colors_order = [C_NI, C_NI, C_FE, C_FE, C_MN, C_MN]
    colors_he = [C_NI, C_FE, C_MN, C_TI, C_GOLD, "#8e44ad"]
    labels_he = ["Ni", "Fe", "Mn", "Ti", "Co", "Cu"]

    def lattice(ox, oy, colors, title, subtitle, ordered=False):
        ax.text(ox + 1.35, oy + 2.55, title, ha="center", fontsize=11, color=C_INK)
        ax.text(ox + 1.35, oy + 2.28, subtitle, ha="center", fontsize=8.2, color=C_MUTED)
        n = 6
        for i in range(n):
            for j in range(n):
                if ordered:
                    c = colors[(i + j) % len(colors)]
                else:
                    c = colors[rng.integers(0, len(colors))]
                ax.add_patch(Circle((ox + 0.28 + j * 0.42, oy + 0.25 + i * 0.32),
                                    0.14, facecolor=c, edgecolor="k", lw=0.4, zorder=3))

    lattice(0.3, 1.55, colors_order, "低熵有序", "空位有序 · 协同 JT", ordered=True)
    lattice(3.7, 1.55, colors_he, "中/高熵无序", r"S$_{\mathrm{config}}$ ↑  相变平滑", ordered=False)

    rounded(ax, 7.15, 1.55, 2.95, 2.55, "#fff", C_GOLD, lw=1.6, r=0.03)
    ax.text(8.62, 3.82, "2026 配方样本", ha="center", fontsize=10.5, color=C_GOLD)
    txt = (
        "高熵 O3\n"
        r"NaTi$_{0.2}$Mn$_{0.2}$Fe$_{0.2}$Ni$_{0.2}$Co$_{0.2}$O$_2$"
        "\n120 mAh g$^{-1}$ @ C/3"
        "\n\n中熵八元 O3/P2 双相"
        "\n非等摩尔压单相短板"
    )
    ax.text(8.62, 2.55, txt, ha="center", va="center", fontsize=8.3, color=C_INK, linespacing=1.45)

    ax.text(5.2, 0.75, "不同半径 / 价态 / M–O 共价性混在同一套八面体格点上",
            ha="center", fontsize=9.5, color=C_INK)

    legend = [("Ni", C_NI), ("Fe", C_FE), ("Mn", C_MN), ("Ti", C_TI), ("Co", C_GOLD), ("Cu/Mg", "#8e44ad")]
    for i, (lab, c) in enumerate(legend):
        ax.add_patch(Circle((1.1 + i * 1.45, 0.14), 0.09, facecolor=c, edgecolor="k", lw=0.4))
        ax.text(1.25 + i * 1.45, 0.14, lab, ha="left", va="center", fontsize=8, color=C_INK)
    save_fig(fig, "33_entropy_mix.png")


# ============================================================
# 34. O3@P2 核壳 / 外延
# ============================================================
def draw_34_core_shell():
    fig, ax = plt.subplots(figsize=(10.2, 5.2))
    ax.set_xlim(0, 10.2)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    ax.set_title("O3@P2：用棱柱外壳给八面体内核穿一件动力学铠甲",
                 fontsize=13, color=C_INK, pad=6)

    cx, cy = 2.35, 2.55
    ax.add_patch(Circle((cx, cy), 1.55, facecolor="#d5f5e3", edgecolor=C_P2, lw=2.4, zorder=2))
    ax.add_patch(Circle((cx, cy), 0.95, facecolor="#d4e6f1", edgecolor=C_O3, lw=2.4, zorder=3))
    ax.add_patch(Circle((cx, cy), 0.28, facecolor=C_NA, edgecolor="k", lw=0.8, zorder=4))
    ax.text(cx, cy + 0.02, "Na", ha="center", va="center", fontsize=8, zorder=5)
    ax.text(cx, cy + 1.78, "P2 外壳  三棱柱通道", ha="center", fontsize=9.5,
            color=C_P2)
    ax.text(cx, cy - 0.55, "O3 内核  高钠容量", ha="center", fontsize=9.5,
            color=C_O3)

    items = [
        (5.05, 3.85, C_O3, "O3 内核",
         "x ≈ 1 · 高库仑效率\n高能量密度"),
        (7.55, 3.85, C_P2, "P2 外壳",
         "低扩散垒\n隔空气 · 约束层滑"),
        (5.05, 1.85, C_GOLD, "Su & Chou, Chem. Sci. 2026",
         "混合熵 + 阳离子势\nO3 内核 @ P2 外壳"),
        (7.55, 1.85, C_ACCENT, "电化学数字",
         r"157.7 mAh g$^{-1}$ @ 0.1 C"
         "\n78.3 mAh g$^{-1}$ @ 10 C"),
    ]
    for x, y, c, t, b in items:
        rounded(ax, x, y - 1.15, 2.35, 1.45, "#fff", c, lw=1.6, r=0.03)
        ax.text(x + 1.175, y + 0.08, t, ha="center", fontsize=9.3, color=c)
        ax.text(x + 1.175, y - 0.55, b, ha="center", va="center", fontsize=8.1,
                color=C_INK, linespacing=1.4)
    save_fig(fig, "34_o3p2_core_shell.png")


# ============================================================
# 35. P2/O3 互锁与近零应变
# ============================================================
def draw_35_interlock():
    fig, ax = plt.subplots(figsize=(10.4, 5.1))
    ax.set_xlim(0, 10.4)
    ax.set_ylim(0, 5.1)
    ax.axis("off")
    ax.set_title("互锁双相：两套堆垛互相卡住，层滑移走不成一条直线",
                 fontsize=13, color=C_INK, pad=6)

    def brick_row(ax, y, offset, color, n=8, w=0.7, h=0.38):
        for i in range(n):
            x = 0.35 + offset + i * (w + 0.06)
            rounded(ax, x, y, w, h, color, "#1c2430", lw=0.7, r=0.01, z=3)

    brick_row(ax, 3.55, 0.00, "#a9cce3")
    brick_row(ax, 3.08, 0.22, "#a9dfbf")
    brick_row(ax, 2.61, 0.00, "#a9cce3")
    brick_row(ax, 2.14, 0.22, "#a9dfbf")
    ax.text(3.3, 4.12, "原子尺度共生长  P2（绿）/ O3（蓝）", ha="center",
            fontsize=10, color=C_INK)
    ax.annotate("", xy=(6.55, 2.9), xytext=(6.15, 2.9),
                arrowprops=dict(arrowstyle="-|>", color=C_INK, lw=1.8))

    rounded(ax, 6.7, 2.05, 3.4, 2.35, "#fff", C_P2, lw=1.6, r=0.03)
    ax.text(8.4, 4.1, "2026 两条定量边界", ha="center", fontsize=10.2,
            color=C_P2)
    ax.text(8.4, 3.15,
            "DFT 热力学边界：\n钠富 O3 相 < 20%\n可近零应变长循环\n\n"
            "最优互锁比：\n82.45% P2 + 17.55% O3",
            ha="center", va="center", fontsize=8.6, color=C_INK, linespacing=1.38)

    ax.text(5.2, 1.05, "P2 板滑成 O2 需整层平移，界面错配把滑移按住",
            ha="center", fontsize=9.2, color=C_INK)
    save_fig(fig, "35_interlock_p2o3.png")


# ============================================================
# 36. Al/Ti 键合工程
# ============================================================
def draw_36_bonding():
    fig, axes = plt.subplots(1, 3, figsize=(11.0, 4.6))

    def octa(ax, stretch=1.0, color=C_TM, title="", note=""):
        ax.set_xlim(-1.7, 1.7)
        ax.set_ylim(-1.85, 1.7)
        ax.set_aspect("equal")
        ax.axis("off")
        pts = [(1, 0), (0, 1 * stretch), (-1, 0), (0, -1 * stretch)]
        ax.plot([1, 0, -1, 0, 1], [0, stretch, 0, -stretch, 0], color=color, lw=1.6)
        ax.plot([-0.7, 0.7], [0.55 * stretch, -0.55 * stretch], color=color, lw=1.0, ls=":")
        ax.plot([-0.7, 0.7], [-0.55 * stretch, 0.55 * stretch], color=color, lw=1.0, ls=":")
        ax.add_patch(Circle((0, 0), 0.22, facecolor=color, edgecolor="k", lw=0.7, zorder=5))
        for x, y in [(1.15, 0), (-1.15, 0), (0, 1.18 * stretch), (0, -1.18 * stretch),
                     (0.72, 0.62 * stretch), (-0.72, -0.62 * stretch)]:
            ax.add_patch(Circle((x * 0.95, y * 0.85), 0.16, facecolor=C_O, edgecolor="k",
                                lw=0.5, zorder=4))
        ax.set_title(title, fontsize=10.5, color=color, pad=4)
        ax.text(0, -1.72, note, ha="center", va="top", fontsize=8.2, color=C_INK, linespacing=1.3)

    octa(axes[0], 1.35, C_MN, r"未掺杂 NFM：JT 拉长",
         r"Mn$^{3+}$/Fe$^{4+}$ e$_g^1$" "\n轴向 M–O 拉开\n层滑 + 开裂")
    octa(axes[1], 1.05, C_AL, r"Al 掺杂：钉氧",
         r"Al$^{3+}$ (d$^0$) 不 JT" "\nAl–O 短而硬\n剪断协同链")
    octa(axes[2], 1.12, C_TI, r"Ti 掺杂：弹簧缓冲",
         "Ti–O 强共价\n撑开层间距\n弹回相变应力")

    fig.suptitle(r"Hou et al., ACS Appl. Mater. Interfaces 2026  ·  10 C = 102.4 mAh g$^{-1}$",
                 fontsize=10.5, color=C_INK, y=0.02)
    plt.tight_layout(rect=[0, 0.08, 1, 1])
    save_fig(fig, "36_alti_bonding.png")


# ============================================================
# 37. 阴离子掺杂双参数准则
# ============================================================
def draw_37_anion():
    fig, ax = plt.subplots(figsize=(10.6, 5.6))
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 5.6)
    ax.axis("off")
    ax.set_title("阴离子掺杂的双参数准则（兰州大学，Adv. Mater. 2026）",
                 fontsize=13.2, color=C_INK, pad=6)

    rounded(ax, 0.3, 3.15, 4.9, 2.05, "#eafaf1", C_F, lw=1.8, r=0.03)
    ax.text(2.75, 4.88, "参数 1 · 价电子构型", ha="center", fontsize=11,
            color=C_F)
    ax.text(2.75, 4.05,
            r"F$^-$：给体 → 补给 Fe$^{3+}$" "\n抑制 Fe$^{4+}$ 与姜-泰勒\n\n"
            r"N$^{3-}$：受体 → 抽 Ni$^{2+}$" "\n助长 Ni$^{3+}$，空气更差",
            ha="center", va="center", fontsize=9, color=C_INK, linespacing=1.5)

    rounded(ax, 5.4, 3.15, 4.9, 2.05, "#f5eef8", C_N, lw=1.8, r=0.03)
    ax.text(7.85, 4.88, "参数 2 · 离子半径匹配", ha="center", fontsize=11,
            color=C_N)
    ax.text(7.85, 4.05,
            r"O$^{2-}$ ≈ 1.40 Å，阴离子须坐氧位" "\n"
            r"Cl$^-$ / Br$^-$ 太大：脱钠坍塌" "\n"
            r"B$^{3-}$ 双重失配：跨层振荡",
            ha="center", va="center", fontsize=9, color=C_INK, linespacing=1.5)

    # matrix
    ax.text(5.3, 2.85, "双参数决策表", ha="center", fontsize=10.5)
    headers = ["掺杂剂", "半径 vs O", "电子角色", "化学后果"]
    rows = [
        ["F−", "匹配", "给体", "抑 Fe4+ · 抗空气"],
        ["N3−", "大致匹配", "受体", "促 Ni3+ · 结构退化"],
        ["Cl−, Br−", "过大", "—", "脱钠坍塌"],
        ["B3−", "双重失配", "—", "跨层振荡"],
    ]
    xs = [0.45, 2.35, 4.35, 6.45]
    widths = [1.8, 1.9, 2.0, 3.7]
    y0 = 2.42
    for i, h in enumerate(headers):
        ax.add_patch(Rectangle((xs[i], y0), widths[i], 0.32, facecolor=C_O3, zorder=3))
        ax.text(xs[i] + widths[i] / 2, y0 + 0.16, h, ha="center", va="center",
                color="white", fontsize=8.6, zorder=4)
    pal = ["#eafaf1", "#fdebd0", "#fadbd8", "#fadbd8"]
    for r, row in enumerate(rows):
        y = y0 - 0.36 * (r + 1)
        for i, cell in enumerate(row):
            ax.add_patch(Rectangle((xs[i], y), widths[i], 0.36, facecolor=pal[r],
                                   edgecolor="#d5d8dc", lw=0.6, zorder=3))
            ax.text(xs[i] + widths[i] / 2, y + 0.18, cell, ha="center", va="center",
                    fontsize=8.3, color=C_INK, zorder=4)

    ax.text(5.3, 0.28, r"模型材料：O3-Na(NiFeMn)$_{1/3}$O$_2$　·　Bai et al., Advanced Materials, 22 Aug 2026",
            ha="center", fontsize=8.6, color=C_MUTED)
    save_fig(fig, "37_anion_dual.png")


# ============================================================
# 38. 氧阴离子氧化还原
# ============================================================
def draw_38_oxygen():
    fig, ax = plt.subplots(figsize=(10.4, 5.2))
    ax.set_xlim(0, 10.4)
    ax.set_ylim(0, 5.2)
    ax.axis("off")
    ax.set_title("氧阴离子氧化还原：额外容量来自 O 2p，风险也来自 O 2p",
                 fontsize=13, color=C_INK, pad=6)

    # orbital energy
    ax.text(2.35, 4.7, "能级图（示意）", ha="center", fontsize=10.5)
    ax.plot([0.7, 4.0], [3.85, 3.85], color=C_NI, lw=3)
    ax.text(4.15, 3.85, r"TM 3d  (e$_g$)", ha="left", va="center", fontsize=9, color=C_NI)
    ax.plot([0.7, 4.0], [2.55, 2.55], color=C_O, lw=3)
    ax.text(4.15, 2.55, r"O 2p  价带顶", ha="left", va="center", fontsize=9, color=C_O)
    ax.plot([0.7, 4.0], [1.55, 1.55], color=C_O3, lw=3)
    ax.text(4.15, 1.55, r"TM 3d  (t$_{2g}$)", ha="left", va="center", fontsize=9, color=C_O3)
    ax.annotate("", xy=(1.05, 3.85), xytext=(1.05, 2.55),
                arrowprops=dict(arrowstyle="<->", color=C_ACCENT, lw=1.5))
    ax.text(1.2, 3.2, "电荷转移能隙", fontsize=8, color=C_ACCENT)
    ax.annotate("先抽谁？", xy=(2.35, 3.2), xytext=(2.7, 4.25),
                fontsize=8.2, color=C_INK,
                arrowprops=dict(arrowstyle="-|>", color=C_INK, lw=1.1))

    rounded(ax, 6.05, 2.55, 4.05, 2.3, "#fff", C_O, lw=1.7, r=0.03)
    ax.text(8.07, 4.55, "可逆 vs 不可逆", ha="center", fontsize=10.5, color=C_O)
    ax.text(8.07, 3.55,
            "可逆：空穴被邻近 TM 钉住\n过氧对，放电还回去\n\n"
            "不可逆：空穴离域 → O2 逸出\nTM 迁入钠层 → 岩盐死层",
            ha="center", va="center", fontsize=8.6, color=C_INK, linespacing=1.45)

    rounded(ax, 0.35, 0.25, 9.7, 1.1, "#fef9e7", C_GOLD, lw=1.4, r=0.02)
    ax.text(5.2, 0.8,
            "IEC Res. 2026　K/Cu/Zr 共掺调 O 2p 价带\n"
            "体积应变 1.23% → 0.45%　·　800 圈保持 78.6%",
            ha="center", va="center", fontsize=9, color=C_INK, linespacing=1.4)
    save_fig(fig, "38_oxygen_redox.png")


# ============================================================
# 39. 尖晶石异质结
# ============================================================
def draw_39_spinel():
    fig, ax = plt.subplots(figsize=(10.2, 4.9))
    ax.set_xlim(0, 10.2)
    ax.set_ylim(0, 4.9)
    ax.axis("off")
    ax.set_title("层状 / 尖晶石异质结：三维通道给二维层状当支柱",
                 fontsize=13, color=C_INK, pad=6)

    for i, y in enumerate([3.55, 3.05, 2.55, 2.05]):
        ax.add_patch(Rectangle((0.4, y), 3.3, 0.38,
                               facecolor="#d4e6f1" if i % 2 == 0 else "#fdebd0",
                               edgecolor=C_O3, lw=1.1))
    ax.text(2.05, 4.15, "层状 Na$_x$TMO$_2$", ha="center", fontsize=10.5,
            color=C_O3)
    ax.text(2.05, 1.75, "二维 Na 扩散  ·  易层滑", ha="center", fontsize=8.4, color=C_MUTED)

    ax.annotate("", xy=(4.55, 3.0), xytext=(3.9, 3.0),
                arrowprops=dict(arrowstyle="-|>", lw=2, color=C_INK))

    # spinel schematic 3x3
    cx, cy = 6.35, 3.05
    for i in range(3):
        for j in range(3):
            ax.add_patch(Rectangle((cx + j * 0.42, cy + i * 0.42), 0.38, 0.38,
                                   facecolor="#d5f5e3", edgecolor=C_P2, lw=1.0))
            ax.add_patch(Circle((cx + 0.19 + j * 0.42, cy + 0.19 + i * 0.42), 0.07,
                                facecolor=C_TM, edgecolor="k", lw=0.3))
    ax.text(6.95, 4.15, "尖晶石 AB$_2$O$_4$", ha="center", fontsize=10.5,
            color=C_P2)
    ax.text(6.95, 1.75, "三维通道  ·  机械钉扎", ha="center", fontsize=8.4, color=C_MUTED)

    rounded(ax, 8.15, 1.7, 1.85, 2.55, "#fff", C_GOLD, lw=1.5, r=0.03)
    ax.text(9.07, 3.95, "三种做法", ha="center", fontsize=9.5, color=C_GOLD)
    ax.text(9.07, 2.85, "体相复合\n\n表面亚层\n\n完整包覆",
            ha="center", va="center", fontsize=9, color=C_INK, linespacing=1.25)

    ax.text(5.1, 0.65,
            "氧密堆积骨架连续，界面可以共格",
            ha="center", fontsize=9.6, color=C_INK)
    save_fig(fig, "39_spinel_hetero.png")


# ============================================================
# 40. 空气与残碱表面化学
# ============================================================
def draw_40_air():
    fig, ax = plt.subplots(figsize=(10.4, 5.0))
    ax.set_xlim(0, 10.4)
    ax.set_ylim(0, 5.0)
    ax.axis("off")
    ax.set_title("空气化学：O3 表面的残碱从哪里来，2026 年怎么拆",
                 fontsize=13, color=C_INK, pad=6)

    steps = [
        (0.3, C_O3, "1. 吸水", "NaTMO2 + H2O\n→ NaOH + 质子化层"),
        (2.85, C_ACCENT, "2. 吸 CO2", "NaOH + CO2\n→ Na2CO3 / NaHCO3"),
        (5.4, "#6c3483", "3. 浆料凝胶", "残碱吃 PVDF\n阻抗涨、颗粒蚀刻"),
        (7.95, C_P2, "4. 破解", "丙二酸中和残碱\n生成丙酸钠保护膜"),
    ]
    for x, c, t, b in steps:
        rounded(ax, x, 2.55, 2.35, 2.05, "#fff", c, lw=1.8, r=0.03)
        ax.add_patch(Rectangle((x, 4.18), 2.35, 0.42, facecolor=c, zorder=3))
        ax.text(x + 1.175, 4.39, t, ha="center", va="center", color="white",
                fontsize=10.5, zorder=4)
        ax.text(x + 1.175, 3.35, b, ha="center", va="center", fontsize=8.8,
                color=C_INK, linespacing=1.45)
    for x in [2.55, 5.1, 7.65]:
        ax.annotate("", xy=(x + 0.25, 3.55), xytext=(x - 0.05, 3.55),
                    arrowprops=dict(arrowstyle="-|>", color=C_INK, lw=1.6))

    rounded(ax, 0.3, 0.25, 9.8, 2.05, "#f4f0e6", C_GOLD, lw=1.4, r=0.02)
    ax.text(5.2, 1.85, "Xie et al., J. Power Sources 2026　·　0.3 wt% 丙二酸（C3）中和残碱",
            ha="center", fontsize=10.2, color=C_INK)
    ax.text(5.2, 0.95,
            "2.0–4.0 V：120 圈 79% → 89%　·　2 C：95 → 110 mAh g−1\n"
            "XRD 体相不变，SEM 表面蚀刻减轻",
            ha="center", va="center", fontsize=9, color=C_INK, linespacing=1.5)
    save_fig(fig, "40_air_surface.png")


# ============================================================
# 41. NM55 相变瀑布
# ============================================================
def draw_41_cascade():
    fig, ax = plt.subplots(figsize=(11.0, 4.6))
    ax.set_xlim(0, 11.0)
    ax.set_ylim(0, 4.6)
    ax.axis("off")
    ax.set_title(r"O3-NaNi$_{0.5}$Mn$_{0.5}$O$_2$ 的相变瀑布（上海科技大学 2026 原位 XRD）",
                 fontsize=12.8, color=C_INK, pad=4)

    phases = [
        ("O3", C_O3, "六方\n高钠"),
        ("O′3", "#5dade2", "单斜\nJT 畸变"),
        ("P′3", "#58d68d", "单斜棱柱"),
        ("P3", C_P2, "六方棱柱"),
        ("P′3′", "#52be80", "再畸变"),
        ("P3′", "#1e8449", "高脱钠\n棱柱"),
        ("O3′/O3′′", C_ACCENT, "高 SOC\n两相"),
    ]
    xs = np.linspace(0.45, 9.7, len(phases))
    for x, (name, c, note) in zip(xs, phases):
        ax.add_patch(Circle((x, 2.85), 0.52, facecolor=c, edgecolor="k", lw=0.8, zorder=3))
        ax.text(x, 2.85, name, ha="center", va="center", color="white",
                fontsize=9.2, zorder=4)
        ax.text(x, 2.05, note, ha="center", va="top", fontsize=7.8, color=C_INK)
    for i in range(len(xs) - 1):
        ax.annotate("", xy=(xs[i + 1] - 0.55, 2.85), xytext=(xs[i] + 0.55, 2.85),
                    arrowprops=dict(arrowstyle="-|>", color=C_INK, lw=1.4))

    ax.annotate("", xy=(10.55, 2.85), xytext=(0.2, 2.85),
                arrowprops=dict(arrowstyle="-|>", color="#d5d8dc", lw=0.0))
    ax.text(5.5, 3.7, "充电 / 脱钠  →", ha="center", fontsize=10, color=C_MUTED)

    rounded(ax, 0.35, 0.2, 10.3, 1.45, "#fff", C_GOLD, lw=1.5, r=0.02)
    ax.text(5.5, 1.28, "结构破坏分两段，对应两套处方",
            ha="center", fontsize=10, color=C_INK)
    ax.text(5.5, 0.65,
            "低 SOC：单斜畸变 + 空位有序 → Fe 抑制、Ti 关掉\n"
            "高 SOC：O3′/O3′′ 两相失配 → Fe 改固溶、Ca2+ 撑钠层\n"
            "NFM424-Ti2.5Ca2 全电池 1 C / 600 圈：24% → 70%",
            ha="center", va="center", fontsize=8.6, color=C_INK, linespacing=1.5)
    save_fig(fig, "41_nm55_cascade.png")


# ============================================================
# 42. 2026 策略雷达 / 路线图
# ============================================================
def draw_42_roadmap():
    fig, ax = plt.subplots(figsize=(10.6, 6.0), subplot_kw=dict(polar=True))

    labels = ["容量", "倍率", "循环", "空气稳定", "高电压可逆", "成本/无钴"]
    N = len(labels)
    ang = np.linspace(0, 2 * np.pi, N, endpoint=False)

    series = {
        "纯 O3-NFM": np.array([0.82, 0.45, 0.40, 0.28, 0.32, 0.88]),
        "纯 P2-NNM": np.array([0.55, 0.85, 0.50, 0.62, 0.38, 0.80]),
        "2026 熵+双相+钉氧": np.array([0.78, 0.82, 0.84, 0.75, 0.72, 0.70]),
    }
    colors = {"纯 O3-NFM": C_O3, "纯 P2-NNM": C_P2, "2026 熵+双相+钉氧": C_ACCENT}

    ang_c = np.concatenate([ang, ang[:1]])
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(ang), labels, fontsize=10)
    ax.set_ylim(0, 1.0)
    ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["", "0.5", "0.75", "1"], fontsize=8, color=C_MUTED)
    ax.grid(color="#d5d8dc", lw=0.7)

    for name, vals in series.items():
        v = np.concatenate([vals, vals[:1]])
        ax.plot(ang_c, v, color=colors[name], lw=2.2, label=name)
        ax.fill(ang_c, v, color=colors[name], alpha=0.12)

    ax.legend(loc="upper right", bbox_to_anchor=(1.28, 1.12), frameon=False, fontsize=9)
    ax.set_title("化学策略把短板补齐：2026 年的层状正极不再赌单相",
                 fontsize=12.5, color=C_INK, pad=18)
    save_fig(fig, "42_strategy_radar.png")


# ============================================================
# 43. 速记海报
# ============================================================
def draw_43_poster():
    fig, ax = plt.subplots(figsize=(10.6, 6.2))
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 6.2)
    ax.axis("off")
    rounded(ax, 0.15, 0.15, 10.3, 5.9, "#fffbeb", C_GOLD, lw=2.2, r=0.02)
    ax.text(5.3, 5.65, "2026 钠电层状正极 · 化学速记", ha="center",
            fontsize=16, color="#7d4e00")
    ax.text(5.3, 5.25, "容量是电子账，寿命是骨架账，空气是表面账",
            ha="center", fontsize=10.5, color=C_INK)

    cards = [
        (0.4, 3.35, C_O3, "电子从哪来",
         "Ni 给电压\nFe 给容量也给 JT\nMn 给骨架\nO 2p 给额外容量"),
        (3.75, 3.35, C_P2, "骨架怎么坏",
         "O3→P3 层滑\nP2→O2 / OP4\n4.0 V O/P 杂化坍塌\n协同姜-泰勒"),
        (7.1, 3.35, C_ACCENT, "2026 怎么修",
         "熵：打散有序\n双相互锁：O3 < 20%\nAl/Ti 钉氧 + 弹簧\nF 给电子"),
    ]
    for x, y, c, t, b in cards:
        rounded(ax, x, y, 3.1, 1.7, "#fff", c, lw=1.7, r=0.03)
        ax.add_patch(Rectangle((x, y + 1.32), 3.1, 0.38, facecolor=c, zorder=3))
        ax.text(x + 1.55, y + 1.51, t, ha="center", va="center", color="white",
                fontsize=11, zorder=4)
        ax.text(x + 1.55, y + 0.62, b, ha="center", va="center", fontsize=8.6,
                color=C_INK, linespacing=1.45)

    ax.text(5.3, 2.95, "一条设计闭环（按化学优先级）", ha="center",
            fontsize=11, color=C_INK)
    loop = [
        (0.45, "1 选氧化还原\n窗口"),
        (2.45, "2 钉氧\nAl/Ti/Zr/F"),
        (4.45, "3 剪协同\n熵 + 半径失配"),
        (6.45, "4 锁层滑\n双相 / 尖晶石"),
        (8.45, "5 清表面\n残碱中和"),
    ]
    for x, t in loop:
        rounded(ax, x, 1.55, 1.75, 1.15, "#fff", C_GOLD, lw=1.3, r=0.03)
        ax.text(x + 0.875, 2.12, t, ha="center", va="center", fontsize=8.6, color=C_INK)
    for x in [2.2, 4.2, 6.2, 8.2]:
        ax.annotate("", xy=(x + 0.22, 2.12), xytext=(x - 0.05, 2.12),
                    arrowprops=dict(arrowstyle="-|>", color=C_GOLD, lw=1.5))

    ax.text(5.3, 0.95, "文献 2026：Ye JES · Su ChemSci · Hou ACS AMI · Bai AdvMater · Kang JEC · Li ELett · Xie JPS",
            ha="center", fontsize=8.2, color=C_MUTED)
    ax.text(5.3, 0.5, "口诀：少造 eg1，钉住氧，卡住层，洗净碱。",
            ha="center", fontsize=11.5, color="#7d4e00")
    save_fig(fig, "43_poster_2026.png")


def main():
    print("=" * 60)
    print("[*] 生成 2026 钠电层状正极化学视角插图")
    print("=" * 60)
    draw_30_map()
    draw_31_redox()
    draw_32_collapse()
    draw_33_entropy()
    draw_34_core_shell()
    draw_35_interlock()
    draw_36_bonding()
    draw_37_anion()
    draw_38_oxygen()
    draw_39_spinel()
    draw_40_air()
    draw_41_cascade()
    draw_42_roadmap()
    draw_43_poster()
    print("=" * 60)
    print(f"[SUCCESS] 14 张图已输出到 {OUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
