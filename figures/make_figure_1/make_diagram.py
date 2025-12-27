#!/usr/bin/env python3
import textwrap

import matplotlib.pyplot as plt
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from matplotlib.patches import FancyBboxPatch, Circle


def add_box(ax, x, y, w, h, text, edgecolor, facecolor="white", fontsize=11):
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.008,rounding_size=0.01",
        linewidth=2,
        edgecolor=edgecolor,
        facecolor=facecolor,
    )
    ax.add_patch(box)
    wrapped = textwrap.fill(text, width=28)
    ax.text(
        x + 0.012,
        y + h - 0.02,
        wrapped,
        ha="left",
        va="top",
        fontsize=fontsize,
    )


def add_image(ax, path, center, zoom):
    image = plt.imread(path)
    ab = AnnotationBbox(OffsetImage(image, zoom=zoom), center, frameon=False)
    ax.add_artist(ab)


def add_elbow_arrow(ax, start, end, angle_a=0, angle_b=90, shrink_a=0, shrink_b=0):
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops=dict(
            arrowstyle="-|>",
            lw=1.6,
            color="black",
            connectionstyle=f"angle,angleA={angle_a},angleB={angle_b},rad=0",
            shrinkA=shrink_a,
            shrinkB=shrink_b,
        ),
    )


def main():
    fig = plt.figure(figsize=(12, 6.54), dpi=150)
    ax = plt.axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    blue = "#3B6FB6"
    orange = "#C7771E"
    purple = "#8A5CAD"
    purple_fill = "#E6D9EC"

    # Left: Original document
    ax.text(0.05, 0.90, "1. Original Document", fontsize=13, weight="bold")
    add_box(
        ax,
        x=0.05,
        y=0.23,
        w=0.22,
        h=0.62,
        edgecolor=blue,
        text=(
            "Ohm's law governs the relationship between voltage V and current I "
            "in resistive circuit of resistance R. V = I x R. For example, if the "
            "a voltage of 12 volts is applied across a 3 Ohm resistance then the "
            "current will be 4 Amperes."
        ),
    )

    # Middle: Masked + ground truth
    ax.text(0.36, 0.90, "2. Masked Document", fontsize=13, weight="bold")
    add_box(
        ax,
        x=0.36,
        y=0.61,
        w=0.23,
        h=0.25,
        edgecolor=blue,
        text=(
            "Ohm's law governs... resistive circuit of resistance R. "
            "[MASKED_TEXT] then the current will be 4 Amperes."
        ),
    )
    ax.text(0.36, 0.49, "Ground Truth Segment", fontsize=12, weight="bold")
    add_box(
        ax,
        x=0.36,
        y=0.26,
        w=0.23,
        h=0.20,
        edgecolor=blue,
        text=(
            "V = I x R. For example, if the a voltage of 12 volts is applied "
            "across a 3 Ohm resistance"
        ),
    )

    # Contiguous masking arrows from original to middle
    ax.text(0.24, 0.58, "Contiguous\nMasking", fontsize=11, ha="center", va="center")
    ax.plot([0.30, 0.30], [0.33, 0.72], color="black", lw=1.6)
    ax.plot([0.27, 0.30], [0.52, 0.52], color="black", lw=1.6)
    ax.annotate(
        "",
        xy=(0.36, 0.70),
        xytext=(0.30, 0.70),
        arrowprops=dict(arrowstyle="-|>", lw=1.6, color="black"),
    )
    ax.annotate(
        "",
        xy=(0.36, 0.32),
        xytext=(0.30, 0.32),
        arrowprops=dict(arrowstyle="-|>", lw=1.6, color="black"),
    )

    # Target LLM (student)
    ax.text(0.71, 0.90, "3. Target LLM", fontsize=13, weight="bold", ha="center")
    add_image(ax, "robot_student.png", center=(0.74, 0.71), zoom=0.15)

    # Predicted completion
    ax.text(0.88, 0.90, "Predicted Completion", fontsize=13, weight="bold", ha="center")
    add_box(
        ax,
        x=0.82,
        y=0.63,
        w=0.17,
        h=0.20,
        edgecolor=orange,
        text=(
            "The relationship is V = I * R. So, with 8 Volts and 2 Ohms..."
        ),
    )

    ax.annotate(
        "",
        xy=(0.82, 0.73),
        xytext=(0.76, 0.73),
        arrowprops=dict(arrowstyle="-|>", lw=1.6, color="black"),
    )
    ax.plot([0.91, 0.91], [0.63, 0.54], color="black", lw=1.6)
    ax.plot([0.91, 0.71], [0.54, 0.54], color="black", lw=1.6)
    ax.annotate(
        "",
        xy=(0.71, 0.41),
        xytext=(0.71, 0.54),
        arrowprops=dict(arrowstyle="-|>", lw=1.6, color="black"),
    )

    # Judge LLM + reward
    ax.text(0.74, 0.20, "4. Judge LLM", fontsize=13, weight="bold", ha="center")
    add_image(ax, "robot_judge.png", center=(0.74, 0.36), zoom=0.15)

    ax.text(0.91, 0.50, "Reward", fontsize=12, weight="bold", ha="center")
    reward = Circle((0.93, 0.36), 0.07, edgecolor=purple, facecolor=purple_fill, lw=2)
    ax.add_patch(reward)
    ax.text(0.93, 0.36, "Similarity\nScore: 2/3", ha="center", va="center", fontsize=11)

    ax.annotate(
        "",
        xy=(0.86, 0.36),
        xytext=(0.78, 0.36),
        arrowprops=dict(arrowstyle="-|>", lw=1.6, color="black"),
    )

    ax.annotate(
        "",
        xy=(0.69, 0.71),
        xytext=(0.59, 0.71),
        arrowprops=dict(arrowstyle="-|>", lw=1.6, color="black"),
    )
    ax.annotate(
        "",
        xy=(0.69, 0.33),
        xytext=(0.59, 0.33),
        arrowprops=dict(arrowstyle="-|>", lw=1.6, color="black"),
    )

    # Description
    ax.text(
        0.5,
        0.08,
        "Overview of the training pipeline: A contiguous text span is masked and "
        "fed to a student LLM. Its prediction is then scored against the ground "
        "truth by a judge LLM.",
        ha="center",
        va="center",
        fontsize=12,
        fontfamily="serif",
    )

    fig.savefig("diagram_generated.svg", bbox_inches="tight")
    fig.savefig("diagram_generated.png", dpi=300, bbox_inches="tight")


if __name__ == "__main__":
    main()
