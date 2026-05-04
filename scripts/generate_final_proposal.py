"""
FINAL Proposal — aligned with the actual Hardware_III repo.
Team: Leo, Elais, Rafik, Seid, Onur, Nithik
Concept: 2-3 construction methods, build ALL physically, Anemone FSM
"""
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm

WIDTH, HEIGHT = landscape(A4)

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
    c.setFillColor(ACCENT)
    c.rect(0, HEIGHT - 3*mm, WIDTH, 3*mm, fill=1, stroke=0)

def footer(c, n):
    c.setFillColor(DIM)
    c.setFont('Helvetica', 7)
    c.drawString(30, 10, 'Guided Comparative Assembly Installation \u2014 Hardware III \u2014 MRAC+MAAI 2025/2026')
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

c = canvas.Canvas('Proposal_final.pdf', pagesize=landscape(A4))

# ──────────────────────────────────────────────
# SLIDE 1: Concept
# ──────────────────────────────────────────────
bg(c)
footer(c, 1)

c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 32)
c.drawString(40, HEIGHT - 62, 'Guided Comparative Assembly')
c.setFont('Helvetica', 14)
c.setFillColor(DIM)
c.drawString(40, HEIGHT - 84, 'Comparing construction methods through interactive physical assembly')

c.setFillColor(HexColor('#1a1a30'))
c.setFont('Helvetica-Bold', 60)
c.drawRightString(WIDTH - 25, HEIGHT - 75, '01')

# Team bar
panel(c, 30, HEIGHT - 120, 755, 22, color=DARK)
c.setFillColor(DIM)
c.setFont('Helvetica', 8.5)
c.drawString(42, HEIGHT - 114, 'Team: Leo \u2022 Elais \u2022 Rafik \u2022 Seid \u2022 Onur \u2022 Nithik    |    IAAC MRAC+MAAI 2025/2026    |    Instructors: Hamid Peiro, Aleksandra Kraeva')

# Mission
panel(c, 30, 310, 370, 170)
tag(c, 42, 460, 'MISSION')
body(c, 42, 438, [
    'We compare different statistics of the housing',
    'construction industry and display them through',
    'an interactive exhibit.',
    '',
    'An interactive table where users physically',
    'assemble 2\u20133 scale models of the same object \u2014',
    'each built with a different construction method.',
    '',
    'As each piece is placed, production data is',
    'mapped directly onto the object: CO\u2082, labor',
    'hours, material origin. The data becomes physical.',
], size=10, leading=15)

# Methods
panel(c, 415, 385, 370, 95)
tag(c, 427, 460, 'CONSTRUCTION METHODS', ACCENT2)

methods = [
    ('MASONRY', 'Brick by brick', 'Traditional', ACCENT2),
    ('3D PRINT', 'Layer by layer', 'Automated', CYAN),
    ('PREFAB', 'Panel by panel', 'Industrial', PURPLE),
]
for i, (name, sub, cat, color) in enumerate(methods):
    bx = 437 + i * 112
    panel(c, bx, 397, 100, 55, color=DARK)
    c.setFillColor(color)
    c.setFont('Helvetica-Bold', 10)
    c.drawCentredString(bx + 50, 435, name)
    c.setFillColor(DIM)
    c.setFont('Helvetica', 8)
    c.drawCentredString(bx + 50, 420, sub)
    c.drawCentredString(bx + 50, 408, cat)

# How it works
panel(c, 415, 310, 370, 65)
tag(c, 427, 355, 'THE POINT', GREEN)
body(c, 427, 333, [
    'Instead of reading abstract statistics, you build',
    'the comparison yourself \u2014 piece by piece.',
], size=10, leading=15)

# Flow diagram
panel(c, 30, 30, 755, 265)
tag(c, 42, 275, 'HOW IT WORKS')

steps = [
    ('1', 'Projector highlights\nnext piece placement', ACCENT2, 55),
    ('2', 'User places\nphysical piece', CYAN, 175),
    ('3', 'Camera confirms\ncorrect placement', PURPLE, 295),
    ('4', 'Data projected\nonto piece', YELLOW, 415),
    ('5', 'Repeat until\nmodel complete', GREEN, 535),
    ('6', 'Next method\nor comparison', ACCENT, 655),
]
for num, label, color, sx in steps:
    panel(c, sx, 180, 105, 65, color=DARK)
    c.setFillColor(color)
    c.setFont('Helvetica-Bold', 16)
    c.drawString(sx + 5, 225, num)
    lines = label.split('\n')
    c.setFont('Helvetica-Bold', 9)
    c.drawString(sx + 25, 228, lines[0])
    c.setFont('Helvetica', 8.5)
    c.setFillColor(TEXT)
    c.drawString(sx + 25, 214, lines[1])

# Arrows between steps
c.setStrokeColor(ACCENT)
c.setLineWidth(1.5)
for ax_pos in [160, 280, 400, 520, 640]:
    c.line(ax_pos, 212, ax_pos + 15, 212)
    c.line(ax_pos + 10, 217, ax_pos + 15, 212)
    c.line(ax_pos + 10, 207, ax_pos + 15, 212)

# Data projected details
body(c, 42, 160, [
    'Data projected per piece:',
], size=9.5, leading=14, color=DIM)
data_items = [
    ('CO\u2082 consumption', ACCENT2, 42),
    ('Labor hours', CYAN, 200),
    ('Material origin', GREEN, 340),
    ('Production method', PURPLE, 500),
]
for label, color, dx in data_items:
    c.setFillColor(color)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(dx, 142, '\u25cf')
    c.setFillColor(TEXT)
    c.setFont('Helvetica', 9)
    c.drawString(dx + 12, 142, label)

# Final comparison note
body(c, 42, 110, [
    'Once all models are complete, a full comparison is projected across the table:',
    'total CO\u2082, total labor, total cost \u2014 side by side.',
], size=9.5, leading=14)

# Proximity sensor feature
body(c, 42, 70, [
    'Bonus: Arduino proximity sensor \u2014 user leans in \u2192 data zooms for detail.',
], size=9, leading=14, color=DIM)

c.showPage()

# ──────────────────────────────────────────────
# SLIDE 2: Interaction System + FSM
# ──────────────────────────────────────────────
bg(c)
footer(c, 2)

c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 30)
c.drawString(40, HEIGHT - 62, 'Interaction System & FSM')
c.setFont('Helvetica', 14)
c.setFillColor(DIM)
c.drawString(40, HEIGHT - 83, 'Input \u2192 Processing \u2192 Output \u2192 Feedback loop')

c.setFillColor(HexColor('#1a1a30'))
c.setFont('Helvetica-Bold', 60)
c.drawRightString(WIDTH - 25, HEIGHT - 75, '02')

# Three columns
col_w = 230
gap = 15
sx = 30

# INPUT
panel(c, sx, 270, col_w, 210)
tag(c, sx + 12, 460, 'INPUT', ACCENT2)
heading(c, sx + 12, 438, 'Physical Placement + Proximity', 11)
body(c, sx + 12, 418, [
    'Overhead USB webcam detects',
    'piece placement on the table.',
    '',
    'Arduino/ESP32 proximity sensor',
    'detects when user leans in \u2192',
    'triggers data zoom on piece.',
    '',
    'Human action = building.',
    'The act of assembly IS the input.',
], size=9.5, leading=14)

# PROCESSING
panel(c, sx + col_w + gap, 270, col_w, 210)
tag(c, sx + col_w + gap + 12, 460, 'PROCESSING', PURPLE)
heading(c, sx + col_w + gap + 12, 438, 'Grasshopper + Anemone FSM', 11)
body(c, sx + col_w + gap + 12, 418, [
    'Rhino/Grasshopper: geometry,',
    'assembly sequence, LCA data.',
    '',
    'Anemone: FSM loop logic.',
    'Firefly: webcam data stream',
    'into Grasshopper.',
    '',
    'Validation: compare detected',
    'position vs target placement.',
], size=9.5, leading=14)

# OUTPUT
panel(c, sx + 2*(col_w + gap), 270, col_w, 210)
tag(c, sx + 2*(col_w + gap) + 12, 460, 'OUTPUT', CYAN)
heading(c, sx + 2*(col_w + gap) + 12, 438, 'Projection Feedback', 11)

feedback_items = [
    ('GUIDE', 'Highlight next placement', CYAN),
    ('CONFIRM', 'Green flash on valid piece', GREEN),
    ('DATA', 'CO\u2082 + hours + origin overlay', YELLOW),
    ('ERROR', 'Ghost guide for correction', ACCENT),
    ('COMPARE', 'Final side-by-side stats', PURPLE),
]
fy = 418
for label, desc, color in feedback_items:
    c.setFillColor(color)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(sx + 2*(col_w + gap) + 12, fy, label)
    c.setFillColor(TEXT)
    c.setFont('Helvetica', 8.5)
    c.drawString(sx + 2*(col_w + gap) + 70, fy, desc)
    fy -= 20

# Projection tool
body(c, sx + 2*(col_w + gap) + 12, fy - 5, [
    'TouchDesigner / HeavyM for',
    'projection mapping layer.',
], size=9, leading=13, color=DIM)

# FSM Diagram — bottom section
panel(c, 30, 25, 755, 230)
tag(c, 42, 235, 'FINITE STATE MACHINE')

# FSM states as boxes
fsm_states = [
    ('IDLE', 'Waiting for user\nAmbient pattern', DIM, 55, 155),
    ('GUIDING', 'Projector highlights\nnext piece target', ACCENT2, 185, 155),
    ('CHECKING', 'Camera validates\nplacement', PURPLE, 315, 155),
    ('CONFIRMED', 'Data projected\non piece', GREEN, 445, 155),
    ('NEXT_PIECE', 'Advance to\nnext piece', CYAN, 445, 70),
    ('ERROR', 'Ghost guide\nshown', ACCENT, 315, 70),
    ('MODEL_COMPLETE', 'Method stats\nsummary', YELLOW, 185, 70),
    ('NEXT_MODEL', 'Switch to\nnext method', ACCENT2, 55, 70),
    ('COMPARISON', 'Side-by-side\nfinal stats', HexColor('#00d4ff'), 610, 112),
]

for name, subtitle, color, fx, fy_pos in fsm_states:
    bw = 115 if len(name) <= 10 else 130
    panel(c, fx, fy_pos, bw, 52, color=DARK)
    c.setFillColor(color)
    c.setFont('Helvetica-Bold', 8.5 if len(name) <= 10 else 7.5)
    c.drawCentredString(fx + bw/2, fy_pos + 37, name)
    lines = subtitle.split('\n')
    c.setFillColor(DIM)
    c.setFont('Helvetica', 7)
    c.drawCentredString(fx + bw/2, fy_pos + 23, lines[0])
    if len(lines) > 1:
        c.drawCentredString(fx + bw/2, fy_pos + 14, lines[1])

# Arrows for FSM
c.setStrokeColor(ACCENT)
c.setLineWidth(1.5)
# IDLE → GUIDING
c.line(170, 181, 185, 181)
# GUIDING → CHECKING
c.line(300, 181, 315, 181)
# CHECKING → CONFIRMED
c.line(430, 181, 445, 181)
# CHECKING → ERROR (down)
c.line(372, 155, 372, 122)
# ERROR → GUIDING (left + up)
c.line(315, 96, 240, 96)
c.line(240, 96, 240, 155)
# CONFIRMED → NEXT_PIECE (down)
c.line(502, 155, 502, 122)
# NEXT_PIECE → GUIDING (loop back)
c.setDash(3, 2)
c.line(445, 96, 240, 50)
c.line(240, 50, 240, 155)
c.setDash()
# CONFIRMED (last) → MODEL_COMPLETE
c.setStrokeColor(YELLOW)
c.line(445, 170, 315, 96)
# MODEL_COMPLETE → NEXT_MODEL
c.line(185, 96, 170, 96)
# NEXT_MODEL → GUIDING (up)
c.setStrokeColor(ACCENT2)
c.line(112, 122, 112, 145)
c.line(112, 145, 185, 170)
# MODEL_COMPLETE (last) → COMPARISON
c.setStrokeColor(CYAN)
c.line(315, 96, 610, 130)

c.showPage()

# ──────────────────────────────────────────────
# SLIDE 3: Tech Stack + Timeline + References
# ──────────────────────────────────────────────
bg(c)
footer(c, 3)

c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 30)
c.drawString(40, HEIGHT - 62, 'Tech Stack & Timeline')
c.setFont('Helvetica', 14)
c.setFillColor(DIM)
c.drawString(40, HEIGHT - 83, 'Tools, phases, and key reference')

c.setFillColor(HexColor('#1a1a30'))
c.setFont('Helvetica-Bold', 60)
c.drawRightString(WIDTH - 25, HEIGHT - 75, '03')

# Tech stack
panel(c, 30, 280, 370, 200)
tag(c, 42, 460, 'TECH STACK')

stack = [
    ('Rhino + Grasshopper', 'Main logic environment', ACCENT2),
    ('Anemone (GH plugin)', 'FSM loop logic', PURPLE),
    ('Firefly (GH plugin)', 'Webcam/sensor \u2192 GH data stream', CYAN),
    ('TouchDesigner / HeavyM', 'Projection mapping + visual output', YELLOW),
    ('Arduino / ESP32', 'Proximity sensor (lean in \u2192 zoom)', GREEN),
    ('USB webcam (overhead)', 'Piece placement detection', ACCENT2),
    ('Video projector (top-down)', 'Guided projection on table', CYAN),
]
sy = 438
for name, desc, color in stack:
    c.setFillColor(color)
    c.setFont('Helvetica-Bold', 9)
    c.drawString(42, sy, name)
    c.setFillColor(DIM)
    c.setFont('Helvetica', 8)
    c.drawString(210, sy, desc)
    sy -= 22

# Reference
panel(c, 415, 380, 370, 100)
tag(c, 427, 460, 'KEY REFERENCE', CYAN)
body(c, 427, 438, [
    'Stefana Parascho \u2014 Cooperative Robotic Assembly',
    '(ETH Diss. 25839)',
    '',
    'Assembly sequence as FSM: each intermediate',
    'state must be structurally valid before the next',
    'step is permitted. Directly maps to our approach.',
], size=9.5, leading=14)

# Additional references
panel(c, 415, 280, 370, 90)
tag(c, 427, 350, 'MORE REFERENCES', DIM)
body(c, 427, 328, [
    'Gramazio Kohler \u2014 Augmented Bricklaying (ETH)',
    'Fologram \u2014 Steampunk Pavilion (Tallinn 2019)',
    'inFORM \u2014 MIT Tangible Media Group (2013)',
    'EPFL SXL \u2014 Reuse-driven structural pavilions',
], size=9, leading=14, color=DIM)

# Timeline
panel(c, 30, 25, 755, 240)
tag(c, 42, 245, 'PROJECT PHASES')

phases = [
    ('Phase 1', 'Proposal & FSM\nFoundation', 'Apr 17', ACCENT, 55),
    ('Phase 2', 'Data Research &\nPhysical Models', 'May 4', ACCENT2, 180),
    ('Phase 3', 'FSM Implementation\n& Assembly Logic', 'May 4', PURPLE, 305),
    ('Phase 4', 'Human-in-the-Loop\nAssembly & Sound', 'May 11', CYAN, 430),
    ('Phase 5', 'Projection Mapping\n& Comparison', 'May 18', GREEN, 555),
    ('Phase 6', 'Integration\nTesting & Finals', 'May 22', YELLOW, 680),
]

for label, desc, deadline, color, px in phases:
    panel(c, px, 140, 110, 75, color=DARK)
    c.setFillColor(color)
    c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(px + 55, 200, label)
    lines = desc.split('\n')
    c.setFillColor(TEXT)
    c.setFont('Helvetica', 8)
    c.drawCentredString(px + 55, 185, lines[0])
    if len(lines) > 1:
        c.drawCentredString(px + 55, 174, lines[1])
    c.setFillColor(DIM)
    c.setFont('Helvetica', 7.5)
    c.drawCentredString(px + 55, 148, deadline)

# Connection line
c.setStrokeColor(DIM)
c.setLineWidth(1.5)
c.setDash(3, 3)
c.line(165, 178, 680, 178)
c.setDash()

# Gantt bars
tasks_g = [
    ('Proposal + FSM sketch',       0, 1, ACCENT),
    ('LCA data + model fabrication', 1, 3, ACCENT2),
    ('FSM in Anemone + detection',   2, 4, PURPLE),
    ('Guided assembly loop + sound', 3, 4, CYAN),
    ('Projection mapping + stats',   4, 5, GREEN),
    ('Integration + testing',        4, 6, YELLOW),
]
phase_x = [55, 180, 305, 430, 555, 680]
gy = 118
for name, s_start, s_end, color in tasks_g:
    x1 = phase_x[s_start] + 55
    x2 = phase_x[min(s_end, 5)] + 55
    c.setFillColor(color)
    c.roundRect(x1, gy, x2 - x1, 10, 3, fill=1, stroke=0)
    c.setFillColor(TEXT)
    c.setFont('Helvetica', 7)
    c.drawRightString(x1 - 5, gy + 1, name)
    gy -= 15

c.save()
print("Saved Proposal_final.pdf")
