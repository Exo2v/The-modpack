#!/usr/bin/env python3
"""
=============================================================================
ASHENFALL: Master World Map & Geological Specification PDF Generator
Compiles a publication-grade, exhaustive PDF document covering:
  1. Heightmap Data & Elevation Formulas (uint16, sea level, shelf dropoff)
  2. Landformations & Exact Coordinates for All 9 Cardinal Regions
  3. Lithosphere Biomes, Spline Density Functions & Multi-Noise Mapping
  4. Temperature Gradients, Altitude Lapse Rates & Biome Blending Laws
  5. Population Instructions: Forcing Still Life Chunk Decoration
=============================================================================
"""

import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_PDF = BASE_DIR / "docs" / "ASHENFALL_WORLD_MAP_MASTER_SPECIFICATION.pdf"
OUTPUT_MD = BASE_DIR / "docs" / "ASHENFALL_WORLD_MAP_MASTER_SPECIFICATION.md"

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Suppress running header on title page

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Running Header
        self.drawString(54, 750, "ASHENFALL GEOLOGICAL SPECIFICATION: Master Continent of Vantyra")
        self.drawRightString(612 - 54, 750, "Lithosphere & Still Life Engine")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 744, 612 - 54, 744)

        # Running Footer
        self.line(54, 45, 612 - 54, 45)
        self.drawString(54, 34, "Ashenfall: The Broken Realm · Master World Map Specification · Minecraft 1.21.1 NeoForge")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 34, page_str)
        self.restoreState()


def build_pdf_and_markdown():
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(OUTPUT_PDF),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Typography & Palette
    c_primary = colors.HexColor("#0f172a")     # Slate 900
    c_accent = colors.HexColor("#0284c7")      # Sky 600
    c_ember = colors.HexColor("#ea580c")       # Orange 600
    c_emerald = colors.HexColor("#059669")     # Emerald 600
    c_secondary = colors.HexColor("#334155")   # Slate 700
    c_muted = colors.HexColor("#64748b")       # Slate 500
    c_box_bg = colors.HexColor("#f8fafc")      # Slate 50
    c_box_border = colors.HexColor("#cbd5e1")  # Slate 300

    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=22, leading=26,
        textColor=c_primary, spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=12, leading=15,
        textColor=c_accent, spaceAfter=10
    )
    meta_style = ParagraphStyle(
        'MetaStyle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=11,
        textColor=c_muted, spaceAfter=12
    )
    h1_style = ParagraphStyle(
        'H1', parent=styles['Heading1'],
        fontName='Helvetica-Bold', fontSize=13.5, leading=17,
        textColor=c_primary, spaceBefore=14, spaceAfter=6, keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'H2', parent=styles['Heading2'],
        fontName='Helvetica-Bold', fontSize=10.5, leading=14,
        textColor=c_accent, spaceBefore=10, spaceAfter=4, keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.8, leading=12.5,
        textColor=c_secondary, alignment=TA_JUSTIFY, spaceAfter=5
    )
    bullet_style = ParagraphStyle(
        'Bullet', parent=body_style,
        leftIndent=12, firstLineIndent=-8, spaceAfter=2.5
    )
    code_style = ParagraphStyle(
        'CodeStyle', parent=styles['Normal'],
        fontName='Courier', fontSize=7.2, leading=9.5,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderPadding=5, spaceBefore=3, spaceAfter=5
    )
    box_text_style = ParagraphStyle(
        'BoxText', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12,
        textColor=colors.HexColor("#1e293b")
    )

    story = []

    # -------------------------------------------------------------------------
    # HEADER
    # -------------------------------------------------------------------------
    story.append(Paragraph("Ashenfall: Master World Map & Geological Specification", title_style))
    story.append(Paragraph("Complete Technical Data: Heightmaps, Coordinates, Lithosphere Splines, Climate Gradients & Still Life Population", subtitle_style))
    story.append(Paragraph("<b>Target Engine:</b> Minecraft 1.21.1 (Pack 48) · <b>Canvas:</b> 8,000 × 8,000 Blocks · <b>World:</b> Continent of Vantyra · <b>Author:</b> Ashenfall Engineering", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=0, spaceAfter=10))

    # Executive Overview Box
    exec_summary = """<b>MASTER WORLDGEN BLUEPRINT:</b> This document provides the definitive, production-grade specification for generating the finite 8,000 × 8,000 block continent of Vantyra. It establishes: (1) Exact 16-bit uint16 heightmap conversion math and Hermite continental shelf dropoff equations; (2) Spatial bounding boxes, target elevations, and coordinates for all 9 cardinal landmarks; (3) Lithosphere cubic spline density function mappings (continents, erosion, ridges); (4) The 5-dimensional multi-noise climate tensor, thermal lapse formulas, and anti-snow-pocket buffer rules; and (5) The 3 deterministic methodologies to force Still Life flora and feature decoration (fallen logs, mossy boulders, multi-tier canopies) across habitable sectors while preserving barren calderas and sheer cliffs."""
    c_table = Table([[Paragraph(exec_summary, box_text_style)]], colWidths=[504])
    c_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_box_bg),
        ('BOX', (0,0), (-1,-1), 1, c_box_border),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(c_table)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # SECTION 1: HEIGHTMAP DATA & ELEVATION SPECIFICATION
    # -------------------------------------------------------------------------
    story.append(Paragraph("1. Heightmap Data & Elevation Mathematical Specification", h1_style))
    story.append(Paragraph("The continent of Vantyra operates on Minecraft 1.21.1's extended world height ceiling: <b>Y = -64 to Y = 320</b> (Total: 384 vertical blocks). Sea level is anchored at <b>Y = 62</b>.", body_style))
    story.append(Paragraph("<b>16-Bit uint16 Normalization Equation:</b> Every pixel in the master heightfield maps directly to a discrete block height through linear transformation:", body_style))
    
    code_h_math = """h_norm = (Y - min_y) / (max_y - min_y) = (Y + 64.0) / 384.0
uint16_value = round(h_norm * 65535.0)
Y_block = -64.0 + (uint16_value / 65535.0) * 384.0"""
    story.append(Paragraph(code_h_math.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    # Elevation Keypoint Table
    h_data = [
        [Paragraph("<b>Geological Feature</b>", meta_style), Paragraph("<b>Target Y Block</b>", meta_style), Paragraph("<b>Norm [0..1]</b>", meta_style), Paragraph("<b>16-Bit uint16</b>", meta_style), Paragraph("<b>Lithosphere Layer / Material</b>", meta_style)],
        [Paragraph("Bedrock Floor", body_style), Paragraph("Y = -64.0", body_style), Paragraph("0.0000", body_style), Paragraph("0", body_style), Paragraph("Solid Bedrock Floor", body_style)],
        [Paragraph("Abyssal Trench (Veil of Salt)", body_style), Paragraph("Y = -32.0 to 10.0", body_style), Paragraph("0.0833 - 0.1927", body_style), Paragraph("5,461 - 12,629", body_style), Paragraph("Deep Cold Ocean / Gravel", body_style)],
        [Paragraph("Sunken Caldera Crater Floor", body_style), Paragraph("Y = 38.0 - 42.0", body_style), Paragraph("0.2656 - 0.2760", body_style), Paragraph("17,406 - 18,088", body_style), Paragraph("Basalt / Lava Basins / Netherite", body_style)],
        [Paragraph("Sunken Reach Drowned Shelf", body_style), Paragraph("Y = 52.0 - 56.0", body_style), Paragraph("0.3021 - 0.3125", body_style), Paragraph("19,798 - 20,480", body_style), Paragraph("Warm Ocean Reefs / Sandbars", body_style)],
        [Paragraph("<b>Mean Sea Level (Water Line)</b>", body_style), Paragraph("<b>Y = 62.0</b>", body_style), Paragraph("<b>0.3281</b>", body_style), Paragraph("<b>21,504</b>", body_style), Paragraph("<b>Water Surface / Sea Surface</b>", body_style)],
        [Paragraph("Forgotten Coast Shoreline", body_style), Paragraph("Y = 68.0 - 74.0", body_style), Paragraph("0.3438 - 0.3594", body_style), Paragraph("22,532 - 23,556", body_style), Paragraph("Stony Shore / Cold Pebble Beaches", body_style)],
        [Paragraph("Gilded Dunes Low Mesas", body_style), Paragraph("Y = 82.0 - 96.0", body_style), Paragraph("0.3802 - 0.4167", body_style), Paragraph("24,917 - 27,307", body_style), Paragraph("Terracotta / Red Sandstone", body_style)],
        [Paragraph("Cogwork March Quarry Benches", body_style), Paragraph("Y = 85.0 - 110.0", body_style), Paragraph("0.3880 - 0.4531", body_style), Paragraph("25,428 - 29,695", body_style), Paragraph("Terraced Badlands (9m steps)", body_style)],
        [Paragraph("Caldera Volcanic Rim", body_style), Paragraph("Y = 142.0 - 156.0", body_style), Paragraph("0.5365 - 0.5729", body_style), Paragraph("35,158 - 37,548", body_style), Paragraph("Blackstone / Basalt Spines", body_style)],
        [Paragraph("Subalpine Taiga Foothills", body_style), Paragraph("Y = 150.0 - 190.0", body_style), Paragraph("0.5573 - 0.6615", body_style), Paragraph("36,523 - 43,351", body_style), Paragraph("Podzol / Coarse Dirt (Pine Tree Limit)", body_style)],
        [Paragraph("Glacial Spine Arêtes & Horns", body_style), Paragraph("Y = 220.0 - 279.2", body_style), Paragraph("0.7396 - 0.8938", body_style), Paragraph("48,471 - 58,575", body_style), Paragraph("Frozen Peaks / Blue Glacier Ice", body_style)],
        [Paragraph("World Build Limit Ceiling", body_style), Paragraph("Y = 320.0", body_style), Paragraph("1.0000", body_style), Paragraph("65,535", body_style), Paragraph("Atmospheric Sky Ceiling", body_style)]
    ]
    t_h = Table(h_data, colWidths=[120, 75, 75, 75, 159])
    t_h.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_h)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Continental Shelf Dropoff (Hermite S-Curve Formula):</b> Beyond the continental shelf radius of $R_{\\text{inner}} = 3{,}300$ blocks, terrain descends monotonically into the abyss, reaching maximum oceanic depth at $R_{\\text{outer}} = 3{,}800$ blocks. The continuous dropoff is formulated as:", body_style))
    code_shelf = """t = clamp((radius - 3300.0) / (3800.0 - 3300.0), 0.0, 1.0)
S(t) = 3.0 * t^2 - 2.0 * t^3   # Continuous Cubic Hermite Spline
H_drop(R) = -600.0 * S(t)       # Deep ocean dropoff plunging into the Veil of Salt"""
    story.append(Paragraph(code_shelf.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    # -------------------------------------------------------------------------
    # SECTION 2: LANDFORMATIONS & EXACT COORDINATES
    # -------------------------------------------------------------------------
    story.append(Paragraph("2. Landformations & Exact Coordinate Specifications", h1_style))
    story.append(Paragraph("The continent of Vantyra is centered at $(X=0, Z=0)$, spanning exactly $-4{,}000$ to $+4{,}000$ blocks along both horizontal axes. The 9 cardinal landmarks are fixed at the following designated coordinates:", body_style))

    coord_data = [
        [Paragraph("<b>Landmark Name</b>", meta_style), Paragraph("<b>Center Coord</b>", meta_style), Paragraph("<b>Bounding Box (X1..X2, Z1..Z2)</b>", meta_style), Paragraph("<b>Target Y</b>", meta_style), Paragraph("<b>Geological Formation Rules</b>", meta_style)],
        [Paragraph("<b>1. Forgotten Coast</b> (Spawn)", body_style), Paragraph("(0, 68, 2500)", body_style), Paragraph("X: [-600, 600]<br/>Z: [2000, 3200]", body_style), Paragraph("68 - 74", body_style), Paragraph("Cold pebble bluffs, rolling wildflower bluffs, ancient stone beacon, starter pier.", body_style)],
        [Paragraph("<b>2. Cogwork March</b>", body_style), Paragraph("(-2100, 85, 0)", body_style), Paragraph("X: [-2800, -1400]<br/>Z: [-700, 700]", body_style), Paragraph("85 - 110", body_style), Paragraph("Concentric 9m quarry steps, brass river chasms, Create factory benches.", body_style)],
        [Paragraph("<b>3. The Ashen Caldera</b>", body_style), Paragraph("(0, 80, 0)", body_style), Paragraph("X: [-750, 750]<br/>Z: [-750, 750]", body_style), Paragraph("38 - 150", body_style), Paragraph("Volcanic ring wall (Y=146), sunken crater basin (Y=40), Obsidian Throne spire (Y=92).", body_style)],
        [Paragraph("<b>4. Solitary Glacial Spine</b>", body_style), Paragraph("(0, 220, -2500)", body_style), Paragraph("X: [-1800, 1800]<br/>Z: [-3500, -1500]", body_style), Paragraph("180 - 279", body_style), Paragraph("Alpine cordillera, Matterhorn arêtes, cirque tarns, flash-frozen pilgrim trails.", body_style)],
        [Paragraph("<b>5. The Gilded Dunes</b>", body_style), Paragraph("(2300, 75, 0)", body_style), Paragraph("X: [1600, 3100]<br/>Z: [-800, 800]", body_style), Paragraph("75 - 94", body_style), Paragraph("Vitrified black-glass dunes, 45° barchan ridges, terracotta canyon mesas.", body_style)],
        [Paragraph("<b>6. The Whispering Fen</b>", body_style), Paragraph("(2000, 63, 2000)", body_style), Paragraph("X: [1300, 2700]<br/>Z: [1300, 2700]", body_style), Paragraph("62 - 66", body_style), Paragraph("Flat sunken bayous, braided delta channels, giant fungal heartwood trees.", body_style)],
        [Paragraph("<b>7. The Sunken Reach</b>", body_style), Paragraph("(-2400, 54, 1600)", body_style), Paragraph("X: [-3200, -1700]<br/>Z: [1000, 2300]", body_style), Paragraph("50 - 62", body_style), Paragraph("Drowned coastal caldera shelf (100 fathoms), coral atolls, barrier sandbars.", body_style)],
        [Paragraph("<b>8. The Hermit's Spire</b>", body_style), Paragraph("(-1800, 140, -1800)", body_style), Paragraph("X: [-2300, -1300]<br/>Z: [-2300, -1300]", body_style), Paragraph("140 - 185", body_style), Paragraph("Solitary granite needles, ascetic rope bridges, silent wind-scoured cloisters.", body_style)],
        [Paragraph("<b>9. The Byzantine Choir</b>", body_style), Paragraph("(1800, 120, -1800)", body_style), Paragraph("X: [1300, 2300]<br/>Z: [-2300, -1300]", body_style), Paragraph("110 - 145", body_style), Paragraph("Gilded resonant basilicas, pink cherry terraces, harmonic acoustic ruins.", body_style)],
        [Paragraph("<b>RIM: The Veil of Salt</b>", body_style), Paragraph("Radius > 3550", body_style), Paragraph("Full perimeter to [-4000, 4000]", body_style), Paragraph("-32 - 62", body_style), Paragraph("Syrupy caustic brine abyss, white salt crusts, space unravels beyond 4000.", body_style)]
    ]
    t_coord = Table(coord_data, colWidths=[90, 75, 95, 54, 190])
    t_coord.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_coord)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # SECTION 3: LITHOSPHERE BIOMES & DENSITY FUNCTIONS
    # -------------------------------------------------------------------------
    story.append(Paragraph("3. Lithosphere Biomes & Spline Density Function Architecture", h1_style))
    story.append(Paragraph("Lithosphere entirely replaces vanilla piecewise linear interpolation with <b>Continuous Cubic Hermite Splines</b> ($S(t) = 3t^2 - 2t^3$). The macro-terrain is governed by three primary density functions in <code>datapacks/ashenfall_data2</code>:", body_style))
    story.append(Paragraph("• <b><code>continents.json</code>:</b> Continuous cubic spline mapping continentalness $C \\in [-1.2, 1.2]$. Ocean basins are clamped below $C < -0.20$; landmass emerges smoothly at $C \\ge 0.05$.<br/>"
                           "• <b><code>erosion.json</code>:</b> Multi-octave domain-warped spline ($E \\in [-1.0, 1.0]$). Low erosion ($E < -0.45$) produces jagged alpine arêtes; high erosion ($E > 0.35$) produces flat floodplains and bayous.<br/>"
                           "• <b><code>ridges.json</code>:</b> Folding harmonic spline ($R \\in [-1.0, 1.0]$). Carves wide U-shaped river valleys at $R \\approx 0$ while cresting sharp ridges at $|R| \\approx 1$.", bullet_style))

    # Biome Mapping Table
    b_data = [
        [Paragraph("<b>Region</b>", meta_style), Paragraph("<b>Target Lithosphere Biomes</b>", meta_style), Paragraph("<b>Cont (C)</b>", meta_style), Paragraph("<b>Erosion (E)</b>", meta_style), Paragraph("<b>Ridges (R)</b>", meta_style), Paragraph("<b>Surface Blocks (Lithosphere)</b>", meta_style)],
        [Paragraph("Forgotten Coast", body_style), Paragraph("minecraft:plains<br/>minecraft:meadow", body_style), Paragraph("0.10 - 0.30", body_style), Paragraph("-0.10 - 0.20", body_style), Paragraph("-0.30 - 0.30", body_style), Paragraph("Grass Block, Podzol, Stony Shore", body_style)],
        [Paragraph("Glacial Spine", body_style), Paragraph("minecraft:frozen_peaks<br/>minecraft:jagged_peaks<br/>minecraft:grove", body_style), Paragraph("0.45 - 0.90", body_style), Paragraph("-0.80 - -0.45", body_style), Paragraph("0.50 - 0.95", body_style), Paragraph("Snow Block, Packed Ice, Calcite, Stone", body_style)],
        [Paragraph("Cogwork March", body_style), Paragraph("minecraft:windswept_hills<br/>minecraft:wooded_badlands", body_style), Paragraph("0.25 - 0.60", body_style), Paragraph("-0.35 - 0.15", body_style), Paragraph("-0.80 - -0.20", body_style), Paragraph("Orange/Yellow Terracotta, Stone, Andesite", body_style)],
        [Paragraph("Ashen Caldera", body_style), Paragraph("minecraft:basalt_deltas<br/>minecraft:eroded_badlands", body_style), Paragraph("0.20 - 0.50", body_style), Paragraph("-0.20 - 0.30", body_style), Paragraph("0.00 - 0.40", body_style), Paragraph("Basalt, Blackstone, Magma Block, Obsidian", body_style)],
        [Paragraph("Gilded Dunes", body_style), Paragraph("minecraft:desert<br/>minecraft:badlands", body_style), Paragraph("0.20 - 0.55", body_style), Paragraph("0.25 - 0.70", body_style), Paragraph("-0.40 - 0.40", body_style), Paragraph("Red Sand, Sandstone, Terracotta", body_style)],
        [Paragraph("Whispering Fen", body_style), Paragraph("minecraft:swamp<br/>minecraft:mangrove_swamp", body_style), Paragraph("0.05 - 0.25", body_style), Paragraph("0.40 - 0.85", body_style), Paragraph("-0.20 - 0.20", body_style), Paragraph("Mud, Peat, Moss, Coarse Dirt", body_style)],
        [Paragraph("Sunken Reach", body_style), Paragraph("minecraft:warm_ocean<br/>minecraft:lukewarm_ocean", body_style), Paragraph("-0.35 - -0.10", body_style), Paragraph("0.10 - 0.50", body_style), Paragraph("-0.50 - 0.50", body_style), Paragraph("Sand, Coral Reefs, Prismarine Gravel", body_style)],
        [Paragraph("Veil of Salt (Abyss)", body_style), Paragraph("minecraft:deep_cold_ocean<br/>minecraft:deep_ocean", body_style), Paragraph("-0.90 - -0.45", body_style), Paragraph("-0.60 - 0.40", body_style), Paragraph("-1.00 - 1.00", body_style), Paragraph("Gravel, Deepslate, Packed Salt", body_style)]
    ]
    t_b = Table(b_data, colWidths=[80, 110, 60, 60, 60, 134])
    t_b.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_b)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # SECTION 4: TEMPERATURE GRADIENT & BIOME BLENDING
    # -------------------------------------------------------------------------
    story.append(Paragraph("4. Temperature Gradient, Altitude Lapse Rates & Biome Blending", h1_style))
    story.append(Paragraph("<b>The 5-Tier Climate Separation Rule:</b> Previous worldgen builds suffered from the 'snow-pocket glitch'—isolated patches of frozen snow generating inside temperate forests. This occurred because temperate and freezing biomes were separated by only 0.10 temperature units, allowing noise jitter to flip the Voronoi cell. In Ashenfall, climate is governed by strict <b>0.55-unit temperature buffering</b>:", body_style))

    clim_data = [
        [Paragraph("<b>Climate Tier</b>", meta_style), Paragraph("<b>Normalized Temp (T)</b>", meta_style), Paragraph("<b>Humidity (H)</b>", meta_style), Paragraph("<b>Target Geography & Buffer Behavior</b>", meta_style)],
        [Paragraph("<b>Tier 0: Glacial Arctic</b>", body_style), Paragraph("T <= -0.75", body_style), Paragraph("H: [-0.4, 0.4]", body_style), Paragraph("Glacial Spine summits (Y > 180). Frozen peaks, ice sheets, permafrost.", body_style)],
        [Paragraph("<b>Tier 1: Boreal Buffer Belt</b>", body_style), Paragraph("-0.60 <= T <= -0.25", body_style), Paragraph("H: [-0.2, 0.6]", body_style), Paragraph("Mandatory 600-block non-snowy pine taiga buffer. Prevents snow from touching temperate plains.", body_style)],
        [Paragraph("<b>Tier 2: Temperate Lowlands</b>", body_style), Paragraph("-0.15 <= T <= 0.40", body_style), Paragraph("H: [-0.1, 0.8]", body_style), Paragraph("Forgotten Coast, plains, meadows, oak/birch woodlands.", body_style)],
        [Paragraph("<b>Tier 3: Subtropical Bayou</b>", body_style), Paragraph("0.35 <= T <= 0.60", body_style), Paragraph("H: [0.5, 1.0]", body_style), Paragraph("Whispering Fen. Saturated peat, mangrove deltas, warm swamps.", body_style)],
        [Paragraph("<b>Tier 4: Arid & Volcanic</b>", body_style), Paragraph("T >= 0.70", body_style), Paragraph("H: [-0.8, -0.2]", body_style), Paragraph("Gilded Dunes and Ashen Caldera. Desert sand seas, terracotta badlands, basalt sinks.", body_style)]
    ]
    t_clim = Table(clim_data, colWidths=[100, 90, 80, 234])
    t_clim.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_clim)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Atmospheric Altitude Lapse Rate Formula:</b> Temperature decreases linearly with elevation above sea level ($Y = 62$), simulating genuine adiabatic expansion:", body_style))
    code_lapse = """# Effective Temperature = Latitude Base + Altitude Lapse Rate
T_eff(x, y, z) = T_base(x, z) - 0.0055 * max(0.0, y - 62.0)
# High summits at Y=220 experience a -0.869 temperature reduction, guaranteeing snow caps."""
    story.append(Paragraph(code_lapse.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    story.append(Paragraph("<b>5D Voronoi Metric & Biome Blending:</b> Biome placement evaluates the Euclidean distance in 5D multi-noise space, smoothed across an 8-block Voronoi cell radius:", body_style))
    code_voronoi = """D(P, B_i) = sqrt((T - T_i)^2 + (H - H_i)^2 + (C - C_i)^2 + (E - E_i)^2 + (W - W_i)^2)
biome_blend_radius = 4  # 9x9 chunk voxel smoothing in Minecraft client options"""
    story.append(Paragraph(code_voronoi.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------------------
    # SECTION 5: POPULATION INSTRUCTIONS & FORCING STILL LIFE
    # -------------------------------------------------------------------------
    story.append(Paragraph("5. Population Instructions: How to Force Still Life to Generate Where Desired", h1_style))
    story.append(Paragraph("Still Life features (branched canopy trees, fallen birch/oak logs, glacial erratic boulders, and wildflower carpets) do not rely on random brush strokes. They are governed by three deterministic mechanisms that can be programmatically forced:", body_style))

    story.append(Paragraph("<b>Method 1: The WorldPainter 'Populate' Layer (100% Guaranteed Native Decorator Pass):</b><br/>"
                           "When pre-generating terrain via WorldPainter or Python, never export chunks as <code>Status: 'full'</code>. Instead, apply the binary <code>ASHFALL_POPULATE_MASK.png</code> to WorldPainter's native <b>Populate</b> layer. When Minecraft loads a chunk flagged with Populate, its internal world decorator natively executes Still Life's entire placed feature registry. Valleys receive lush trees and fallen logs; cliffs and volcanic calderas remain completely bare.", body_style))

    story.append(Paragraph("<b>Method 2: Still Life Biome Tag Injections (Datapack Level):</b><br/>"
                           "Still Life feature placement is bound to biome tags in <code>data/still_life/tags/worldgen/biome/</code>. By adding target biomes into these tags, Still Life is forced to generate in those specific biomes:", body_style))
    
    code_tags = """# data/still_life/tags/worldgen/biome/has_canopy.json -> ["minecraft:plains", "minecraft:forest"]
# data/still_life/tags/worldgen/biome/has_fallen_logs.json -> ["minecraft:forest", "minecraft:taiga"]
# data/still_life/tags/worldgen/biome/has_boulders.json -> ["minecraft:windswept_hills", "minecraft:meadow"]"""
    story.append(Paragraph(code_tags.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    story.append(Paragraph("<b>Method 3: The Still Life Slope-Aware Surface Rule:</b><br/>"
                           "Still Life inspects local geological slope angles. Tree and log decorators require grass/dirt surface blocks. Terrain steeper than $35^\\circ$ automatically strips topsoil to bare rock scree, naturally preventing trees from generating on cliff faces:", body_style))

    # Slope Rule Table
    slope_data = [
        [Paragraph("<b>Slope Angle (θ)</b>", meta_style), Paragraph("<b>Surface Block (Still Life Rule)</b>", meta_style), Paragraph("<b>Vegetation & Feature Population Density</b>", meta_style)],
        [Paragraph("0° <= θ < 25°", body_style), Paragraph("Grass Block / Deep Loam (3-5 blocks)", body_style), Paragraph("100% Full Canopy Trees, Fallen Logs, Wildflowers, Shrub understory.", body_style)],
        [Paragraph("25° <= θ <= 35°", body_style), Paragraph("Coarse Dirt, Permadirt, Podzol", body_style), Paragraph("40% Density: Pine Taiga, berry bushes, small stone erratics.", body_style)],
        [Paragraph("35° < θ <= 45°", body_style), Paragraph("Cobblestone, Stone Scree, Gravel", body_style), Paragraph("5% Density: Mossy boulders, clinging lichen. Trees strictly excluded.", body_style)],
        [Paragraph("θ > 45° (Sheer Cliffs)", body_style), Paragraph("Solid Bedrock, Granite, Basalt", body_style), Paragraph("0% Population: 100% bare rock scree. No trees or logs can spawn.", body_style)],
        [Paragraph("Y > 225.0 (Treeline)", body_style), Paragraph("Snow Block, Packed Ice, Calcite", body_style), Paragraph("0% Population: Climatic treeline cutoff. High-altitude glacial frost.", body_style)],
        [Paragraph("Caldera Rim / Crater", body_style), Paragraph("Blackstone, Basalt, Magma Block", body_style), Paragraph("0% Population: Volcanic barrenness mask overrides all foliage.", body_style)]
    ]
    t_slope = Table(slope_data, colWidths=[90, 150, 264])
    t_slope.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_slope)
    story.append(Spacer(1, 10))

    story.append(Paragraph("<b>Turnkey Execution Command:</b> To re-generate all heightmaps, 16-bit uint16 assets, Still Life populate masks, and JSR-223 WorldPainter scripts, run:", body_style))
    code_run = """python generate_ashfall.py --res 2048 --out worldpainter
# Output: ASHFALL_HEIGHTMAP_16BIT.png, ASHFALL_POPULATE_MASK.png, ashenfall_worldpainter_setup.js"""
    story.append(Paragraph(code_run.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[✓] PDF successfully generated: {OUTPUT_PDF} ({OUTPUT_PDF.stat().st_size} bytes)")


def generate_markdown():
    """Generates the complementary master markdown specification file."""
    md_content = """# Ashenfall: Master World Map & Geological Specification
### *Complete Technical Data: Heightmaps, Coordinates, Lithosphere Splines, Climate Gradients & Still Life Population*
**Target Engine:** Minecraft 1.21.1 Java Edition · **Data Pack Format:** 48 · **Canvas:** 8,000 × 8,000 Blocks  
**World:** Continent of Vantyra · **Dependencies:** Lithosphere (v1.3+), Still Life (v0.1+)

---

## 1. Heightmap Data & Elevation Mathematical Specification

The continent of Vantyra operates across Minecraft 1.21.1's extended world height ceiling:
* **Minimum World Height:** $Y = -64$
* **Maximum World Height:** $Y = 320$
* **Total Height Space:** $384$ blocks
* **Mean Sea Level (Water Surface):** $Y = 62$

### 16-Bit uint16 Linear Normalization Equation
Every pixel in the master heightfield maps directly to a discrete block elevation through linear scaling:

$$h_{\\text{norm}} = \\frac{Y - (-64.0)}{384.0} = \\frac{Y + 64.0}{384.0}$$
$$V_{\\text{uint16}} = \\text{round}(h_{\\text{norm}} \\times 65535.0)$$
$$Y_{\\text{block}} = -64.0 + \\left(\\frac{V_{\\text{uint16}}}{65535.0}\\right) \\times 384.0$$

### Elevation Keypoints Table

| Geological Feature | Target Y Block | Normalized [0..1] | 16-Bit uint16 | Lithosphere Material / Layer |
| :--- | :---: | :---: | :---: | :--- |
| **Bedrock Floor** | $Y = -64.0$ | $0.0000$ | `0` | Solid Bedrock Floor |
| **Abyssal Trench (Veil of Salt)** | $Y = -32.0 \\to 10.0$ | $0.0833 \\to 0.1927$ | `5,461` $\\to$ `12,629` | Deep Cold Ocean / Gravel |
| **Sunken Caldera Floor** | $Y = 38.0 \\to 42.0$ | $0.2656 \\to 0.2760$ | `17,406` $\\to$ `18,088` | Basalt / Lava Basins / Obsidian |
| **Sunken Reach Drowned Shelf** | $Y = 52.0 \\to 56.0$ | $0.3021 \\to 0.3125$ | `19,798` $\\to$ `20,480` | Warm Ocean Reefs / Sandbars |
| **Mean Sea Level (Water Line)** | **$Y = 62.0$** | **$0.3281$** | **`21,504`** | **Water Surface / Sea Surface** |
| **Forgotten Coast Shoreline** | $Y = 68.0 \\to 74.0$ | $0.3438 \\to 0.3594$ | `22,532` $\\to$ `23,556` | Stony Shore / Cold Pebble Beaches |
| **Gilded Dunes Low Mesas** | $Y = 82.0 \\to 96.0$ | $0.3802 \\to 0.4167$ | `24,917` $\\to$ `27,307` | Terracotta / Red Sandstone |
| **Cogwork March Quarry Benches** | $Y = 85.0 \\to 110.0$ | $0.3880 \\to 0.4531$ | `25,428` $\\to$ `29,695` | Terraced Badlands (9m steps) |
| **Caldera Volcanic Rim** | $Y = 142.0 \\to 156.0$ | $0.5365 \\to 0.5729$ | `35,158` $\\to$ `37,548` | Blackstone / Basalt Spines |
| **Subalpine Taiga Foothills** | $Y = 150.0 \\to 190.0$ | $0.5573 \\to 0.6615$ | `36,523` $\\to$ `43,351` | Podzol / Coarse Dirt (Pine Limit) |
| **Glacial Spine Arêtes & Horns**| $Y = 220.0 \\to 279.2$ | $0.7396 \\to 0.8938$ | `48,471` $\\to$ `58,575` | Frozen Peaks / Blue Glacier Ice |
| **World Build Limit Ceiling** | $Y = 320.0$ | $1.0000$ | `65,535` | Atmospheric Sky Ceiling |

### Continental Shelf Dropoff (Hermite S-Curve Formula)
Beyond the continental shelf radius of $R_{\\text{inner}} = 3{,}300$ blocks, terrain descends monotonically into the abyss, reaching maximum ocean depth at $R_{\\text{outer}} = 3{,}800$ blocks:

$$t = \\text{clamp}\\left(\\frac{R - 3300.0}{3800.0 - 3300.0}, 0.0, 1.0\\right)$$
$$S(t) = 3t^2 - 2t^3 \\quad \\text{(Continuous Cubic Hermite Spline)}$$
$$H_{\\text{drop}}(R) = -600.0 \\times S(t) \\quad \\text{(Plunging into the Veil of Salt)}$$

---

## 2. Landformations & Exact Coordinate Specifications

```
                            [ NORTH: Z = -4000 ]
                     ══════════════════════════════════
                            THE VEIL OF SALT (OCEAN)
                     ══════════════════════════════════
                                    │
                       [ THE SOLITARY GLACIAL SPINE ]
                      (Z = -1500 to -3500, X = -1800 to +1800)
                     Jagged Snow Peaks & Glacial Cirques (Y = 180 - 279)
                                    │
   [ WEST: X = -4000 ]              │              [ EAST: X = +4000 ]
 ══════════════════════             │             ══════════════════════
   THE SUNKEN REACH                 │               THE GILDED DUNES
 (Drowned Port Ostraka)             │              (Al-Qadira Sand Sea)
  Shallow Lagoons & Reefs           │              Rolling Dunes & Terracotta
  X = -2400, Z = +1600              │              X = +2300, Z = 0
            │                       │                       │
            ├─────────────── [ THE CALDERA ] ───────────────┤
            │                  (X = 0, Z = 0)               │
            │           Throne of Melted Obsidian           │
            │          Jagged Volcanic Ring: Y = 146        │
            │           Sunken Crater Floor: Y = 40         │
            │                       │                       │
   [ THE COGWORK MARCH ]            │             [ THE WHISPERING FEN ]
  (Brass Canyons & Terraces)        │             (Deep Bayou & Mangroves)
  Stepped Cliffs & River Gorges     │             Muddy Deltas (Y = 62 - 66)
  X = -2100, Z = 0                  │             X = +2000, Z = +2000
                                    │
                     [ THE FORGOTTEN COAST & SPAWN ]
                       (X = 0, Z = 2500 — Marked RED)
                     Cold Pebble Beaches & Rolling Bluffs
                                    │
                     ══════════════════════════════════
                            THE VEIL OF SALT (OCEAN)
                     ══════════════════════════════════
                            [ SOUTH: Z = +4000 ]
```

### Landmark Coordinates Table

| Landmark Name | Center Coord $(X, Y, Z)$ | Bounding Box $(X_1..X_2, Z_1..Z_2)$ | Target $Y$ | Geological Formation Rules |
| :--- | :---: | :---: | :---: | :--- |
| **1. Forgotten Coast (Spawn)** | `(0, 68, 2500)` | $X: [-600, 600], Z: [2000, 3200]$ | $68 - 74$ | Cold pebble bluffs, rolling wildflower bluffs, stone beacon pier. |
| **2. Cogwork March** | `(-2100, 85, 0)` | $X: [-2800, -1400], Z: [-700, 700]$ | $85 - 110$ | Concentric 9m quarry steps, brass river chasms, Create factory benches. |
| **3. The Ashen Caldera** | `(0, 80, 0)` | $X: [-750, 750], Z: [-750, 750]$ | $38 - 150$ | Volcanic ring wall ($Y=146$), sunken crater basin ($Y=40$), Obsidian Throne ($Y=92$). |
| **4. Solitary Glacial Spine** | `(0, 220, -2500)` | $X: [-1800, 1800], Z: [-3500, -1500]$ | $180 - 279$ | Alpine cordillera, Matterhorn arêtes, cirque tarns, flash-frozen pilgrim trails. |
| **5. The Gilded Dunes** | `(2300, 75, 0)` | $X: [1600, 3100], Z: [-800, 800]$ | $75 - 94$ | Vitrified black-glass dunes, $45^\\circ$ barchan ridges, terracotta canyon mesas. |
| **6. The Whispering Fen** | `(2000, 63, 2000)` | $X: [1300, 2700], Z: [1300, 2700]$ | $62 - 66$ | Flat sunken bayous, braided delta channels, giant fungal heartwood trees. |
| **7. The Sunken Reach** | `(-2400, 54, 1600)` | $X: [-3200, -1700], Z: [1000, 2300]$ | $50 - 62$ | Drowned coastal caldera shelf (100 fathoms), coral atolls, barrier sandbars. |
| **8. The Hermit's Spire** | `(-1800, 140, -1800)`| $X: [-2300, -1300], Z: [-2300, -1300]$ | $140 - 185$ | Solitary granite needles, ascetic rope bridges, silent wind-scoured cloisters. |
| **9. The Byzantine Choir** | `(1800, 120, -1800)` | $X: [1300, 2300], Z: [-2300, -1300]$ | $110 - 145$ | Gilded resonant basilicas, pink cherry terraces, harmonic acoustic ruins. |
| **RIM: The Veil of Salt** | $R > 3550$ | Full perimeter to $[-4000, 4000]$ | $-32 - 62$ | Syrupy caustic brine abyss, white salt crusts; space dissolves beyond $4000$. |

---

## 3. Lithosphere Biomes & Density Function Architecture

Lithosphere eliminates stepped contour terracing through 3 continuous cubic spline functions:

1. **`continents.json` (Continentalness $C \\in [-1.2, 1.2]$):**
   * $C < -0.20$: Submarine oceanic trenches (`deep_cold_ocean`, `deep_ocean`).
   * $-0.20 \\le C \\le 0.05$: Coastal bluffs and beaches.
   * $0.05 < C \\le 0.60$: Inland fertile lowlands and valleys.
   * $C > 0.60$: High mountain cordilleras.
2. **`erosion.json` (Erosion Detail $E \\in [-1.0, 1.0]$):**
   * $E < -0.45$: Low erosion produces jagged alpine arêtes and Matterhorn horns (Solitary Spine).
   * $-0.45 \\le E \\le 0.25$: Moderate erosion produces terraced plateaus (Cogwork March).
   * $E > 0.25$: High erosion produces flat bayous and floodplains (Whispering Fen).
3. **`ridges.json` (Ridge Lines $R \\in [-1.0, 1.0]$):**
   * $R \\approx 0$: Carves wide U-shaped glacial river valleys.
   * $|R| \\approx 1$: Forms sharp knife-edge crests and arêtes.

---

## 4. Temperature Gradient, Altitude Lapse Rates & Biome Blending

### 5-Tier Climate Banding (Anti-Snow-Pocket Rule)
To eliminate snow pockets from generating in temperate forests, climate zones are separated by **at least $0.55$ temperature units**:

* **Tier 0: Glacial Arctic ($T \\le -0.75$):** Glacial Spine summits ($Y > 180$). `frozen_peaks`, `jagged_peaks`, `snowy_slopes`.
* **Tier 1: Boreal Buffer Belt ($-0.60 \\le T \\le -0.25$):** Mandatory 600-block non-snowy pine taiga buffer.
* **Tier 2: Temperate Lowlands ($-0.15 \\le T \\le 0.40$):** Forgotten Coast, plains, meadows, oak/birch woodlands.
* **Tier 3: Subtropical Bayou ($0.35 \\le T \\le 0.60$):** Whispering Fen. Saturated peat, mangrove deltas, warm swamps.
* **Tier 4: Arid & Volcanic ($T \\ge 0.70$):** Gilded Dunes and Ashen Caldera. Desert sand seas, terracotta badlands, basalt sinks.

### Atmospheric Altitude Lapse Rate Formula
Temperature decreases linearly with elevation above sea level:
$$T_{\\text{eff}}(x, y, z) = T_{\\text{base}}(x, z) - 0.0055 \\times \\max(0.0, y - 62.0)$$

### 5D Multi-Noise Voronoi Metric & Client Blending
Biome placement evaluates Euclidean distance in 5D multi-noise space $(T, H, C, E, W)$:
$$D(\\mathbf{P}, \\mathbf{B}_i) = \\sqrt{(T - T_i)^2 + (H - H_i)^2 + (C - C_i)^2 + (E - E_i)^2 + (W - W_i)^2}$$
Client biome blend radius is set to `4` (9×9 chunk voxel smoothing), eliminating knife-edge biome borders.

---

## 5. Population Instructions: How to Force Still Life to Generate Where Desired

Still Life features (tall branched canopies, fallen birch/oak logs, mossy boulders, and wildflower carpets) are forced through three deterministic methods:

### Method 1: The WorldPainter 'Populate' Layer (100% Guaranteed Native Pass)
1. Generate the binary mask `ASHFALL_POPULATE_MASK.png` (white = fertile valleys, black = bare rock/caldera).
2. In WorldPainter's JSR-223 script:
   ```javascript
   var popMask = wp.getHeightMap().fromFile("worldpainter/ASHFALL_POPULATE_MASK.png").go();
   var popLayer = wp.getLayer().withName("Populate").go();
   wp.applyHeightMap(popMask).toWorld(world).applyToLayer(popLayer).fromLevels(128, 255).toLevel(1).go();
   ```
3. Export the world to `.minecraft/saves`. Chunks with the Populate flag natively trigger Minecraft's `FEATURES` pass, generating Still Life's full placed feature registry.

### Method 2: Still Life Biome Tag Injections (Datapack Level)
In `data/still_life/tags/worldgen/biome/`, add your target biome IDs:
* `has_canopy.json`: `["minecraft:plains", "minecraft:forest", "minecraft:meadow"]`
* `has_fallen_logs.json`: `["minecraft:forest", "minecraft:taiga", "minecraft:old_growth_pine_taiga"]`
* `has_boulders.json`: `["minecraft:windswept_hills", "minecraft:meadow", "minecraft:stony_shore"]`

### Method 3: The Still Life Slope-Aware Surface Rule
Still Life automatically inspects local slope angles $\\theta = \\arctan(\\|\\nabla H\\|)$:
* **$0^\\circ \\le \\theta < 25^\\circ$:** 100% Deep Grass & Soil $\\to$ 100% Full Canopy Trees, Fallen Logs, Wildflowers.
* **$25^\\circ \\le \\theta \\le 35^\\circ$:** Coarse Dirt & Podzol $\\to$ 40% Density (Pine taiga, berry bushes).
* **$35^\\circ < \\theta \\le 45^\\circ$:** Scree & Gravel $\\to$ 5% Density (Mossy boulders only).
* **$\\theta > 45^\\circ$:** 100% Bare Bedrock & Basalt $\\to$ **0% Population (No trees or logs can spawn).**
* **$Y > 225.0$:** Climatic Treeline Cutoff $\\to$ **0% Population (Glacial frost and ice only).**
* **Caldera Rim:** Barrenness mask overrides all foliage $\\to$ **0% Population.**
"""
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"[✓] Markdown successfully generated: {OUTPUT_MD} ({OUTPUT_MD.stat().st_size} bytes)")

if __name__ == "__main__":
    generate_markdown()
    build_pdf_and_markdown()
