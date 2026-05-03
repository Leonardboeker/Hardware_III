"""Generate 3-slide proposal as PDF for the Interactive Assembly Installation."""
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.units import cm, mm

WIDTH, HEIGHT = landscape(A4)

# Colors
BG = HexColor('#1a1a2e')
ACCENT = HexColor('#e94560')
TEXT = HexColor('#eaeaea')
SUBTITLE = HexColor('#a3a3c2')
DARK_PANEL = HexColor('#16213e')
GREEN = HexColor('#2d6a4f')
ORANGE = HexColor('#f97316')
CYAN = HexColor('#06b6d4')
PURPLE = HexColor('#8b5cf6')

def draw_bg(c):
    c.setFillColor(BG)
    c.rect(0, 0, WIDTH, HEIGHT, fill=1, stroke=0)
    # accent line top
    c.setFillColor(ACCENT)
    c.rect(0, HEIGHT - 4*mm, WIDTH, 4*mm, fill=1, stroke=0)

def draw_footer(c, slide_num):
    c.setFillColor(SUBTITLE)
    c.setFont('Helvetica', 8)
    c.drawString(30, 15, 'Interactive Assembly Installation — Hardware III — MRAC 2025/2026')
    c.drawRightString(WIDTH - 30, 15, f'{slide_num}/3')

def draw_panel(c, x, y, w, h, color=DARK_PANEL):
    c.setFillColor(color)
    c.roundRect(x, y, w, h, 6, fill=1, stroke=0)

def text_block(c, x, y, lines, font='Helvetica', size=11, color=TEXT, leading=16):
    """Draw multiple lines of text, returns final y."""
    c.setFont(font, size)
    c.setFillColor(color)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


# ──────────────────────────────────────────────
# SLIDE 1: Concept & Modules
# ──────────────────────────────────────────────
c = canvas.Canvas('Proposal_slides.pdf', pagesize=landscape(A4))

draw_bg(c)
draw_footer(c, 1)

# Title
c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 28)
c.drawString(40, HEIGHT - 60, 'Comparative Assembly')
c.setFont('Helvetica', 14)
c.setFillColor(SUBTITLE)
c.drawString(40, HEIGHT - 82, 'How Construction Methods Shape What We Build')

# Left panel — Concept
draw_panel(c, 30, 180, 370, 310)
c.setFillColor(ACCENT)
c.setFont('Helvetica-Bold', 13)
c.drawString(45, 470, 'CONCEPT')

text_block(c, 45, 448, [
    'A tabletop installation where the user physically',
    'assembles a small wall section, guided by a projector.',
    '',
    'The projector overlays real-time LCA data directly',
    'onto each physical piece as it is placed: CO\u2082 cost,',
    'labor hours, and material supply chain.',
    '',
    'Three construction methods are compared through',
    'the same final form — same wall, different process,',
    'different environmental footprint.',
    '',
    'The data becomes physical. You don\'t read a chart —',
    'you build both versions and feel the difference.',
], size=10.5, leading=16.5)

# Middle panel — Modules
draw_panel(c, 410, 330, 185, 160)
c.setFillColor(ORANGE)
c.setFont('Helvetica-Bold', 11)
c.drawString(422, 470, 'MODULES')
text_block(c, 422, 448, [
    'Masonry bricks',
    '  4 x 2 x 1.5 cm blocks',
    '',
    '3DP concrete layers',
    '  8 x 2 x 0.5 cm strips',
    '',
    'Prefab panels',
    '  8 x 4 x 1 cm units',
], size=9.5, leading=14, color=TEXT)

# Right panel — Connection Logic
draw_panel(c, 605, 330, 185, 160)
c.setFillColor(CYAN)
c.setFont('Helvetica-Bold', 11)
c.drawString(617, 470, 'CONNECTION LOGIC')
text_block(c, 617, 448, [
    'Masonry: gravity stack',
    '  \u00b15mm position tolerance',
    '',
    '3DP: sequential layers',
    '  layer N after N-1 only',
    '',
    'Prefab: slot alignment',
    '  \u00b110\u00b0 rotation tolerance',
], size=9.5, leading=14, color=TEXT)

# Bottom panel — Final Object
draw_panel(c, 410, 180, 380, 140)
c.setFillColor(GREEN)
c.setFont('Helvetica-Bold', 11)
c.drawString(422, 300, 'FINAL ASSEMBLED OBJECT')
text_block(c, 422, 278, [
    'A small wall section (\u224825 x 20 cm) built three times,',
    'each with a different construction method.',
    '',
    'All modules laser-cut or 3D-printed at tabletop scale.',
    'ArUco fiducial markers on underside for camera tracking.',
], size=9.5, leading=14, color=TEXT)

# White space callout
draw_panel(c, 30, 40, 760, 50, color=HexColor('#2a1a3e'))
c.setFillColor(ACCENT)
c.setFont('Helvetica-Bold', 10)
c.drawString(45, 68, 'WHITE SPACE')
c.setFillColor(TEXT)
c.setFont('Helvetica', 9.5)
c.drawString(45, 50, 'No existing project combines interactive tabletop assembly + projection-mapped LCA data + construction method comparison.')

c.showPage()

# ──────────────────────────────────────────────
# SLIDE 2: Interaction & Feedback
# ──────────────────────────────────────────────
draw_bg(c)
draw_footer(c, 2)

c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 28)
c.drawString(40, HEIGHT - 60, 'Interaction & Feedback')
c.setFont('Helvetica', 14)
c.setFillColor(SUBTITLE)
c.drawString(40, HEIGHT - 82, 'Human input \u2192 System logic \u2192 Projection output')

# Input panel
draw_panel(c, 30, 260, 240, 220)
c.setFillColor(ORANGE)
c.setFont('Helvetica-Bold', 12)
c.drawString(45, 460, 'INPUT')
c.setFillColor(SUBTITLE)
c.setFont('Helvetica', 9)
c.drawString(45, 444, 'What human action drives the system?')

text_block(c, 45, 420, [
    'Physical object placement',
    '',
    'Overhead USB webcam reads',
    'ArUco markers on each piece.',
    '',
    'No touch. No gesture.',
    'The act of building IS',
    'the input.',
    '',
    'Marker gives: piece ID,',
    'position (x,y), rotation (\u03b8)',
], size=10, leading=14.5, color=TEXT)

# Processing panel
draw_panel(c, 285, 260, 220, 220)
c.setFillColor(PURPLE)
c.setFont('Helvetica-Bold', 12)
c.drawString(300, 460, 'PROCESSING')
c.setFillColor(SUBTITLE)
c.setFont('Helvetica', 9)
c.drawString(300, 444, 'FSM + validation rules')

text_block(c, 300, 420, [
    '5-state FSM controls flow:',
    'IDLE \u2192 READY \u2192 CHECKING',
    '\u2192 CONFIRMED / ERROR',
    '\u2192 COMPLETE',
    '',
    'Validation rule:',
    'Compare detected marker',
    'position/rotation against',
    'target within tolerance.',
    '',
    'LCA database lookup per piece.',
], size=10, leading=14.5, color=TEXT)

# Output panel
draw_panel(c, 520, 260, 270, 220)
c.setFillColor(ACCENT)
c.setFont('Helvetica-Bold', 12)
c.drawString(535, 460, 'OUTPUT (Projection)')
c.setFillColor(SUBTITLE)
c.setFont('Helvetica', 9)
c.drawString(535, 444, 'What does projection feedback do?')

text_block(c, 535, 420, [
    'GUIDE    Target outline for next piece',
    'CONFIRM  Green pulse on valid placement',
    'INFORM   LCA data projected ON the piece:',
    '            \u2022 CO\u2082 (kg)',
    '            \u2022 Labor (hours)',
    '            \u2022 Material origin map',
    'ERROR    Red outline + ghost correction',
    'COMPARE  Final side-by-side dashboard',
], size=10, leading=14.5, color=TEXT)

# Feedback loop diagram
draw_panel(c, 30, 80, 760, 160)
c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 11)
c.drawString(45, 220, 'THE FEEDBACK LOOP')

# Flow boxes
flow_items = [
    ('User places\npiece', ORANGE, 80),
    ('Camera detects\nArUco marker', CYAN, 230),
    ('FSM validates\nposition', PURPLE, 380),
    ('Projector overlays\nLCA data on piece', ACCENT, 530),
    ('User sees feedback\nplaces next piece', GREEN, 680),
]
for label, color, x in flow_items:
    draw_panel(c, x, 110, 120, 55, color=color)
    lines = label.split('\n')
    c.setFillColor(TEXT)
    c.setFont('Helvetica-Bold', 9)
    c.drawCentredString(x + 60, 148, lines[0])
    c.setFont('Helvetica', 8.5)
    c.drawCentredString(x + 60, 134, lines[1])

# Arrows between flow boxes
c.setStrokeColor(ACCENT)
c.setLineWidth(2)
for x in [200, 350, 500, 650]:
    c.line(x, 137, x + 30, 137)
    c.line(x + 25, 142, x + 30, 137)
    c.line(x + 25, 132, x + 30, 137)

# Loop-back arrow text
c.setFillColor(SUBTITLE)
c.setFont('Helvetica-Oblique', 9)
c.drawCentredString(420, 95, '\u2190 loop continues until all pieces placed for current method \u2192')

c.showPage()

# ──────────────────────────────────────────────
# SLIDE 3: System Architecture & References
# ──────────────────────────────────────────────
draw_bg(c)
draw_footer(c, 3)

c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 28)
c.drawString(40, HEIGHT - 60, 'System Architecture')
c.setFont('Helvetica', 14)
c.setFillColor(SUBTITLE)
c.drawString(40, HEIGHT - 82, 'Tech stack, references, and timeline')

# Tech stack panel
draw_panel(c, 30, 280, 370, 200)
c.setFillColor(ACCENT)
c.setFont('Helvetica-Bold', 12)
c.drawString(45, 460, 'TECH STACK')

stack_items = [
    ('Rhino / Grasshopper', 'Geometry, LCA data, assembly sequence design'),
    ('TouchDesigner', 'Runtime: camera input, projection output, FSM'),
    ('ArUco markers', 'Fiducial tracking under projector light'),
    ('HD Projector', 'Overhead, projection-maps onto table + pieces'),
    ('USB Webcam', 'Overhead, feeds marker detection pipeline'),
    ('OSC Bridge', 'Grasshopper \u2194 TouchDesigner communication'),
]
y = 438
for title, desc in stack_items:
    c.setFillColor(CYAN)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(45, y, title)
    c.setFillColor(SUBTITLE)
    c.setFont('Helvetica', 8.5)
    c.drawString(200, y, desc)
    y -= 22

# System diagram panel
draw_panel(c, 30, 100, 370, 165)
c.setFillColor(ORANGE)
c.setFont('Helvetica-Bold', 12)
c.drawString(45, 245, 'SYSTEM DIAGRAM')

# Simple flow
sys_items = [
    ('Physical pieces + ArUco', 70, 205),
    ('Overhead webcam', 170, 205),
    ('Processing (TD/GH)', 270, 205),
    ('Overhead projector', 170, 145),
    ('Table surface', 270, 145),
]

for label, x, y_pos in sys_items:
    c.setFillColor(TEXT)
    c.setFont('Helvetica', 8.5)
    c.drawCentredString(x, y_pos, label)

c.setStrokeColor(ACCENT)
c.setLineWidth(1.5)
# pieces → webcam
c.line(110, 210, 140, 210)
# webcam → processing
c.line(205, 210, 235, 210)
# processing → projector
c.line(270, 200, 210, 160)
# projector → table
c.line(210, 150, 240, 150)

c.setFillColor(SUBTITLE)
c.setFont('Helvetica-Oblique', 8)
c.drawCentredString(200, 118, '\u2190 Closed feedback loop: place \u2192 detect \u2192 validate \u2192 project \u2192 place \u2192')

# References panel
draw_panel(c, 415, 100, 375, 380)
c.setFillColor(ACCENT)
c.setFont('Helvetica-Bold', 12)
c.drawString(430, 460, 'KEY REFERENCES')

refs = [
    ('Augmented Bricklaying', 'Gramazio Kohler Research, ETH Zurich', 'AR-guided masons placing bricks for complex facades'),
    ('Steampunk Pavilion', 'Fologram + Gwyllim Jahn, Tallinn 2019', 'Untrained builders assembling curved timber via AR'),
    ('inFORM', 'Hiroshi Ishii / MIT Tangible Media, 2013', 'Canonical "data you can touch" reference'),
    ('Material Cultures', 'London, 2021\u2013', 'Bio-based comparison demonstrators'),
    ('Striatus Bridge', 'ZHA + Block Research Group, 2021', '3D-printed concrete structural demonstration'),
    ('EPFL Structural Xploration Lab', 'Corentin Fivet', 'Pavilions from reclaimed components, carbon-driven'),
]

y = 438
for title, org, desc in refs:
    c.setFillColor(TEXT)
    c.setFont('Helvetica-Bold', 10)
    c.drawString(430, y, title)
    c.setFillColor(CYAN)
    c.setFont('Helvetica', 8.5)
    c.drawString(430, y - 13, org)
    c.setFillColor(SUBTITLE)
    c.setFont('Helvetica', 8)
    c.drawString(430, y - 25, desc)
    y -= 50

# Timeline mini
draw_panel(c, 30, 20, 760, 65, color=HexColor('#2a1a3e'))
c.setFillColor(TEXT)
c.setFont('Helvetica-Bold', 10)
c.drawString(45, 62, 'TIMELINE')

timeline = ['S1 Apr 10: Concept', 'S2 Apr 17: Mapping', 'S3 May 4: FSM', 'S4 May 11: Projection', 'S5 May 18: Integration', 'Finals May 22']
x = 45
for item in timeline:
    c.setFillColor(SUBTITLE)
    c.setFont('Helvetica', 8.5)
    c.drawString(x, 38, item)
    x += 128

c.save()
print("Saved Proposal_slides.pdf")
