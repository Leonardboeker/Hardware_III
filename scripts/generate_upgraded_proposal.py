"""
UPGRADED Proposal — 3 slides PDF
Incorporates all review critiques + strongest additions.
"""
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER

WIDTH, HEIGHT = landscape(A4)

# ─── Palette ───
BG        = HexColor('#0f0f1a')
PANEL     = HexColor('#161627')
ACCENT    = HexColor('#ff3366')
ACCENT2   = HexColor('#ff6b35')
CYAN      = HexColor('#00d4ff')
GREEN     = HexColor('#00cc88')
PURPLE    = HexColor('#8855ff')
YELLOW    = HexColor('#ffcc00')
TEXT      = HexColor('#f0f0f0')
DIM       = HexColor('#7a7a9e')
DARK      = HexColor('#0a0a14')

def bg(c):
    c.setFillColor(BG)
    c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)
    # Top accent bar
    c.setFillColor(ACCENT)
    c.rect(0, HEIGHT - 3*mm, WIDTH, 3*mm, fill=1, stroke=0)
    # Thin bottom line
    c.setFillColor(HexColor('#1a1a30'))
    c.rect(0, 0, WIDTH, 1*mm, fill=1, stroke=0)

def footer(c, n):
    c.setFillColor(DIM)
    c.setFont('Helvetica', 7)
    c.drawString(30, 10, 'MATTER & METHOD \u2014 Hardware III \u2014 MRAC 2025/2026')
    c.drawRightString(WIDTH - 30, 10, f'{n} / 3')

def panel(c, x, y, w, h, color=PANEL, radius=8):
    c.setFillColor(color)
    c.roundRect(x, y, w, h, radius, fill=1, stroke=0)

def tag(c, x, y, label, color=ACCENT):
    c.setFillColor(color)
    c.setFont('Helvetica-Bold', 7.5)
    tw = c.stringWidth(label, 'Helvetica-Bold', 7.5)
    c.roundRect(x, y - 3, tw + 10, 14, 3, fill=1, stroke=0)
    c.setFillColor(BG)
    c.drawString(x + 5, y, label)

def heading(c, x, y, text, size=13, color=TEXT):
    c.setFillColor(color)
    c.setFont('Helvetica-Bold', size)
    c.drawString(x, y, text)

def body(c, x, y, lines, size=9.5, leading=14, color=TEXT):
    c.setFont('Helvetica', size)
    c.setFillColor(color)
    for line in lines:
        if line.startswith('**'):
            clean = line.strip('*')
            c.setFont('Helvetica-Bold', size)
            c.drawString(x, y, clean)
            c.setFont('Helvetica', size)
        else:
            c.drawString(x, y, line)
        y -= leading
    return y

def bullet(c, x, y, items, size=9, leading=14, color=TEXT, bullet_color=ACCENT):
    for item in items:
        c.setFillColor(bullet_color)
        c.setFont('Helvetica-Bold', 8)
        c.drawString(x, y + 1, '\u25cf')
        c.setFillColor(color)
        c.setFont('Helvetica', size)
        c.drawString(x + 12, y, item)
        y -= leading
    return y

# ═══════════════════════════════════════════════
c = canvas.Canvas('Proposal_v2.pdf', pagesize=landscape(A4))

# ──────────────────────────────────────────────
# SLIDE 1: The Concept (Redesigned)
# ──────────────────────────────────────────────
bg(c)
footer(c, 1)

# Title block
c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 36)
c.drawString(40, HEIGHT - 65, 'MATTER & METHOD')
c.setFont('Helvetica', 15)
c.setFillColor(DIM)
c.drawString(40, HEIGHT - 88, 'Building the same wall four ways. Feeling the difference.')

# Concept description — left column
panel(c, 30, 195, 370, 290)
tag(c, 42, 465, 'CONCEPT')
body(c, 42, 445, [
    'A tabletop installation. One wall section.',
    'Four construction methods. One projector.',
    '',
    'You physically build ONE method end-to-end,',
    'guided by projected light on the table.',
    'As each piece lands, data appears ON IT:',
    'CO\u2082 cost, labor hours, supply chain origin.',
    '',
    'The other three methods play as projected',
    'animations on adjacent zones \u2014 same table,',
    'no rebuilding, no visitor fatigue.',
    '',
    'At the end: all four methods compared',
    'side by side. Same wall. Different worlds.',
], size=10, leading=15.5)

# The four methods — right column
panel(c, 415, 370, 370, 115)
tag(c, 427, 465, 'THE FOUR METHODS', ACCENT2)
# Method cards
methods = [
    ('MASONRY', 'Brick by brick', 'Traditional', ACCENT2),
    ('3D PRINT', 'Layer by layer', 'Automated', CYAN),
    ('PREFAB', 'Panel by panel', 'Industrial', PURPLE),
    ('REUSED', 'Salvaged brick', 'Circular', GREEN),
]
x_start = 427
for i, (name, sub, cat, color) in enumerate(methods):
    bx = x_start + i * 88
    panel(c, bx, 382, 80, 55, color=DARK)
    c.setFillColor(color)
    c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(bx + 40, 420, name)
    c.setFillColor(DIM)
    c.setFont('Helvetica', 7.5)
    c.drawCentredString(bx + 40, 407, sub)
    c.drawCentredString(bx + 40, 395, cat)

# Why reused brick?
panel(c, 415, 255, 370, 105)
tag(c, 427, 340, 'WHY REUSED BRICK?', GREEN)
body(c, 427, 318, [
    'Embodied carbon: near zero. Outperforms 3DP',
    'on every metric. Forces visitors to ask:',
    '"If this is so much better, why don\'t we do it?"',
    '',
    'The answer is policy, logistics, supply chains \u2014',
    'not technology. That\'s the real conversation.',
], size=9.5, leading=14.5)

# UX fix callout
panel(c, 415, 195, 370, 50, color=HexColor('#1a0f2e'))
c.setFillColor(YELLOW)
c.setFont('Helvetica-Bold', 8)
c.drawString(427, 225, 'UX DECISION')
c.setFillColor(TEXT)
c.setFont('Helvetica', 9)
c.drawString(427, 208, 'Build ONE method. Animate three. Same comparison, no fatigue.')

# White space bar
panel(c, 30, 30, 755, 50, color=HexColor('#0d1a2e'))
c.setFillColor(CYAN)
c.setFont('Helvetica-Bold', 9)
c.drawString(45, 60, 'WHITE SPACE')
c.setFillColor(TEXT)
c.setFont('Helvetica', 9)
c.drawString(45, 43, 'No existing project combines interactive tabletop assembly + projection-mapped LCA data + multi-method comparison.')
c.setFillColor(DIM)
c.setFont('Helvetica', 8)
c.drawString(45, 30, 'Refs: Gramazio Kohler Augmented Bricklaying (ETH) \u2022 Fologram Steampunk Pavilion (Tallinn 2019) \u2022 EPFL SXL reuse demonstrators \u2022 inFORM (MIT)')

# Slide number accent
c.setFillColor(ACCENT)
c.setFont('Helvetica-Bold', 60)
c.setFillColor(HexColor('#1a1a30'))
c.drawRightString(WIDTH - 25, HEIGHT - 75, '01')

c.showPage()

# ──────────────────────────────────────────────
# SLIDE 2: Interaction System
# ──────────────────────────────────────────────
bg(c)
footer(c, 2)

c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 30)
c.drawString(40, HEIGHT - 62, 'INTERACTION SYSTEM')
c.setFont('Helvetica', 14)
c.setFillColor(DIM)
c.drawString(40, HEIGHT - 83, 'Input \u2192 Processing \u2192 Output \u2192 Feedback loop')

c.setFillColor(HexColor('#1a1a30'))
c.setFont('Helvetica-Bold', 60)
c.drawRightString(WIDTH - 25, HEIGHT - 75, '02')

# Three columns: Input / Logic / Output
col_w = 240
gap = 15
start_x = 30

# INPUT
panel(c, start_x, 235, col_w, 240)
tag(c, start_x + 12, 455, 'INPUT', ACCENT2)
heading(c, start_x + 12, 432, 'Physical Placement', 12)
body(c, start_x + 12, 412, [
    'Overhead USB webcam reads ArUco',
    'fiducial markers on each piece.',
    '',
    'No touch. No gesture. No wearable.',
    'The act of building IS the input.',
    '',
    'Each marker encodes:',
], size=9.5, leading=13.5)
bullet(c, start_x + 12, 318, [
    'Piece ID (which block)',
    'Position (x, y on table)',
    'Rotation (\u03b8 orientation)',
], size=9, leading=13, bullet_color=ACCENT2)

# PROCESSING
panel(c, start_x + col_w + gap, 235, col_w, 240)
tag(c, start_x + col_w + gap + 12, 455, 'PROCESSING', PURPLE)
heading(c, start_x + col_w + gap + 12, 432, 'FSM + Validation', 12)
body(c, start_x + col_w + gap + 12, 412, [
    '5-state finite state machine:',
    'IDLE \u2192 READY \u2192 CHECKING',
    '\u2192 CONFIRMED / ERROR \u2192 COMPLETE',
    '',
    'Validation per method:',
], size=9.5, leading=13.5)
bullet(c, start_x + col_w + gap + 12, 340, [
    'Masonry: \u00b15mm position',
    '3DP: sequential layer order',
    'Prefab: \u00b110\u00b0 rotation',
    'Reused: irregular — wider tol.',
], size=9, leading=13, bullet_color=PURPLE)

# OUTPUT
panel(c, start_x + 2*(col_w + gap), 235, col_w, 240)
tag(c, start_x + 2*(col_w + gap) + 12, 455, 'OUTPUT', CYAN)
heading(c, start_x + 2*(col_w + gap) + 12, 432, 'Projection Feedback', 12)

feedback_items = [
    ('GUIDE', 'Target outline for next piece', CYAN),
    ('CONFIRM', 'Green pulse on valid placement', GREEN),
    ('DATA', 'CO\u2082 + hours + origin ON the piece', YELLOW),
    ('ERROR', 'Red outline + ghost correction', ACCENT),
    ('COMPARE', 'Final 4-method dashboard', PURPLE),
]
fy = 410
for label, desc, color in feedback_items:
    c.setFillColor(color)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(start_x + 2*(col_w + gap) + 12, fy, label)
    c.setFillColor(TEXT)
    c.setFont('Helvetica', 8.5)
    c.drawString(start_x + 2*(col_w + gap) + 70, fy, desc)
    fy -= 18

# Feedback loop bar at bottom
panel(c, 30, 90, 755, 130)
tag(c, 42, 200, 'FEEDBACK LOOP')

# Flow diagram
flow = [
    ('Place piece', ACCENT2, 55),
    ('Camera\ndetects', CYAN, 195),
    ('FSM\nvalidates', PURPLE, 335),
    ('Data projected\nON piece', YELLOW, 475),
    ('User reads\nplaces next', GREEN, 615),
]
for label, color, fx in flow:
    panel(c, fx, 110, 115, 60, color=DARK)
    lines = label.split('\n')
    c.setFillColor(color)
    c.setFont('Helvetica-Bold', 9.5)
    c.drawCentredString(fx + 57, 153 if len(lines) == 1 else 155, lines[0])
    if len(lines) > 1:
        c.setFont('Helvetica', 8.5)
        c.setFillColor(DIM)
        c.drawCentredString(fx + 57, 140, lines[1])

# Arrows
c.setStrokeColor(ACCENT)
c.setLineWidth(2)
for ax_pos in [170, 310, 450, 590]:
    c.line(ax_pos, 140, ax_pos + 25, 140)
    # arrowhead
    c.line(ax_pos + 20, 145, ax_pos + 25, 140)
    c.line(ax_pos + 20, 135, ax_pos + 25, 140)

# Loop back text
c.setFillColor(DIM)
c.setFont('Helvetica-Oblique', 8.5)
c.drawCentredString(400, 98, '\u2190 loop continues until all pieces placed \u2014 then method comparison triggers \u2192')

# Bonus features row
panel(c, 30, 25, 755, 55, color=HexColor('#1a0f2e'))
tag(c, 42, 58, 'BONUS FEATURES', YELLOW)

bonuses = [
    'Material-origin map ON each piece',
    'Carbon-budget clock ticking on table',
    'Failure states (misplace = animated collapse)',
    'LCA as ranges with sources, not single figures',
]
bx = 195
for b in bonuses:
    c.setFillColor(TEXT)
    c.setFont('Helvetica', 8)
    c.drawString(bx, 42, '\u2022 ' + b)
    bx += 185 if bx < 500 else 0
    if bx >= 500 + 185:
        break

# Reflow bonuses properly
c.setFillColor(TEXT)
c.setFont('Helvetica', 8)
c.drawString(195, 50, '\u2022 Material-origin map ON each piece            \u2022 Carbon-budget clock ticking on table')
c.drawString(195, 36, '\u2022 Failure states (misplace = animated collapse)  \u2022 LCA shown as ranges with sources')

c.showPage()

# ──────────────────────────────────────────────
# SLIDE 3: Architecture + Timeline + References
# ──────────────────────────────────────────────
bg(c)
footer(c, 3)

c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 30)
c.drawString(40, HEIGHT - 62, 'SYSTEM & TIMELINE')
c.setFont('Helvetica', 14)
c.setFillColor(DIM)
c.drawString(40, HEIGHT - 83, 'Tech stack, key references, and term schedule')

c.setFillColor(HexColor('#1a1a30'))
c.setFont('Helvetica-Bold', 60)
c.drawRightString(WIDTH - 25, HEIGHT - 75, '03')

# Tech stack panel — left
panel(c, 30, 280, 350, 200)
tag(c, 42, 460, 'TECH STACK')

stack = [
    ('Rhino / Grasshopper', 'Geometry + LCA data + assembly sequences', ACCENT2),
    ('TouchDesigner', 'Runtime: camera, FSM, projection mapping', CYAN),
    ('ArUco markers', 'Reliable tracking under projector light', GREEN),
    ('OSC bridge', 'GH \u2194 TD real-time communication', PURPLE),
    ('HD projector + webcam', 'Both overhead, closed feedback loop', YELLOW),
]
sy = 438
for name, desc, color in stack:
    c.setFillColor(color)
    c.setFont('Helvetica-Bold', 9.5)
    c.drawString(42, sy, name)
    c.setFillColor(DIM)
    c.setFont('Helvetica', 8)
    c.drawString(185, sy, desc)
    sy -= 26

# Why TouchDesigner callout
panel(c, 42, 290, 326, 42, color=HexColor('#1a0f2e'))
c.setFillColor(YELLOW)
c.setFont('Helvetica-Bold', 7.5)
c.drawString(52, 318, 'WHY NOT PURE GRASSHOPPER?')
c.setFillColor(DIM)
c.setFont('Helvetica', 7.5)
c.drawString(52, 304, 'GH is single-threaded. Anemone stalls canvas. Projector light')
c.drawString(52, 293, 'contaminates webcam. TD handles CV + projection natively.')

# References panel — right
panel(c, 395, 280, 390, 200)
tag(c, 407, 460, 'REFERENCES', CYAN)

refs = [
    ('Augmented Bricklaying', 'Gramazio Kohler, ETH', 'AR-guided masonry for complex facades'),
    ('Steampunk Pavilion', 'Fologram, Tallinn 2019', 'Public assembly via holographic guidance'),
    ('inFORM', 'MIT Tangible Media 2013', 'Canonical tangible data interaction'),
    ('EPFL SXL', 'Corentin Fivet', 'Reuse-driven structural pavilions'),
    ('Striatus Bridge', 'ZHA + BRG 2021', '3D-printed concrete at structural scale'),
    ('Material Cultures', 'London 2021\u2013', 'Bio-based construction comparisons'),
]
ry = 438
for title, org, desc in refs:
    c.setFillColor(TEXT)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(407, ry, title)
    c.setFillColor(CYAN)
    c.setFont('Helvetica', 7.5)
    c.drawString(555, ry, org)
    c.setFillColor(DIM)
    c.setFont('Helvetica', 7.5)
    c.drawString(407, ry - 11, desc)
    ry -= 28

# Timeline — full width bottom
panel(c, 30, 25, 755, 240)
tag(c, 42, 245, 'TERM TIMELINE')

# Session markers
sessions = [
    ('S1', 'Apr 10', 'Concept &\nProposal', ACCENT, 65),
    ('S2', 'Apr 17', 'Input &\nMapping', ACCENT2, 195),
    ('S3', 'May 4', 'FSM &\nLogic', PURPLE, 335),
    ('S4', 'May 11', 'Projection &\nFeedback', CYAN, 475),
    ('S5', 'May 18', 'Integration', GREEN, 600),
    ('FINAL', 'May 22', 'Presentation', YELLOW, 710),
]

for label, date, desc, color, sx in sessions:
    # Circle
    c.setFillColor(color)
    c.circle(sx + 20, 200, 14, fill=1, stroke=0)
    c.setFillColor(BG)
    c.setFont('Helvetica-Bold', 8)
    c.drawCentredString(sx + 20, 197, label)
    # Date
    c.setFillColor(DIM)
    c.setFont('Helvetica', 7.5)
    c.drawCentredString(sx + 20, 180, date)
    # Description
    c.setFillColor(TEXT)
    c.setFont('Helvetica', 8)
    dl = desc.split('\n')
    c.drawCentredString(sx + 20, 168, dl[0])
    if len(dl) > 1:
        c.drawCentredString(sx + 20, 157, dl[1])

# Connection line
c.setStrokeColor(DIM)
c.setLineWidth(1.5)
c.setDash(3, 3)
c.line(85, 200, 710, 200)
c.setDash()

# Gantt bars below
tasks_gantt = [
    ('Modules + Fabrication',    1, 3, ACCENT2),
    ('ArUco + Camera Pipeline',  1, 3, CYAN),
    ('LCA Data + Ranges',        1, 3, GREEN),
    ('FSM Implementation',       2, 4, PURPLE),
    ('Projection Mapping',       3, 5, YELLOW),
    ('Integration + Polish',     4, 5, ACCENT),
]

# Map session index to x position
session_x = [65, 195, 335, 475, 600, 710]
gy = 130
for name, s_start, s_end, color in tasks_gantt:
    x1 = session_x[s_start] + 20
    x2 = session_x[s_end] + 20
    c.setFillColor(color)
    c.roundRect(x1, gy, x2 - x1, 12, 3, fill=1, stroke=0)
    c.setFillColor(TEXT)
    c.setFont('Helvetica', 7.5)
    c.drawRightString(x1 - 8, gy + 2, name)
    gy -= 17

c.save()
print("Saved Proposal_v2.pdf")
