#!/usr/bin/env python3
"""
Generate a vector graphic (SVG) of the training pipeline diagram.
Matches the exact layout from diagram.png
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
import os

# Set up the figure to match the original diagram proportions (wider, shorter)
fig, ax = plt.subplots(1, 1, figsize=(18, 7), dpi=150)
ax.set_xlim(0, 18)
ax.set_ylim(0, 7)
ax.axis('off')

# Define colors to match original
color_document_box = 'white'
color_document_border = 'black'
color_prediction_box = '#FFF3E0'  # Light beige
color_prediction_border = 'black'
color_reward_bg = '#E1BEE7'  # Light purple
color_reward_border = '#8B4789'  # Purple
color_arrow = 'black'
color_text = 'black'

# Font settings
font_title = {'fontsize': 10, 'fontweight': 'bold', 'color': color_text, 'family': 'sans-serif'}
font_body = {'fontsize': 8, 'color': color_text, 'family': 'sans-serif'}
font_small = {'fontsize': 7, 'color': color_text, 'family': 'sans-serif'}

# ============================================================================
# Step 1: Original Document (top left)
# ============================================================================
box1_x, box1_y = 0.3, 4.5
box1_w, box1_h = 2.4, 2.0

box1 = Rectangle((box1_x, box1_y), box1_w, box1_h,
                  edgecolor=color_document_border,
                  facecolor=color_document_box,
                  linewidth=1.5)
ax.add_patch(box1)

# Title above box
ax.text(box1_x, box1_y + box1_h + 0.05, '1. Original Document',
        ha='left', va='bottom', **font_title)

# Content
doc_text = ("Ohm's law governs\nthe relationship\nbetween voltage V\nand current I in a\n"
            "resistive circuit of\nresistance R.\nV= I x R.\nFor example, if the a\n"
            "voltage of 12 volts is\napplied across a 3\nOhm resistance then\n"
            "the current will be 4\nAmpere.")
ax.text(box1_x + 0.1, box1_y + box1_h - 0.1, doc_text,
        ha='left', va='top', **font_body, linespacing=1.3)

# ============================================================================
# Step 2: Masked Document (center-left) - TWO SEPARATE BOXES
# ============================================================================
box2_x = 3.5
box2_section_y = 4.5  # Base y for the entire section
box2_w = 2.4

# Title above both boxes
ax.text(box2_x, box2_section_y + 2.05, '2. Masked Document',
        ha='left', va='bottom', **font_title)

# Upper box: Masked Document content
masked_box_y = box2_section_y + 1.0
masked_box_h = 1.0
masked_box = Rectangle((box2_x, masked_box_y), box2_w, masked_box_h,
                       edgecolor=color_document_border,
                       facecolor=color_document_box,
                       linewidth=1.5)
ax.add_patch(masked_box)

# Masked text content
masked_text = ("Ohm's law governs...\nresistive circuit of\n[MASKED_TEXT]\n"
               "then the current will\nbe 4 Amperes.")
ax.text(box2_x + 0.1, masked_box_y + masked_box_h - 0.1, masked_text,
        ha='left', va='top', **font_body, linespacing=1.3)

# Lower box: Ground Truth Segment
gt_box_y = box2_section_y
gt_box_h = 0.9
gt_box = Rectangle((box2_x, gt_box_y), box2_w, gt_box_h,
                   edgecolor=color_document_border,
                   facecolor='white',
                   linewidth=1.5)
ax.add_patch(gt_box)

# Ground Truth label and content
ax.text(box2_x + 0.1, gt_box_y + gt_box_h - 0.05, 'Ground Truth Segment',
        ha='left', va='top', **font_small, fontweight='bold')
gt_text = "V= I x R. For example,\nif the a voltage of 12\nvolts is applied across\na 3 Ohm resistance"
ax.text(box2_x + 0.1, gt_box_y + gt_box_h - 0.25, gt_text,
        ha='left', va='top', **font_small, linespacing=1.2)

# Define the center point for arrows (between the two boxes)
box2_center_y = box2_section_y + 1.0

# ============================================================================
# Arrow 1: Original -> Forked to both Masked Document and Ground Truth
# ============================================================================
# Main horizontal arrow from Original Document
fork_start_x = box1_x + box1_w + 0.1
fork_mid_x = box1_x + box1_w + 0.5
fork_y = box1_y + box1_h/2

# Horizontal segment
arrow1_horizontal = FancyArrowPatch((fork_start_x, fork_y),
                                   (fork_mid_x, fork_y),
                                   arrowstyle='-', mutation_scale=15,
                                   linewidth=1.5, color=color_arrow)
ax.add_patch(arrow1_horizontal)

# Fork to upper box (Masked Document)
arrow1_upper = FancyArrowPatch((fork_mid_x, fork_y),
                              (box2_x - 0.1, masked_box_y + masked_box_h/2),
                              arrowstyle='->', mutation_scale=15,
                              linewidth=1.5, color=color_arrow)
ax.add_patch(arrow1_upper)

# Fork to lower box (Ground Truth Segment)
arrow1_lower = FancyArrowPatch((fork_mid_x, fork_y),
                              (box2_x - 0.1, gt_box_y + gt_box_h/2),
                              arrowstyle='->', mutation_scale=15,
                              linewidth=1.5, color=color_arrow)
ax.add_patch(arrow1_lower)

# Label for arrow
ax.text(fork_mid_x, fork_y + 0.25, 'Contiguous',
        ha='center', va='bottom', **font_small)
ax.text(fork_mid_x, fork_y + 0.05, 'Masking',
        ha='center', va='bottom', **font_small)

# ============================================================================
# Step 3: Target LLM (robot student)
# ============================================================================
# Position at same vertical center as the boxes
robot_student_x, robot_student_y = 7.5, box2_center_y + 0.3

# Load and display robot student image
script_dir = os.path.dirname(os.path.abspath(__file__))
robot_student_path = os.path.join(script_dir, 'robot_student.png')
if os.path.exists(robot_student_path):
    img_student = Image.open(robot_student_path)
    imagebox_student = OffsetImage(img_student, zoom=0.12)
    ab_student = AnnotationBbox(imagebox_student, (robot_student_x, robot_student_y),
                                frameon=False, pad=0)
    ax.add_artist(ab_student)

# Label below robot
ax.text(robot_student_x, robot_student_y - 0.95, '3. Target LLM',
        ha='center', va='top', fontsize=9, fontweight='bold', color=color_text, family='sans-serif')

# ============================================================================
# Arrow 2: Masked Document -> Target LLM (only from upper box)
# ============================================================================
arrow2 = FancyArrowPatch((box2_x + box2_w + 0.1, masked_box_y + masked_box_h/2),
                        (robot_student_x - 0.7, robot_student_y - 0.2),
                        arrowstyle='->', mutation_scale=15,
                        linewidth=1.5, color=color_arrow)
ax.add_patch(arrow2)

# ============================================================================
# Predicted Completion box (top right)
# ============================================================================
pred_x, pred_y = 9.5, 4.5
pred_w, pred_h = 2.8, 2.0

# ============================================================================
# Arrow 3: Target LLM -> Predicted Completion
# ============================================================================
arrow3 = FancyArrowPatch((robot_student_x + 0.7, robot_student_y - 0.2),
                        (pred_x - 0.1, box2_center_y),
                        arrowstyle='->', mutation_scale=15,
                        linewidth=1.5, color=color_arrow)
ax.add_patch(arrow3)

box_pred = Rectangle((pred_x, pred_y), pred_w, pred_h,
                     edgecolor=color_prediction_border,
                     facecolor=color_prediction_box,
                     linewidth=1.5)
ax.add_patch(box_pred)

# Title above box
ax.text(pred_x, pred_y + pred_h + 0.05, 'Predicted Completion',
        ha='left', va='bottom', **font_title)

# Content
pred_text = ("The relationship is\nV = I * R.\nSo, with 8 Volts and\n3 Ohms...")
ax.text(pred_x + 0.1, pred_y + pred_h - 0.1, pred_text,
        ha='left', va='top', **font_body, linespacing=1.4)

# ============================================================================
# Arrow 4: Predicted Completion -> Judge LLM
# ============================================================================
arrow4 = FancyArrowPatch((pred_x + pred_w/2, pred_y - 0.1),
                        (pred_x + pred_w/2, 3.2),
                        arrowstyle='->', mutation_scale=15,
                        linewidth=1.5, color=color_arrow)
ax.add_patch(arrow4)

# ============================================================================
# Step 4: Judge LLM (robot judge)
# ============================================================================
robot_judge_x, robot_judge_y = pred_x + pred_w/2, 2.5

# Load and display robot judge image
robot_judge_path = os.path.join(script_dir, 'robot_judge.png')
if os.path.exists(robot_judge_path):
    img_judge = Image.open(robot_judge_path)
    imagebox_judge = OffsetImage(img_judge, zoom=0.12)
    ab_judge = AnnotationBbox(imagebox_judge, (robot_judge_x, robot_judge_y),
                             frameon=False, pad=0)
    ax.add_artist(ab_judge)

# Label below robot
ax.text(robot_judge_x, robot_judge_y - 0.85, '4. Judge LLM',
        ha='center', va='top', fontsize=9, fontweight='bold', color=color_text, family='sans-serif')

# ============================================================================
# Arrow 5: Judge LLM -> Reward
# ============================================================================
arrow5 = FancyArrowPatch((robot_judge_x + 0.7, robot_judge_y),
                        (13.5, robot_judge_y),
                        arrowstyle='->', mutation_scale=15,
                        linewidth=1.5, color=color_arrow)
ax.add_patch(arrow5)

# ============================================================================
# Reward Badge (circular, bottom right)
# ============================================================================
reward_x, reward_y = 14.5, robot_judge_y
reward_radius = 0.6

# Outer circle
circle_outer = Circle((reward_x, reward_y), reward_radius,
                     edgecolor=color_reward_border,
                     facecolor=color_reward_bg,
                     linewidth=2)
ax.add_patch(circle_outer)

# Text in circle
ax.text(reward_x, reward_y + 0.15, 'Similarity',
        ha='center', va='center', fontsize=7, fontweight='normal', color=color_text, family='sans-serif')
ax.text(reward_x, reward_y - 0.15, 'Score: 2/3',
        ha='center', va='center', fontsize=8, fontweight='normal', color=color_text, family='sans-serif')

# Label below circle
ax.text(reward_x, reward_y - reward_radius - 0.15, 'Reward',
        ha='center', va='top', fontsize=9, fontweight='bold', color=color_text, family='sans-serif')

# ============================================================================
# Caption at the bottom
# ============================================================================
caption_text = ("Overview of the training pipeline: A contiguous text span is masked and fed to a student LLM.\n"
                "Its prediction is then scored against the ground truth by a judge LLM.")
ax.text(9, 0.3, caption_text,
        ha='center', va='bottom', fontsize=9, color=color_text, family='sans-serif')

# ============================================================================
# Save the figure as PNG for comparison
# ============================================================================
output_path_png = os.path.join(script_dir, 'figure_1_generated.png')
output_path_svg = os.path.join(script_dir, 'figure_1.svg')
plt.tight_layout(pad=0.5)
plt.savefig(output_path_png, format='png', bbox_inches='tight', dpi=150)
plt.savefig(output_path_svg, format='svg', bbox_inches='tight', dpi=150)
print(f"✓ Successfully generated: {output_path_png}")
print(f"✓ Successfully generated: {output_path_svg}")
plt.close()
