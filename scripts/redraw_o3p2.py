# -*- coding: utf-8 -*-
"""
O3 / P2 / 八面体 / 三棱柱 全套结构图重绘。
构图从氧层几何出发，不沿用旧版线框、表格与正弦能垒。
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
    FancyArrow, Arc, Wedge, Ellipse, RegularPolygon,
)
from matplotlib.collections import LineCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Line3DCollection

for fp in (
    "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
):
    if os.path.exists(fp):
        fm.fontManager.addfont(fp)

mpl.rcParams["font.sans-serif"] = ["WenQuanYi Micro Hei", "DejaVu Sans"]
mpl.rcParams["axes.unicode_minus"] = False
mpl.rcParams["savefig.dpi"] = 230
mpl.rcParams["savefig.bbox"] = "tight"
mpl.rcParams["mathtext.fontset"] = "dejavusans"

O3 = "#1d4e89"
P2 = "#2d6a4f"
NA = "#e6a817"
TM = "#1aa38a"
OX = "#d64545"
INK = "#1c2430"
MUTED = "#5c6570"
GOLD = "#b8860b"
ACC = "#c0392b"
PAPER = "#ffffff"
CREAM = "#fbf7f0"
LINE = "#e2d8c8"

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "images"))
os.makedirs(OUT, exist_ok=True)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name), facecolor=PAPER, edgecolor="none")
    plt.close(fig)
    print("[OK]", name)


def box(ax, x, y, w, h, fc, ec, lw=1.5, r=0.02, z=2, alpha=1):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad={r}",
                       facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z, alpha=alpha)
    ax.add_patch(p)
    return p


def arr(ax, a, b, color=INK, lw=1.6, ms=11, rad=0, style="-|>"):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle=style, mutation_scale=ms,
                                 lw=lw, color=color, connectionstyle=f"arc3,rad={rad}", zorder=5))


def tri(ang0=np.pi / 6, r=1.0, z=0.9):
    a = ang0 + np.array([0, 2 * np.pi / 3, 4 * np.pi / 3])
    return np.column_stack([r * np.cos(a), r * np.sin(a), np.full(3, z)])


# ============================================================
# 01  两种笼子：两枚氧三角怎么围出 NaO6
# ============================================================
def draw_01():
    fig = plt.figure(figsize=(10.8, 5.2))

    def cage(ax, eclipsed, title, color):
        ax.set_xlim(-1.15, 1.15)
        ax.set_ylim(-1.15, 1.15)
        ax.set_zlim(-1.05, 1.05)
        ax.set_box_aspect((1, 1, 0.92), zoom=1.25)
        ax.set_axis_off()
        ax.view_init(22, 28)
        for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
            pane.fill = False
            pane.set_edgecolor("none")
        top = tri(np.pi / 6, 1.0, 0.78)
        bot = tri(np.pi / 6 if eclipsed else np.pi / 6 + np.pi / 3, 1.0, -0.78)
        faces = [top, bot]
        if eclipsed:
            for i in range(3):
                j = (i + 1) % 3
                faces.append([top[i], top[j], bot[j], bot[i]])
        else:
            for i in range(3):
                faces.append([top[i], bot[i], bot[(i + 1) % 3]])
                faces.append([top[i], top[(i + 1) % 3], bot[(i + 1) % 3]])
        poly = Poly3DCollection(faces, alpha=0.32, facecolor=color,
                                edgecolor=color, linewidths=1.5)
        ax.add_collection3d(poly)
        for p in np.vstack([top, bot]):
            ax.scatter(*p, s=90, c=OX, edgecolors="k", lw=0.45, zorder=8)
            ax.plot([0, p[0]], [0, p[1]], [0, p[2]], color="#9aa3ad", lw=0.8, ls=":")
        ax.scatter(0, 0, 0, s=210, c=NA, edgecolors="k", lw=0.6, zorder=9)
        ax.text2D(0.5, 0.98, title, transform=ax.transAxes, ha="center", va="top",
                  fontsize=13, color=color)

    ax1 = fig.add_subplot(121, projection="3d")
    cage(ax1, False, "O · 八面体", O3)
    ax2 = fig.add_subplot(122, projection="3d")
    cage(ax2, True, "P · 三棱柱", P2)

    fig.suptitle(r"NaO$_6$：八面体与三棱柱", fontsize=14, color=INK, y=0.04)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.96, bottom=0.10, wspace=0.04)
    save(fig, "01_polyhedra.png")


# ============================================================
# 02  跳跃窗口：三角颈 vs 矩形门，带尺度标尺
# ============================================================
def draw_02():
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 5.0))

    ax = axes[0]
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.15, 2.05)
    ax.set_aspect("equal")
    ax.axis("off")
    t = np.array([[0, 1.45], [-1.28, -0.78], [1.28, -0.78]])
    ax.add_patch(Polygon(t, closed=True, fc="#dce6f2", ec=O3, lw=2.4, zorder=2))
    for p in t:
        ax.add_patch(Circle(p, 0.32, fc=OX, ec="k", lw=0.7, zorder=4))
    ax.add_patch(Circle((0, 0.12), 0.42, fc=NA, ec="k", lw=1.1, ls="--", zorder=5))
    ax.text(0, 0.12, r"Na$^+$", ha="center", va="center", fontsize=10, color=INK, zorder=6)
    arr(ax, (0, -0.45), (0, -1.48), O3, lw=2.0, ms=14)
    ax.set_title("O3 · 三角窗口", fontsize=12.5, color=O3, pad=8)
    ax.text(0, 1.80, r"$r \approx 1.05\ \mathrm{\AA}$    $E_a \sim 0.5\ \mathrm{eV}$",
            ha="center", fontsize=9.5, color=MUTED)

    ax = axes[1]
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.15, 2.05)
    ax.set_aspect("equal")
    ax.axis("off")
    r = np.array([[-1.05, -1.15], [1.05, -1.15], [1.05, 1.15], [-1.05, 1.15]])
    ax.add_patch(Polygon(r, closed=True, fc="#d7eee3", ec=P2, lw=2.4, zorder=2))
    for p in r:
        ax.add_patch(Circle(p, 0.32, fc=OX, ec="k", lw=0.7, zorder=4))
    ax.add_patch(Circle((0, 0), 0.50, fc=NA, ec="k", lw=1.1, zorder=5))
    ax.text(0, 0, r"Na$^+$", ha="center", va="center", fontsize=10, color=INK, zorder=6)
    arr(ax, (1.55, 0), (1.95, 0), P2, lw=2.0, ms=14)
    ax.set_title("P2 · 矩形窗口", fontsize=12.5, color=P2, pad=8)
    ax.text(0, 1.80, r"$r \approx 1.35\ \mathrm{\AA}$    $E_a \sim 0.25\ \mathrm{eV}$",
            ha="center", fontsize=9.5, color=MUTED)
    plt.tight_layout(rect=[0, 0.06, 1, 1])
    save(fig, "02_hop_windows.png")


# ============================================================
# 10  通式：三层千层饼
# ============================================================
def draw_10():
    fig, ax = plt.subplots(figsize=(10.4, 4.8))
    ax.set_xlim(0, 10.4)
    ax.set_ylim(0, 4.8)
    ax.axis("off")
    ax.set_title(r"Na$_x$TMO$_2$  三块积木", fontsize=14, color=INK, pad=6)

    def layer_row(y, n, color, r, x0=1.35, gap=0.72, jitter=0.0):
        xs = x0 + np.arange(n) * gap + jitter
        ax.scatter(xs, [y] * n, s=r, c=color, edgecolors="k", lw=0.45, zorder=4)
        return xs

    layer_row(4.05, 9, OX, 90, jitter=0.00)
    layer_row(3.55, 7, TM, 130, x0=1.70)
    layer_row(3.05, 9, OX, 90, jitter=0.36)
    layer_row(2.45, 6, NA, 170, x0=2.05)
    layer_row(1.85, 9, OX, 90, jitter=0.00)
    layer_row(1.35, 7, TM, 130, x0=1.70)
    layer_row(0.85, 9, OX, 90, jitter=0.36)

    ax.annotate("", xy=(8.15, 0.75), xytext=(8.15, 4.15),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.6))
    ax.text(8.35, 2.45, "c 轴", fontsize=10, color=INK, va="center")

    for y, c, t in [(3.75, NA, r"Na$_x$"), (2.45, TM, "TM"), (1.15, OX, r"O$_2$")]:
        ax.scatter([8.85], [y], s=230, c=c, edgecolors="k", lw=0.5, zorder=5)
        ax.text(9.15, y, t, ha="left", va="center", fontsize=13, color=c)
    save(fig, "10_formula.png")


# ============================================================
# 03  O3 侧视：ABC 错开的三明治
# ============================================================
def draw_03():
    fig, ax = plt.subplots(figsize=(10.6, 5.6))
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 5.6)
    ax.axis("off")
    ax.set_title(r"O3  ·  氧层 ABCABC 交错  ·  钠坐进八面体空隙",
                 fontsize=13.2, color=O3, pad=4)

    # offset map
    off = {"A": 0.00, "B": 0.38, "C": 0.76}
    seq = [
        ("A", "O", OX, 90),
        ("B", "TM", TM, 125),
        ("C", "O", OX, 90),
        ("A", "Na", NA, 155),
        ("B", "O", OX, 90),
        ("C", "TM", TM, 125),
        ("A", "O", OX, 90),
        ("B", "Na", NA, 155),
        ("C", "O", OX, 90),
        ("A", "TM", TM, 125),
        ("B", "O", OX, 90),
        ("C", "Na", NA, 155),
    ]
    ys = np.linspace(5.15, 0.85, len(seq))
    for y, (let, kind, col, s) in zip(ys, seq):
        xs = 1.55 + off[let] + np.arange(8) * 0.62
        ax.scatter(xs, [y] * 8, s=s, c=col, edgecolors="k", lw=0.35, zorder=4)
        ax.text(0.85, y, f"{let}  {kind}", ha="right", va="center",
                fontsize=8.6, color=col)
    ax.annotate("", xy=(7.35, 0.85), xytext=(7.35, 5.15),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.7))
    ax.text(7.55, 3.0, "周期\n3 层 TM", va="center", fontsize=10, color=INK)
    save(fig, "03_o3_stacking.png")


# ============================================================
# 04  P2 侧视：ABBA 对齐
# ============================================================
def draw_04():
    fig, ax = plt.subplots(figsize=(10.6, 5.4))
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 5.4)
    ax.axis("off")
    ax.set_title(r"P2  ·  氧层 ABBA 对齐  ·  钠坐进三棱柱空隙",
                 fontsize=13.2, color=P2, pad=4)

    off = {"A": 0.00, "B": 0.38}
    seq = [
        ("A", "O", OX, 90),
        (" ", "TM", TM, 125),
        ("B", "O", OX, 90),
        ("B", "Na", NA, 155),
        ("B", "O", OX, 90),
        (" ", "TM", TM, 125),
        ("A", "O", OX, 90),
        ("A", "Na", NA, 155),
        ("A", "O", OX, 90),
    ]
    # TM sits between A and B, no letter of its own
    ys = np.linspace(4.95, 0.85, len(seq))
    for y, (let, kind, col, s) in zip(ys, seq):
        jitter = off.get(let, 0.19)
        xs = 1.55 + jitter + np.arange(8) * 0.62
        ax.scatter(xs, [y] * 8, s=s, c=col, edgecolors="k", lw=0.35, zorder=4)
        label = f"{let}  {kind}" if let.strip() else f"    {kind}"
        ax.text(0.85, y, label, ha="right", va="center",
                fontsize=8.6, color=col)

    # alignment ticks on Na prism layers (BB and AA)
    for y in (ys[3], ys[7]):
        ax.plot([1.35, 6.55], [y, y], color=NA, lw=0.7, ls="--", alpha=0.5, zorder=2)
    ax.text(6.55, ys[3], "BB", va="center", fontsize=9.5, color=NA)
    ax.text(6.55, ys[7], "AA", va="center", fontsize=9.5, color=NA)

    ax.annotate("", xy=(7.35, 0.85), xytext=(7.35, 4.95),
                arrowprops=dict(arrowstyle="<->", color=INK, lw=1.7))
    ax.text(7.55, 2.9, "周期\n2 层 TM", va="center", fontsize=10, color=INK)
    save(fig, "04_p2_stacking.png")


# ============================================================
# 05  Delmas：字母是笼子，数字是步数
# ============================================================
def draw_05():
    fig, ax = plt.subplots(figsize=(10.6, 5.0))
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 5.0)
    ax.axis("off")
    ax.set_title("Delmas 记号  =  一个字母  +  一个数字",
                 fontsize=14, color=INK, pad=6)

    box(ax, 0.3, 1.55, 4.55, 3.05, "#eef3f9", O3, lw=1.8)
    ax.text(2.57, 4.25, "字母  ·  钠坐在什么笼子", ha="center",
            fontsize=11.5, color=O3)
    ax.text(1.4, 3.35, "O", ha="center", fontsize=28, color=O3)
    ax.text(1.4, 2.60, "八面体\n氧层交错", ha="center", fontsize=10, color=INK)
    ax.text(3.7, 3.35, "P", ha="center", fontsize=28, color=P2)
    ax.text(3.7, 2.60, "三棱柱\n氧层对齐", ha="center", fontsize=10, color=INK)
    ax.plot([2.55, 2.55], [1.75, 3.95], color=LINE, lw=1.2)

    box(ax, 5.15, 1.55, 5.15, 3.05, "#eef6f1", P2, lw=1.8)
    ax.text(7.72, 4.25, "数字  ·  几块 TMO$_2$ 走完一圈", ha="center",
            fontsize=11.5, color=P2)
    ax.text(6.55, 3.35, "3", ha="center", fontsize=28, color=O3)
    ax.text(6.55, 2.60, "A-B-C 三步\nO3 / P3", ha="center", fontsize=10, color=INK)
    ax.text(8.9, 3.35, "2", ha="center", fontsize=28, color=P2)
    ax.text(8.9, 2.60, "A-B 折返\nP2 / O2", ha="center", fontsize=10, color=INK)
    ax.plot([7.72, 7.72], [1.75, 3.95], color=LINE, lw=1.2)

    ax.text(5.3, 0.72, "O3 = 八面体 · 3 层 TM      P2 = 三棱柱 · 2 层 TM",
            ha="center", fontsize=11, color=INK)
    save(fig, "05_delmas.png")


# ============================================================
# 06  P2 两种钠位：俯视蜂窝
# ============================================================
def draw_06():
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 5.1))

    def hex_lattice(ax, highlight="e"):
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_xlim(-2.55, 2.55)
        ax.set_ylim(-2.30, 2.55)
        a = 1.05
        tms = []
        for i in range(-2, 3):
            for j in range(-2, 3):
                x = a * (i + 0.5 * j)
                y = a * (np.sqrt(3) / 2) * j
                if abs(x) < 2.2 and abs(y) < 1.95:
                    tms.append((x, y))
                    ax.add_patch(Circle((x, y), 0.20, fc=TM, ec="k", lw=0.45, zorder=3))
        if highlight == "e":
            left, right = (-a, 0.0), (0.0, 0.0)
            mid = ((left[0] + right[0]) / 2, 0.0)
            ax.plot([left[0], right[0]], [0, 0], color=O3, lw=2.6, zorder=4)
            ax.add_patch(Circle(left, 0.20, fc=TM, ec=O3, lw=1.2, zorder=5))
            ax.add_patch(Circle(right, 0.20, fc=TM, ec=O3, lw=1.2, zorder=5))
            ax.add_patch(Circle(mid, 0.28, fc=NA, ec="k", lw=1.05, zorder=6))
            ax.text(mid[0], -1.95, r"Na$_e$  共棱", ha="center", fontsize=10.5, color=O3)
            ax.set_title(r"Na$_e$ · 边共享", fontsize=12.5, color=O3, pad=6)
        else:
            ax.add_patch(Circle((0, 0), 0.20, fc=TM, ec=ACC, lw=1.2, zorder=5))
            ax.add_patch(Circle((0, 0), 0.58, fill=False, ec=ACC, lw=1.5, ls="--", zorder=4))
            ax.add_patch(Circle((0, 0.42), 0.28, fc=NA, ec="k", lw=1.05, zorder=6))
            ax.plot([0, 0], [0.18, 0.22], color=ACC, lw=0.8, zorder=4)
            ax.text(0, -1.95, r"Na$_f$  面共享", ha="center", fontsize=10.5, color=ACC)
            ax.set_title(r"Na$_f$ · 面共享", fontsize=12.5, color=ACC, pad=6)

    hex_lattice(axes[0], "e")
    hex_lattice(axes[1], "f")
    fig.suptitle("P2 层内两套三棱柱位", fontsize=13.5, color=INK, y=0.02)
    plt.tight_layout(rect=[0, 0.06, 1, 1])
    save(fig, "06_p2_na_sites.png")


# ============================================================
# 07  扩散：路径卡通 + 能垒
# ============================================================
def draw_07():
    fig = plt.figure(figsize=(10.8, 5.6))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.15, 1.0], hspace=0.38, wspace=0.18)

    ax = fig.add_subplot(gs[0, 0])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")
    ax.set_title("O3  绕路  Oh → Td → Oh", fontsize=11.5, color=O3)
    sites = [(1.5, 2.0, "Oh"), (5.0, 2.0, "Td"), (8.5, 2.0, "Oh")]
    cols = [O3, ACC, O3]
    sizes = [1.15, 0.72, 1.15]
    for (x, y, lab), c, s in zip(sites, cols, sizes):
        ax.add_patch(RegularPolygon((x, y), 6 if lab == "Oh" else 3, radius=s,
                                    orientation=np.pi / 6 if lab == "Oh" else 0,
                                    fc="#dce6f2" if lab == "Oh" else "#fdebd0",
                                    ec=c, lw=2, zorder=3))
        ax.text(x, y, lab, ha="center", va="center", fontsize=11, color=c)
    arr(ax, (2.7, 2.0), (4.15, 2.0), O3, lw=1.8)
    arr(ax, (5.85, 2.0), (7.3, 2.0), O3, lw=1.8)
    ax.text(5.0, 0.55, "四面体小", ha="center", fontsize=9, color=MUTED)

    ax = fig.add_subplot(gs[0, 1])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis("off")
    ax.set_title("P2  直通  Prism → Prism", fontsize=11.5, color=P2)
    for x, lab in ((2.3, "Prism"), (7.7, "Prism")):
        ax.add_patch(Rectangle((x - 1.15, 1.15), 2.3, 1.8, fc="#d7eee3", ec=P2, lw=2, zorder=3))
        ax.text(x, 2.05, lab, ha="center", va="center", fontsize=11, color=P2)
    arr(ax, (3.6, 2.05), (6.4, 2.05), P2, lw=1.8)
    ax.text(5.0, 3.35, "矩形窗", ha="center", fontsize=9, color=P2)
    ax.text(5.0, 0.55, "层内面共享", ha="center", fontsize=9, color=MUTED)

    ax = fig.add_subplot(gs[1, :])
    x = np.linspace(0, 1, 300)
    y_o3 = 0.55 * np.exp(-((x - 0.5) ** 2) / (2 * 0.045 ** 2))
    y_p2 = 0.24 * np.exp(-((x - 0.5) ** 2) / (2 * 0.07 ** 2))
    ax.plot(x, y_o3, color=O3, lw=2.6, label=r"O3   $E_a \approx 0.55$ eV")
    ax.plot(x, y_p2, color=P2, lw=2.6, label=r"P2   $E_a \approx 0.24$ eV")
    ax.fill_between(x, y_o3, alpha=0.10, color=O3)
    ax.fill_between(x, y_p2, alpha=0.10, color=P2)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.72)
    ax.set_yticks([0, 0.24, 0.55])
    ax.set_ylabel("能垒 / eV", fontsize=10)
    ax.set_xlabel("跳跃反应坐标", fontsize=10)
    ax.legend(frameon=False, fontsize=10, loc="upper right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", ls="--", alpha=0.35)
    save(fig, "07_diffusion.png")


# ============================================================
# 08  相变：板在滑
# ============================================================
def draw_08():
    fig, axes = plt.subplots(2, 3, figsize=(10.8, 5.4))

    def slabs(ax, shifts, title, color, caption):
        ax.set_xlim(-0.2, 4.4)
        ax.set_ylim(-0.3, 3.3)
        ax.axis("off")
        ax.set_title(title, fontsize=10.5, color=color)
        ys = [0.35, 1.15, 1.95, 2.75]
        fill = {O3: "#d4e6f1", P2: "#d5f5e3"}.get(color, "#fdecea")
        for y, sh in zip(ys, shifts):
            ax.add_patch(Rectangle((0.35 + sh, y), 3.3, 0.42,
                                   fc=fill, ec=color, lw=1.3, zorder=3))
            # Na dots
            ax.scatter(np.linspace(0.7 + sh, 3.3 + sh, 5), [y + 0.21] * 5,
                       s=18, c=NA, edgecolors="k", lw=0.2, zorder=4)
        ax.text(2.15, -0.15, caption, ha="center", fontsize=8.2, color=MUTED)

    slabs(axes[0, 0], [0, 0, 0, 0], "O3  满钠", O3, "ABC 交错，八面体钠")
    slabs(axes[0, 1], [0, 0.35, 0, 0.35], "→ P3  层滑", O3, "相邻板平移，钠变棱柱")
    slabs(axes[0, 2], [0, 0.55, 0.15, 0.70], "深脱钠  开裂风险", ACC, "应变累积，阻抗上升")

    slabs(axes[1, 0], [0, 0, 0, 0], "P2  缺钠", P2, "ABBA 对齐，通道宽")
    slabs(axes[1, 1], [0, 0.12, 0, 0.12], "中电压  固溶", P2, "多数区间平滑脱嵌")
    slabs(axes[1, 2], [0, 0.50, 0, 0.50], "→ O2 / OP4", ACC, "高电压 c 轴猛缩")

    fig.suptitle("充电 = 抽走层间支柱。空了，TMO$_2$ 板就相对滑动。",
                 fontsize=13, color=INK, y=0.02)
    plt.tight_layout(rect=[0, 0.06, 1, 0.98])
    save(fig, "08_phase_transition.png")


# ============================================================
# 09  对照：六维雷达条，不是密表
# ============================================================
def draw_09():
    fig, ax = plt.subplots(figsize=(10.6, 5.6))
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 5.6)
    ax.axis("off")
    ax.set_title("O3 赌能量，P2 赌功率。量产配方在两者之间微调。",
                 fontsize=13, color=INK, pad=6)

    items = [
        ("初始钠  x", 0.95, 0.62, "≈ 1.0", "≈ 0.67"),
        ("扩散快慢", 0.42, 0.88, "Oh–Td–Oh 慢", "矩形窗 快"),
        ("相变复杂度", 0.78, 0.48, "O3→P3→O1", "宽固溶，高压 O2"),
        ("空气稳定", 0.32, 0.70, "易成残碱", "相对耐潮"),
        ("全电池匹配", 0.90, 0.45, "自身供钠", "常需补钠"),
        ("循环寿命", 0.48, 0.72, "高压易裂", "骨架更皮实"),
    ]
    ax.text(4.2, 5.18, "O3", ha="center", fontsize=13, color=O3)
    ax.text(8.15, 5.18, "P2", ha="center", fontsize=13, color=P2)
    for i, (name, o3v, p2v, t1, t2) in enumerate(items):
        y = 4.55 - i * 0.68
        ax.text(0.22, y + 0.10, name, ha="left", va="center", fontsize=10, color=INK)
        ax.add_patch(Rectangle((2.4, y), 3.6, 0.22, fc="#edf1f5", zorder=2))
        ax.add_patch(Rectangle((2.4, y), 3.6 * o3v, 0.22, fc=O3, zorder=3))
        ax.add_patch(Rectangle((6.35, y), 3.6, 0.22, fc="#edf1f5", zorder=2))
        ax.add_patch(Rectangle((6.35, y), 3.6 * p2v, 0.22, fc=P2, zorder=3))
        ax.text(4.2, y + 0.36, t1, ha="center", fontsize=8.0, color=O3)
        ax.text(8.15, y + 0.36, t2, ha="center", fontsize=8.0, color=P2)
    ax.text(5.3, 0.28, "条越长越好理解成“这一项更占优”。相变复杂度相反：条越长越折腾。",
            ha="center", fontsize=8.6, color=MUTED)
    save(fig, "09_compare.png")


# ============================================================
# 11  三维：交错 vs 对齐
# ============================================================
def draw_11():
    fig = plt.figure(figsize=(10.8, 5.2))

    def pack(ax, eclipsed, title, color):
        ax.set_axis_off()
        ax.view_init(16, 32)
        ax.set_xlim(-0.15, 2.35)
        ax.set_ylim(-0.15, 2.15)
        ax.set_zlim(-0.05, 2.55)
        ax.set_box_aspect((1.15, 1.0, 1.15), zoom=1.22)
        for pane in (ax.xaxis.pane, ax.yaxis.pane, ax.zaxis.pane):
            pane.fill = False
            pane.set_edgecolor("none")
        ax.set_title(title, fontsize=12, color=color, pad=4)
        a = 0.78

        def layer(z, ox_off, show_na=False, show_tm=False):
            for i in range(4):
                for j in range(4):
                    x = (i + 0.5 * j) * a * 0.82 + ox_off[0]
                    y = j * a * np.sqrt(3) / 2 * 0.82 + ox_off[1]
                    ax.scatter(x, y, z, s=36, c=OX, edgecolors="k", lw=0.2, depthshade=True)
            if show_tm:
                for i in range(3):
                    for j in range(3):
                        x = (i + 0.5 + 0.5 * j) * a * 0.82 + ox_off[0]
                        y = (j + 0.35) * a * np.sqrt(3) / 2 * 0.82 + ox_off[1]
                        ax.scatter(x, y, z + 0.28, s=52, c=TM, edgecolors="k", lw=0.2)
            if show_na:
                for i in range(3):
                    for j in range(3):
                        x = (i + 0.35 + 0.5 * j) * a * 0.82 + ox_off[0] + 0.08
                        y = (j + 0.22) * a * np.sqrt(3) / 2 * 0.82 + ox_off[1] + 0.06
                        ax.scatter(x, y, z + 0.42, s=70, c=NA, edgecolors="k", lw=0.25)

        if eclipsed:
            layer(0.0, (0, 0), show_tm=True)
            layer(1.05, (0, 0), show_na=True)
            layer(2.10, (0, 0), show_tm=True)
        else:
            layer(0.0, (0, 0), show_tm=True)
            layer(1.05, (0.30, 0.18), show_na=True)
            layer(2.10, (0.60, 0.36), show_tm=True)

    ax1 = fig.add_subplot(121, projection="3d")
    pack(ax1, False, "O3  上下氧错开", O3)
    ax2 = fig.add_subplot(122, projection="3d")
    pack(ax2, True, "P2  上下氧叠合", P2)
    fig.suptitle("红氧 · 青 TM · 金钠", fontsize=12, color=MUTED, y=0.03)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.90, bottom=0.08, wspace=0.06)
    save(fig, "11_3d_layers.png")


# ============================================================
# 12  速记海报
# ============================================================
def draw_12():
    fig, ax = plt.subplots(figsize=(10.8, 5.8))
    ax.set_xlim(0, 10.8)
    ax.set_ylim(0, 5.8)
    ax.axis("off")
    box(ax, 0.18, 0.18, 10.44, 5.44, "#fffbeb", GOLD, lw=2.0)
    ax.text(5.4, 5.22, "O3 / P2  四句口诀", ha="center",
            fontsize=16, color="#7d4e00")

    cards = [
        (0.45, 2.85, O3, "字母看笼子", "O 交错 → 八面体\nP 对齐 → 三棱柱"),
        (3.85, 2.85, P2, "数字看步数", "3 = 绕完 A-B-C\n2 = A-B 折返"),
        (7.25, 2.85, ACC, "O3 高钠", "x ≈ 1\n能量优先"),
        (0.45, 0.45, GOLD, "P2 快离子", "矩形窗\nx ≈ 2/3"),
        (3.85, 0.45, O3, "出口决定倍率", "三角窗窄\n矩形窗宽"),
        (7.25, 0.45, P2, "工业折中", "P2/O3 双相\nO3 补钠  P2 保通道"),
    ]
    for x, y, c, t, b in cards:
        box(ax, x, y, 3.1, 2.05, "#fff", c, lw=1.6)
        ax.add_patch(Rectangle((x, y + 1.62), 3.1, 0.43, fc=c, zorder=3))
        ax.text(x + 1.55, y + 1.83, t, ha="center", va="center",
                color="white", fontsize=11, zorder=4)
        ax.text(x + 1.55, y + 0.75, b, ha="center", va="center",
                fontsize=9, color=INK, linespacing=1.45)
    save(fig, "12_poster.png")


# ============================================================
# 20  ABC 三个落点：俯视密排
# ============================================================
def draw_20():
    fig, ax = plt.subplots(figsize=(10.4, 5.4))
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_xlim(-0.6, 10.6)
    ax.set_ylim(-1.15, 5.15)
    ax.set_title("密堆积平面只有三个落点  A / B / C", fontsize=13.5, color=INK, pad=8)

    a = 0.92
    cols = {"A": "#e74c3c", "B": "#2980b9", "C": "#27ae60"}
    panels = [("A", 0.35), ("B", 3.85), ("C", 7.35)]
    for k, x0 in panels:
        xs, ys = [], []
        for i in range(3):
            for j in range(3):
                x = x0 + (i + 0.5 * j) * a
                y = 0.70 + j * a * np.sqrt(3) / 2
                ax.add_patch(Circle((x, y), 0.22, fc=cols[k], ec="k", lw=0.35, zorder=3))
                xs.append(x)
                ys.append(y)
        cx = 0.5 * (min(xs) + max(xs))
        ax.text(cx, 4.55, k, ha="center", color=cols[k], fontsize=22)
        ax.text(cx, 4.12,
                {"A": "参考格点", "B": "错开半步", "C": "再错开半步"}[k],
                ha="center", fontsize=8.6, color=MUTED)

    ax.text(5.2, -0.55,
            "换字母 → 八面体          同字母 → 三棱柱",
            ha="center", fontsize=10.5, color=INK)
    save(fig, "20_abc_sites.png")


# ============================================================
# 21  O3 三步绕三角形
# ============================================================
def draw_21():
    fig, ax = plt.subplots(figsize=(10.4, 5.4))
    ax.set_xlim(0, 10.4)
    ax.set_ylim(0, 5.4)
    ax.axis("off")
    ax.set_title("O 型必须绕完 A–B–C。三步才回家，所以是 O3。",
                 fontsize=13, color=O3, pad=4)

    verts = np.array([[2.55, 1.55], [5.2, 4.05], [7.85, 1.55]])
    labels = ["A", "B", "C"]
    cols = ["#e74c3c", "#2980b9", "#27ae60"]
    ax.add_patch(Polygon(verts, closed=True, fill=False, ec=O3, lw=2.2, zorder=2))
    for (x, y), lab, c in zip(verts, labels, cols):
        ax.add_patch(Circle((x, y), 0.46, fc=c, ec="k", lw=0.7, zorder=4))
        ax.text(x, y, lab, ha="center", va="center", color="white",
                fontsize=18, zorder=5)
    for i, step in enumerate(["1", "2", "3"]):
        p, q = verts[i], verts[(i + 1) % 3]
        ax.annotate("", xy=q * 0.78 + p * 0.22, xytext=p * 0.78 + q * 0.22,
                    arrowprops=dict(arrowstyle="-|>", color=O3, lw=2.0))
        mid = 0.5 * (p + q)
        nrm = np.array([-(q - p)[1], (q - p)[0]])
        nrm = nrm / (np.linalg.norm(nrm) + 1e-9) * 0.32
        ax.text(*(mid + nrm), f"第 {step} 步", ha="center", va="center",
                fontsize=9, color=O3)

    ax.text(5.2, 0.55, "氧序列 ABCABC", ha="center", fontsize=11, color=INK)
    save(fig, "21_o3_three_steps.png")


# ============================================================
# 22  P2 两步折返
# ============================================================
def draw_22():
    fig, ax = plt.subplots(figsize=(10.2, 5.0))
    ax.set_xlim(0, 10.2)
    ax.set_ylim(0, 5.0)
    ax.axis("off")
    ax.set_title("P 型在两个落点之间弹一次。两步回家，所以是 P2。",
                 fontsize=13, color=P2)

    ax.add_patch(Circle((2.6, 2.35), 0.55, fc="#e74c3c", ec="k", lw=0.8, zorder=4))
    ax.add_patch(Circle((7.6, 2.35), 0.55, fc="#2980b9", ec="k", lw=0.8, zorder=4))
    ax.text(2.6, 2.35, "A", ha="center", va="center", color="white", fontsize=20, zorder=5)
    ax.text(7.6, 2.35, "B", ha="center", va="center", color="white", fontsize=20, zorder=5)
    ax.annotate("", xy=(6.9, 2.70), xytext=(3.3, 2.70),
                arrowprops=dict(arrowstyle="-|>", color=P2, lw=2.4))
    ax.annotate("", xy=(3.3, 2.00), xytext=(6.9, 2.00),
                arrowprops=dict(arrowstyle="-|>", color=P2, lw=2.4))
    ax.text(5.1, 3.05, "第 1 步  A→B   BB 对齐", ha="center", fontsize=10.5, color=P2)
    ax.text(5.1, 1.55, "第 2 步  B→A   AA 对齐", ha="center", fontsize=10.5, color=P2)

    ax.text(5.1, 0.55, "氧序列 ABBA", ha="center", fontsize=11, color=INK)
    save(fig, "22_p2_two_steps.png")


# ============================================================
# 23  周期家族：珠串
# ============================================================
def draw_23():
    fig, ax = plt.subplots(figsize=(10.8, 5.4))
    ax.set_xlim(0, 10.8)
    ax.set_ylim(0, 5.4)
    ax.axis("off")
    ax.set_title("数字 = TMO$_2$ 板走完一圈的步数", fontsize=13.5, color=INK)

    fams = [
        ("P2", P2, "ABBA", "棱柱 · 两步"),
        ("P3", "#1e8449", "ABBCCA", "棱柱 · 三步"),
        ("O3", O3, "ABCABC", "八面体 · 三步"),
        ("O2", "#6c3483", "ABAC", "八面体 · 两步"),
    ]
    for i, (name, c, seq, geo) in enumerate(fams):
        x = 0.35 + i * 2.6
        box(ax, x, 1.35, 2.4, 3.4, "#fff", c, lw=1.8)
        ax.add_patch(Rectangle((x, 4.25), 2.4, 0.5, fc=c, zorder=3))
        ax.text(x + 1.2, 4.50, name, ha="center", va="center", color="white",
                fontsize=16, zorder=4)
        ax.text(x + 1.2, 3.90, geo, ha="center", fontsize=10, color=c)
        cmap = {"A": "#e74c3c", "B": "#2980b9", "C": "#27ae60"}
        beads = list(seq)
        yy = 3.35
        for k, ch in enumerate(beads):
            ax.add_patch(Circle((x + 0.45 + (k % 6) * 0.32, yy - (k // 6) * 0.38),
                                0.14, fc=cmap[ch], ec="k", lw=0.3, zorder=4))
        ax.text(x + 1.2, 2.45, seq, ha="center", fontsize=10, color=INK, fontfamily="DejaVu Sans")
    save(fig, "23_period_family.png")


# ============================================================
# 24  为什么 O 两步合不上
# ============================================================
def draw_24():
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 5.1))

    ax = axes[0]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("O 型走两步  ·  停在 C  ·  缺 C→A", fontsize=11.5, color=ACC, pad=6)
    verts = np.array([[5.0, 7.55], [2.35, 3.05], [7.65, 3.05]])
    cols = ["#e74c3c", "#2980b9", "#27ae60"]
    labs = ["A", "B", "C"]
    r = 0.70
    for i, style in ((0, "-|>"), (1, "-|>")):
        p, q = verts[i], verts[i + 1]
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=14,
                                     lw=2.2, color=O3, shrinkA=18, shrinkB=18, zorder=3))
    ax.add_patch(FancyArrowPatch(verts[2], verts[0], arrowstyle="-", mutation_scale=1,
                                 lw=1.8, color=ACC, linestyle="--",
                                 shrinkA=18, shrinkB=18, zorder=3))
    for (x, y), c, lab in zip(verts, cols, labs):
        ax.add_patch(Circle((x, y), r, fc=c, ec="k", lw=0.6, zorder=4))
        ax.text(x, y, lab, ha="center", va="center", color="white", fontsize=16, zorder=5)
    ax.text(5, 1.35, "缺口还在", ha="center", fontsize=12.5, color=ACC)

    ax = axes[1]
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("P 型走两步  ·  A↔B 折返  ·  刚好闭合", fontsize=11.5, color=P2, pad=6)
    ax.add_patch(Circle((2.7, 5.2), 0.78, fc="#e74c3c", ec="k", lw=0.6, zorder=4))
    ax.add_patch(Circle((7.3, 5.2), 0.78, fc="#2980b9", ec="k", lw=0.6, zorder=4))
    ax.text(2.7, 5.2, "A", ha="center", va="center", color="white", fontsize=18, zorder=5)
    ax.text(7.3, 5.2, "B", ha="center", va="center", color="white", fontsize=18, zorder=5)
    ax.annotate("", xy=(6.4, 5.95), xytext=(3.6, 5.95),
                arrowprops=dict(arrowstyle="-|>", color=P2, lw=2.2))
    ax.annotate("", xy=(3.6, 4.45), xytext=(6.4, 4.45),
                arrowprops=dict(arrowstyle="-|>", color=P2, lw=2.2))
    ax.text(5, 1.35, "锁上了", ha="center", fontsize=12.5, color=P2)

    fig.suptitle("真正决定 2 还是 3 的，是钠层两侧氧换不换字母",
                 fontsize=13, color=INK, y=0.02)
    plt.tight_layout(rect=[0, 0.07, 1, 1])
    save(fig, "24_cannot_close.png")


def main():
    print("=" * 56)
    print("重绘 O3 / P2 / 八面体 / 三棱柱 全套结构图")
    print("=" * 56)
    draw_01()
    draw_02()
    draw_10()
    draw_03()
    draw_04()
    draw_05()
    draw_06()
    draw_07()
    draw_08()
    draw_09()
    draw_11()
    draw_12()
    draw_20()
    draw_21()
    draw_22()
    draw_23()
    draw_24()
    print("=" * 56)
    print("完成", OUT)
    print("=" * 56)


if __name__ == "__main__":
    main()
