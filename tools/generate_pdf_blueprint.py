#!/usr/bin/env python3
"""
=============================================================================
ASHENFALL: Programmatic Large-Scale Terrain Architecture PDF Generator
Compiles a publication-grade technical whitepaper PDF using ReportLab
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
OUTPUT_PDF = BASE_DIR / "docs" / "design" / "PROGRAMMATIC_LARGE_SCALE_TERRAIN_SYSTEM_SPECIFICATION.pdf"

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
            # Suppress headers/footers on title cover page
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Running Header
        self.drawString(54, 750, "ASHENFALL SPECIFICATION: Programmatic Large-Scale Terrain Pipeline")
        self.drawRightString(612 - 54, 750, "Minecraft 1.21.1+ Architecture")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 744, 612 - 54, 744)

        # Running Footer
        self.line(54, 45, 612 - 54, 45)
        self.drawString(54, 34, "Confidential & Open Source Reference · World Machine / Gaea to WorldPainter")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 34, page_str)
        self.restoreState()


def build_pdf():
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

    # Custom typography
    c_primary = colors.HexColor("#0f172a")     # Slate 900
    c_accent = colors.HexColor("#0284c7")      # Sky 600
    c_secondary = colors.HexColor("#334155")   # Slate 700
    c_muted = colors.HexColor("#64748b")       # Slate 500
    c_box_bg = colors.HexColor("#f8fafc")      # Slate 50
    c_box_border = colors.HexColor("#cbd5e1")  # Slate 300

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=c_primary,
        alignment=TA_LEFT,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=16,
        textColor=c_accent,
        alignment=TA_LEFT,
        spaceAfter=14
    )

    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=c_muted,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=c_primary,
        spaceBefore=16,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=15,
        textColor=c_accent,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=c_secondary,
        alignment=TA_JUSTIFY,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor("#0f172a"),
        backColor=colors.HexColor("#f1f5f9"),
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6
    )

    box_text_style = ParagraphStyle(
        'BoxText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#1e293b")
    )

    story = []

    # =========================================================================
    # TITLE & HEADER BLOCK
    # =========================================================================
    story.append(Paragraph("Programmatic Large-Scale Minecraft Terrain Architecture", title_style))
    story.append(Paragraph("A Technical Blueprint for Automated 10,000 × 10,000 Block Continents", subtitle_style))
    story.append(Paragraph("<b>Author:</b> Ashenfall Core Engineering Group &nbsp;|&nbsp; <b>Version:</b> 2.5.0-Enterprise &nbsp;|&nbsp; <b>Target:</b> Minecraft 1.21.1+ (World Machine / Gaea to WorldPainter)", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=0, spaceAfter=12))

    # Executive Summary Callout Box
    summary_html = """<b>EXECUTIVE SUMMARY:</b><br/>
    Constructing massive photorealistic Minecraft continents ($10{,}000 \\times 10{,}000$ blocks, covering $100\\text{ km}^2$ and $100{,}000{,}000$ surface columns) cannot be accomplished through manual brush painting. Hand-painting at this scale causes unnatural repetition, concentric brush rings, broken hydrological flow, and unsustainable human labor overhead.<br/><br/>
    This document outlines the complete three-stage programmatic architecture: (1) <b>Procedural Geological Simulation</b> (spline-guided instance scattering, thermal scree weathering, and priority-flood river routing); (2) <b>Ecological Probability Transformation</b> (multi-criteria evaluation and blue-noise spatial dithering); and (3) <b>Headless WorldPainter Script Automation</b> (declarative config files driving JSR-223 Rhino ECMAScript execution).
    """
    callout_table = Table([[Paragraph(summary_html, box_text_style)]], colWidths=[504])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), c_box_bg),
        ('BOX', (0,0), (-1,-1), 1, c_box_border),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 14))

    # =========================================================================
    # FORMAL TABLE OF CONTENTS / OUTLINE
    # =========================================================================
    story.append(Paragraph("Document Structure & PDF Outline", h1_style))
    toc_data = [
        [Paragraph("<b>Chapter</b>", meta_style), Paragraph("<b>Title & Core Technical Topics</b>", meta_style), Paragraph("<b>Domain</b>", meta_style)],
        [Paragraph("<b>1</b>", body_style), Paragraph("<b>Executive Summary & The Paradigm Shift</b><br/>Voxel scaling limits, declarative simulation vs. manual painting, pipeline overview.", body_style), Paragraph("System Overview", body_style)],
        [Paragraph("<b>2</b>", body_style), Paragraph("<b>Stage 1: Procedural Geological Synthesis</b><br/>Spline instance scattering, Frenet-Serret frames, thermal weathering, priority-flood rivers.", body_style), Paragraph("Geomorphology", body_style)],
        [Paragraph("<b>3</b>", body_style), Paragraph("<b>Stage 2: Ecological Probability & Distribution</b><br/>Continuous MCE, treeline/snowline response curves, blue-noise spatial dithering.", body_style), Paragraph("Spatial Statistics", body_style)],
        [Paragraph("<b>4</b>", body_style), Paragraph("<b>Stage 3: Headless WorldPainter Automation</b><br/>Declarative YAML schemas, Rhino JSR-223 scripting host, wpscript CLI integration.", body_style), Paragraph("Compiler & CLI", body_style)],
        [Paragraph("<b>5</b>", body_style), Paragraph("<b>Production Code Architecture & Reference Modules</b><br/>End-to-end Python/Java code for scattering, weathering, dithering, and JSR223 synthesis.", body_style), Paragraph("Reference Source", body_style)],
        [Paragraph("<b>6</b>", body_style), Paragraph("<b>Tool Comparison & Production Execution Guide</b><br/>World Machine vs. Gaea vs. Custom Python; troubleshooting common artifacts.", body_style), Paragraph("Implementation", body_style)]
    ]
    t_toc = Table(toc_data, colWidths=[30, 374, 100])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_toc)
    story.append(Spacer(1, 14))

    # =========================================================================
    # CHAPTER 1
    # =========================================================================
    story.append(Paragraph("1. Executive Summary & The Paradigm Shift", h1_style))
    story.append(Paragraph("When building at 10,000 × 10,000 scale, traditional terraforming tools fail due to fundamental human and software scaling constraints. A human artist operating a 200-block diameter brush in WorldPainter would have to perform over 50,000 distinct brush strokes to cover the continent once, inevitably producing unnatural circular ripples and inconsistent topography.", body_style))
    story.append(Paragraph("The programmatic paradigm treats terrain as a <b>directed acyclic graph (DAG) of physical transformations</b>. Artistic intent is expressed through high-level guide vectors (mountain spine splines, river sources, coast boundaries), while mathematical simulations execute low-level erosion, slope texturing, and object placement.", body_style))

    # Pipeline stages table
    p_data = [
        [Paragraph("<b>Pipeline Stage</b>", meta_style), Paragraph("<b>Input Artifact</b>", meta_style), Paragraph("<b>Applied Mathematics / Logic</b>", meta_style), Paragraph("<b>Output Artifact</b>", meta_style)],
        [Paragraph("<b>1. Geology</b>", body_style), Paragraph("Guide Splines & Boundaries", body_style), Paragraph("Cubic splines, arête instances, stream power law, thermal slumping", body_style), Paragraph("16-Bit Lossless Heightmap", body_style)],
        [Paragraph("<b>2. Distribution</b>", body_style), Paragraph("Heightmap & Gradients", body_style), Paragraph("Slope derivative |∇H|, ecological MCE, blue-noise spatial dithering", body_style), Paragraph("Binary Layer Masks (Populate, Frost)", body_style)],
        [Paragraph("<b>3. Automation</b>", body_style), Paragraph("Heightmap + Masks + Config", body_style), Paragraph("JSR-223 Rhino ECMAScript compiler, wpscript CLI automation", body_style), Paragraph("Minecraft Anvil Region (.mca)", body_style)]
    ]
    t_pipe = Table(p_data, colWidths=[80, 110, 194, 120])
    t_pipe.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_pipe)
    story.append(Spacer(1, 14))

    # =========================================================================
    # CHAPTER 2
    # =========================================================================
    story.append(Paragraph("2. Stage 1: Procedural Geological Synthesis", h1_style))
    story.append(Paragraph("2.1 Instance Scattering for Mountain Ridgelines", h2_style))
    story.append(Paragraph("Standard Perlin noise produces isotropic mounds without tectonic structure. Real mountain ranges consist of continuous structural axes formed by tectonic uplift. The system utilizes <b>instance scattering</b> along parametric guide curves:", body_style))
    story.append(Paragraph("• <b>Structural Fault Spline C(t):</b> A parametric Hermite or Bézier curve (x(t), z(t)) with unit tangent vector T(t) and normal N(t).<br/>"
                           "• <b>Arête Primitive:</b> h_ridge(u, v) = H_0 · exp(-|v| / σ) · (1 - (u/L)²) · (1 + η · Noise(u, v)).<br/>"
                           "• <b>Polynomial Smooth-Max Blending:</b> smax(a, b, k) = (a + b + sqrt((a - b)² + k)) / 2. This avoids both flat plateau truncation and razor-sharp derivative seams, creating organic mountain passes (cols).", bullet_style))

    story.append(Paragraph("2.2 Thermal Weathering & Talus Slumping", h2_style))
    story.append(Paragraph("Rock faces cannot exceed the natural <b>angle of repose</b> (θ_c ≈ 35°–40°). Material exceeding this angle breaks away and deposits at the cliff foot as concave parabolic talus aprons. The finite-difference cellular model displaces excess mass downhill along the direction of steepest descent (-∇H / ||∇H||), creating natural scree slopes and rugged cliff faceting.", body_style))

    story.append(Paragraph("2.3 Flow Restructuring & Hydrological River Routing", h2_style))
    story.append(Paragraph("Standard procedural noise generates hollow pits that trap water. The system resolves this using a three-tier hydrological engine:", body_style))
    story.append(Paragraph("1. <b>Priority-Flood (Barnes / Wang-Liu):</b> Raises landlocked depressions to spillway levels or carves breach lines, guaranteeing monotonic descent to sea level (H(p_{i+1}) ≤ H(p_i)).<br/>"
                           "2. <b>D-Infinity Flow Accumulation:</b> Calculates the upstream catchment area A(x, z) for every cell based on aspect angles.<br/>"
                           "3. <b>Stream Power Law Carving:</b> Valley incision follows ΔH = -K · A^m · ||∇H||^n (m ≈ 0.5, n ≈ 1.0), cutting deep V-shaped mountain canyons and wide meandering lowland floodplains.", bullet_style))
    story.append(Spacer(1, 10))

    # =========================================================================
    # CHAPTER 3
    # =========================================================================
    story.append(Paragraph("3. Stage 2: Ecological Probability & Distribution", h1_style))
    story.append(Paragraph("3.1 The Fundamental Challenge: Continuous Fields vs. Discrete Voxels", h2_style))
    story.append(Paragraph("Simulation software computes continuous floating-point fields (height H ∈ [-64, 320], slope θ ∈ [0°, 90°], moisture M ∈ [0, 1]). Minecraft, however, requires discrete integer block IDs and exact point coordinates for trees, rocks, and foliage.", body_style))

    story.append(Paragraph("3.2 Multi-Criteria Evaluation (MCE) & Ecological Suitability", h2_style))
    story.append(Paragraph("For each feature, a suitability function P_feature(x, z) evaluates multiple environmental parameters:", body_style))
    story.append(Paragraph("• <b>Slope-Aware Topsoil Law:</b> Slopes < 35° receive 100% deep soil; slopes > 45° are stripped to bare stone scree.<br/>"
                           "• <b>Climatic Treeline:</b> Sigmoidal probability drop between Y=180 and Y=225 blocks; above Y=225, tree probability is 0.<br/>"
                           "• <b>Glacial Snowline:</b> Deep snow accumulates above Y=210 on gentle slopes, but is shed on steep cliff faces.", bullet_style))

    story.append(Paragraph("3.3 Blue Noise Spatial Dithering (Void-and-Cluster)", h2_style))
    story.append(Paragraph("Thresholding continuous probability against standard white noise causes unnatural clustering and bare voids. The system utilizes <b>blue noise dithering</b> (void-and-cluster matrix), which maximizes spatial distance between placed points. The resulting binary mask distributes foliage, fallen logs, and boulders with natural biological randomness and zero grid artifacts.", body_style))
    story.append(Spacer(1, 10))

    # =========================================================================
    # CHAPTER 4
    # =========================================================================
    story.append(Paragraph("4. Stage 3: Headless WorldPainter Automation", h1_style))
    story.append(Paragraph("4.1 Declarative Configuration Architecture", h2_style))
    story.append(Paragraph("Rather than manually clicking in WorldPainter, all world dimensions, build limits, strata bands, and mask mappings are specified in a single declarative configuration file (`terrain_config.yaml`).", body_style))

    code_yaml = """world:
  name: "Ashenfall_Continent"
  width: 10000; height: 10000; min_y: -64; max_y: 320; sea_level: 62
inputs:
  heightmap: "exports/height_16bit.png"
  populate_mask: "exports/mask_populate.png"
  frost_mask: "exports/mask_frost.png"
strata:
  - range: [-64, 61]; terrain: "Gravel / Sand"
  - range: [62, 130]; terrain: "Grass / Bare Dirt"; slope_limit: [0, 35]
  - range: [131, 190]; terrain: "Podzol / Coarse"
  - range: [191, 250]; terrain: "Stone / Cobblestone"
  - range: [251, 320]; terrain: "Deep Snow" """
    story.append(Paragraph(code_yaml.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    story.append(Paragraph("4.2 Automated JSR-223 Rhino Script Compiler", h2_style))
    story.append(Paragraph("A Python compiler translates `terrain_config.yaml` into a deterministic ECMAScript file executed by WorldPainter's internal scripting engine (`wpscript`):", body_style))

    code_js = """var heightMap = wp.getHeightMap().fromFile("exports/height_16bit.png").go();
var world = wp.createWorld().fromHeightMap(heightMap).scale(100)
    .fromLevels(0, 65535).toLevels(-64, 320).withWaterLevel(62)
    .withLowerBuildLimit(-64).withUpperBuildLimit(320).go();
var popMask = wp.getHeightMap().fromFile("exports/mask_populate.png").go();
var popLayer = wp.getLayer().withName("Populate").go();
wp.applyHeightMap(popMask).toWorld(world).applyToLayer(popLayer).fromLevels(128, 255).toLevel(1).go();
wp.exportWorld(world).toDirectory(".minecraft/saves/Ashenfall").go();"""
    story.append(Paragraph(code_js.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))
    story.append(Spacer(1, 10))

    # =========================================================================
    # CHAPTER 5 & 6
    # =========================================================================
    story.append(Paragraph("5. Production Software Architecture & Reference Modules", h1_style))
    story.append(Paragraph("The complete pipeline is implemented as five decoupled Python and JavaScript modules:", body_style))
    story.append(Paragraph("1. `instance_scatterer.py`: Evaluates 3D cubic splines and composites exponential arête ridges using smooth-max.<br/>"
                           "2. `thermal_weathering.py`: Vectorized finite-difference cellular automata for slope slumping.<br/>"
                           "3. `hydraulic_router.py`: Monotonic downhill stream power carver.<br/>"
                           "4. `blue_noise_dither.py`: Converts continuous suitability matrices into un-clumped binary placement masks.<br/>"
                           "5. `jsr223_compiler.py`: Emits verified WorldPainter scripts for headless CLI execution.", bullet_style))

    story.append(Paragraph("6. Practical Tooling Comparison", h1_style))
    comp_data = [
        [Paragraph("<b>Feature</b>", meta_style), Paragraph("<b>World Machine</b>", meta_style), Paragraph("<b>QuadSpinner Gaea</b>", meta_style), Paragraph("<b>Custom Python / C++</b>", meta_style)],
        [Paragraph("<b>Architecture</b>", body_style), Paragraph("Node-based CPU DAG", body_style), Paragraph("Node-based GPU DAG", body_style), Paragraph("Pure Scripting / SIMD", body_style)],
        [Paragraph("<b>Free Limit</b>", body_style), Paragraph("512 × 512 Basic", body_style), Paragraph("1024 × 1024 Community", body_style), Paragraph("Unlimited (RAM bound)", body_style)],
        [Paragraph("<b>Hydrology</b>", body_style), Paragraph("River Reach Device", body_style), Paragraph("Hydraulic Erosion", body_style), Paragraph("Priority-Flood + Stream Power", body_style)],
        [Paragraph("<b>Automation</b>", body_style), Paragraph("CLI Batch Builds", body_style), Paragraph("Enterprise Automation", body_style), Paragraph("100% Native Headless", body_style)]
    ]
    t_comp = Table(comp_data, colWidths=[90, 130, 140, 144])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#f1f5f9")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 14))

    story.append(Paragraph("<b>Document Reference:</b> Complete architectural markdown specification is available in the repository at <code>docs/design/PROGRAMMATIC_LARGE_SCALE_TERRAIN_SYSTEM_SPECIFICATION.md</code>.", meta_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[✓] PDF build successful: {OUTPUT_PDF} ({OUTPUT_PDF.stat().st_size} bytes)")

if __name__ == "__main__":
    build_pdf()
