import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and print total page numbers (e.g. Page 1 of 3).
    Also paints publication-quality running headers and footers.
    """
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
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Running Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(45, 755, "Routing Protocol Simulator: Methodology & Benchmarking Report")
            self.drawRightString(567, 755, "DUAL (EIGRP) vs. Path Vector (BGP)")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(45, 748, 567, 748)

        # Running Footer (all pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(45, 42, 567, 42)
        
        self.drawString(45, 30, "Author: Neeraj Roy  |  GitHub: NeerajRoy24/routing-protocol-simulator")
        self.drawRightString(567, 30, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


def create_methodology_pdf(output_filename="Routing_Protocol_Simulator_Methodology.pdf"):
    # Page margins: 45 pt (0.625 inch) for optimal layout balance
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    # Typography styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=4
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#0284C7"),
        spaceAfter=8
    )

    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#334155")
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#1E3A8A"),
        spaceBefore=6,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155"),
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11.5,
        textColor=colors.HexColor("#0F172A")
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor("#0F172A")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=9.5,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#1E293B")
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell_style,
        fontName='Helvetica-Bold'
    )

    table_cell_center = ParagraphStyle(
        'TableCellCenter',
        parent=table_cell_style,
        alignment=1
    )

    story = []

    # =========================================================================
    # PAGE 1: TITLE, METADATA, ABSTRACT, & SECTION 1 (ALGORITHMIC FOUNDATIONS)
    # =========================================================================
    story.append(Paragraph("Routing Protocol Simulator: Methodology & Benchmarking Report", title_style))
    story.append(Paragraph("A Comparative Architectural Analysis of Diffusing Update Algorithm (DUAL / EIGRP) and Path Vector (BGP)", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#0284C7"), spaceAfter=8))

    meta_data = [
        [
            Paragraph("<b>Author:</b> Neeraj Roy", meta_style),
            Paragraph("<b>Protocol Paradigms:</b> Advanced Distance-Vector vs. Path Vector", meta_style),
            Paragraph("<b>Repository:</b> NeerajRoy24/routing-protocol-simulator", meta_style)
        ],
        [
            Paragraph("<b>Target Autonomous Systems:</b> 6 AS Domains", meta_style),
            Paragraph("<b>Evaluation Engine:</b> Python NetworkX + Matplotlib", meta_style),
            Paragraph("<b>Date:</b> October 2026  |  <b>Version:</b> 1.0.0", meta_style)
        ]
    ]
    t_meta = Table(meta_data, colWidths=[170, 202, 150])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 0.6, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 6))

    summary_text = (
        "<b>Executive Abstract:</b> Traditional academic network curriculum typically contrasts simple Bellman-Ford "
        "(RIP) against Dijkstra link-state (OSPF). However, production enterprise networks and the global Internet rely "
        "on advanced hybrid protocols engineered for rapid sub-second convergence and policy-driven loop prevention. "
        "This project presents a rigorous simulator and comparative benchmark evaluating Cisco's <b>Diffusing Update "
        "Algorithm (DUAL / EIGRP)</b> and the Border Gateway Protocol's <b>Path Vector (BGP)</b> engine over an asymmetric "
        "multi-autonomous-system virtual mesh. We examine loop-freedom invariants, mathematical metric formulas, backup "
        "successor feasibility conditions, fault-induced reconvergence latency, and algorithmic scaling up to 100 routers."
    )
    t_summary = Table([[Paragraph(summary_text, callout_style)]], colWidths=[522])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EFF6FF")),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#3B82F6")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(t_summary)
    story.append(Spacer(1, 6))

    story.append(Paragraph("1. Algorithmic Foundations & Protocol Mechanics", h1_style))
    story.append(Paragraph(
        "Routing algorithms must satisfy two fundamental invariants: <i>correctness (guaranteed loop-freedom at all times)</i> "
        "and <i>rapid convergence (minimal packet loss and downtime during topological disruptions)</i>. This simulation models "
        "two fundamentally distinct mechanisms designed to achieve loop freedom without global link-state floods.",
        body_style
    ))

    story.append(Paragraph("1.1 Diffusing Update Algorithm (DUAL / EIGRP - RFC 7868)", h2_style))
    story.append(Paragraph(
        "DUAL models an advanced Distance Vector protocol utilizing a composite metric combining link bandwidth and latency. "
        "The standard scaled metric formula implemented in our simulation engine is:",
        body_style
    ))

    formula_table = Table([[
        Paragraph(
            "<b>Classic Composite Metric Equation:</b><br/>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<code>Metric = 256 * [ (10^4 / Bandwidth_Mbps) + (Delay_ms / 10) ]</code><br/>"
            "This metric inversely rewards high throughput while penalizing path propagation latency.",
            code_style
        )
    ]], colWidths=[522])
    formula_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('BOX', (0, 0), (-1, -1), 0.6, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(formula_table)
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<b>The Feasibility Condition (FC):</b> DUAL guarantees instantaneous local failover by maintaining backup neighbors "
        "called <b>Feasible Successors (FS)</b>. A neighbor <i>N</i> qualifies as a Feasible Successor for destination <i>D</i> "
        "if and only if: <br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>Reported Distance (RD_N->D) &lt; Feasible Distance (FD_Local->D)</b><br/>"
        "Because <i>N</i>'s path to <i>D</i> is strictly shorter than the current local Feasible Distance, it is mathematically "
        "impossible for <i>N</i>'s path to loop through the local node. If the primary Successor link fails and an FS exists, "
        "failover occurs in <b>&lt; 5 ms (Passive state)</b>. If no FS exists, the router enters <b>Active state</b> and broadcasts "
        "diffusing queries to neighboring routers, causing bounded convergence latency.",
        body_style
    ))

    story.append(Paragraph("1.2 Path Vector Routing (BGP-4 - RFC 4271)", h2_style))
    story.append(Paragraph(
        "Unlike interior IGP metrics based on physical link attributes, the Border Gateway Protocol (BGP) operates across "
        "independent Autonomous Systems (AS). BGP prevents routing loops by explicitly recording each traversed AS number in "
        "the <code>AS_PATH</code> attribute. If a router detects its own ASN within the received path vector, the route is dropped immediately.<br/>"
        "<b>BGP Decision Hierarchy Modeled:</b> (1) <b>Highest Local Preference (<code>LOCAL_PREF</code>)</b>: Policy override configured by network operators; "
        "(2) <b>Shortest <code>AS_PATH</code> Length</b>: Hop-by-hop autonomous system traversal minimization; "
        "(3) <b>Lowest Latency</b>: Cumulative physical delay fallback when policies and hop counts are identical.",
        body_style
    ))

    # Clean Page Break to Page 2
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: NETWORK TOPOLOGY, METHODOLOGY, & EXPERIMENTAL RESULTS TABLE
    # =========================================================================
    story.append(Paragraph("2. Virtual Network Topology & Simulation Architecture", h1_style))
    story.append(Paragraph(
        "The simulation models a 6-router meshed backbone network spanning 6 Autonomous Systems (AS 65001 through AS 65006). "
        "The topology is deliberately constructed with heterogeneous link capacities to examine the divergent routing paths "
        "chosen by throughput/latency optimization (DUAL) versus policy/hop-count rules (BGP).",
        body_style
    ))

    topo_headers = [
        Paragraph("Link Edge", table_header_style),
        Paragraph("Autonomous Systems", table_header_style),
        Paragraph("Bandwidth", table_header_style),
        Paragraph("Delay", table_header_style),
        Paragraph("DUAL Metric", table_header_style),
        Paragraph("BGP LocalPref", table_header_style),
        Paragraph("Link Classification", table_header_style)
    ]

    topo_rows = [
        [Paragraph("R1 <-> R2", table_cell_bold), Paragraph("AS 65001 <-> AS 65002", table_cell_style), Paragraph("1000 Mbps", table_cell_center), Paragraph("4 ms", table_cell_center), Paragraph("2,662", table_cell_center), Paragraph("150 (High)", table_cell_center), Paragraph("Fiber Backbone", table_cell_style)],
        [Paragraph("R2 <-> R3", table_cell_bold), Paragraph("AS 65002 <-> AS 65003", table_cell_style), Paragraph("1000 Mbps", table_cell_center), Paragraph("4 ms", table_cell_center), Paragraph("2,662", table_cell_center), Paragraph("150 (High)", table_cell_center), Paragraph("Fiber Backbone (Cut Target)", table_cell_style)],
        [Paragraph("R3 <-> R5", table_cell_bold), Paragraph("AS 65003 <-> AS 65005", table_cell_style), Paragraph("1000 Mbps", table_cell_center), Paragraph("4 ms", table_cell_center), Paragraph("2,662", table_cell_center), Paragraph("150 (High)", table_cell_center), Paragraph("Fiber Backbone", table_cell_style)],
        [Paragraph("R5 <-> R6", table_cell_bold), Paragraph("AS 65005 <-> AS 65006", table_cell_style), Paragraph("1000 Mbps", table_cell_center), Paragraph("4 ms", table_cell_center), Paragraph("2,662", table_cell_center), Paragraph("150 (High)", table_cell_center), Paragraph("Fiber Backbone", table_cell_style)],
        [Paragraph("R2 <-> R4", table_cell_bold), Paragraph("AS 65002 <-> AS 65004", table_cell_style), Paragraph("100 Mbps", table_cell_center), Paragraph("15 ms", table_cell_center), Paragraph("25,984", table_cell_center), Paragraph("120 (Med)", table_cell_center), Paragraph("Backup Mesh Route", table_cell_style)],
        [Paragraph("R4 <-> R5", table_cell_bold), Paragraph("AS 65004 <-> AS 65005", table_cell_style), Paragraph("100 Mbps", table_cell_center), Paragraph("12 ms", table_cell_center), Paragraph("25,907", table_cell_center), Paragraph("120 (Med)", table_cell_center), Paragraph("Backup Mesh Route", table_cell_style)],
        [Paragraph("R3 <-> R6", table_cell_bold), Paragraph("AS 65003 <-> AS 65006", table_cell_style), Paragraph("100 Mbps", table_cell_center), Paragraph("25 ms", table_cell_center), Paragraph("26,240", table_cell_center), Paragraph("120 (Med)", table_cell_center), Paragraph("Cross-AS Backup Route", table_cell_style)],
        [Paragraph("R1 <-> R4", table_cell_bold), Paragraph("AS 65001 <-> AS 65004", table_cell_style), Paragraph("10 Mbps", table_cell_center), Paragraph("45 ms", table_cell_center), Paragraph("257,152", table_cell_center), Paragraph("100 (Default)", table_cell_center), Paragraph("Low-Speed Direct Transit", table_cell_style)],
        [Paragraph("R4 <-> R6", table_cell_bold), Paragraph("AS 65004 <-> AS 65006", table_cell_style), Paragraph("10 Mbps", table_cell_center), Paragraph("45 ms", table_cell_center), Paragraph("257,152", table_cell_center), Paragraph("100 (Default)", table_cell_center), Paragraph("Low-Speed Direct Transit", table_cell_style)],
    ]

    t_topo = Table([topo_headers] + topo_rows, colWidths=[65, 100, 60, 42, 60, 75, 120])
    t_topo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_topo)
    story.append(Spacer(1, 8))

    story.append(Paragraph("3. Fault Injection & Reconvergence Methodology", h1_style))
    story.append(Paragraph(
        "To rigorously quantify routing resilience, our simulation pipeline executes two successive phases: "
        "<b>Phase 1 (Steady State)</b> and <b>Phase 2 (Link Failure Injection)</b>. In Phase 2, a complete fiber cut is injected "
        "on edge <code>R2 <-> R3</code> (status set to <code>DOWN</code>). This severs the primary 4-hop gigabit backbone. "
        "The simulator immediately invokes reconvergence routines to observe path recalculation, end-to-end packet delay, "
        "and bottleneck bandwidth preservation.",
        body_style
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("4. Quantitative Benchmarking & Experimental Results", h1_style))
    story.append(Paragraph(
        "Table 2 summarizes the empirical routing decisions, metrics, latency, and bottleneck bandwidths computed by the simulation engine.",
        body_style
    ))

    res_headers = [
        Paragraph("Phase / State", table_header_style),
        Paragraph("Routing Protocol", table_header_style),
        Paragraph("Selected Router Path", table_header_style),
        Paragraph("Computed Metric", table_header_style),
        Paragraph("End-to-End Delay", table_header_style),
        Paragraph("Bottleneck BW", table_header_style)
    ]

    res_rows = [
        [
            Paragraph("Phase 1<br/>(Steady-State)", table_cell_bold),
            Paragraph("<b>DUAL (EIGRP)</b>", table_cell_style),
            Paragraph("R1 -> R2 -> R3 -> R5 -> R6", table_cell_style),
            Paragraph("10,648 (Scaled FD)", table_cell_center),
            Paragraph("<b>16 ms</b> (Ultra-fast)", table_cell_center),
            Paragraph("1000 Mbps", table_cell_center)
        ],
        [
            Paragraph("Phase 1<br/>(Steady-State)", table_cell_bold),
            Paragraph("<b>Path Vector (BGP)</b>", table_cell_style),
            Paragraph("R1 -> R2 -> R3 -> R6", table_cell_style),
            Paragraph("3 AS-Hops (LocalPref 150)", table_cell_center),
            Paragraph("33 ms", table_cell_center),
            Paragraph("100 Mbps", table_cell_center)
        ],
        [
            Paragraph("Phase 2<br/>(Post-Failure Cut)", table_cell_bold),
            Paragraph("<b>DUAL (EIGRP)</b>", table_cell_style),
            Paragraph("R1 -> R2 -> R4 -> R5 -> R6", table_cell_style),
            Paragraph("57,215 (Backup FS)", table_cell_center),
            Paragraph("<b>35 ms</b>", table_cell_center),
            Paragraph("100 Mbps", table_cell_center)
        ],
        [
            Paragraph("Phase 2<br/>(Post-Failure Cut)", table_cell_bold),
            Paragraph("<b>Path Vector (BGP)</b>", table_cell_style),
            Paragraph("R1 -> R2 -> R4 -> R6", table_cell_style),
            Paragraph("3 AS-Hops (LocalPref 150)", table_cell_center),
            Paragraph("64 ms", table_cell_center),
            Paragraph("10 Mbps", table_cell_center)
        ],
    ]

    t_res = Table([res_headers] + res_rows, colWidths=[80, 85, 155, 87, 57, 58])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1E293B")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_res)

    # Clean Page Break to Page 3
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: VISUAL BENCHMARKS, ARCHITECTURAL FINDINGS, & CONCLUSION
    # =========================================================================
    chart_path = os.path.join(os.path.dirname(__file__), "performance_analysis.png")
    if os.path.exists(chart_path):
        story.append(Paragraph("<b>Figure 1:</b> Empirical Convergence Latency Scaling & Post-Failure Delay Benchmarks", h2_style))
        story.append(Image(chart_path, width=522, height=195))
        story.append(Spacer(1, 6))

    story.append(Paragraph("5. Architectural Analysis & Key Insights", h1_style))
    story.append(Paragraph(
        "<b>1. Composite Bandwidth+Delay Metrics Maximize Data-Plane Throughput:</b><br/>"
        "In steady-state, DUAL prioritized throughput and delay, selecting the 4-hop gigabit fiber route (<code>R1->R2->R3->R5->R6</code>), "
        "achieving <b>16 ms</b> latency and <b>1000 Mbps</b> bottleneck throughput. Conversely, BGP chose <code>R1->R2->R3->R6</code> "
        "solely because it offered fewer AS hops (3 hops), routing traffic over an inferior 100 Mbps link with double the physical delay (<b>33 ms</b>).",
        body_style
    ))
    story.append(Paragraph(
        "<b>2. Resiliency Under Core Backbone Link Cuts:</b><br/>"
        "When link <code>R2 <-> R3</code> was severed, DUAL preserved an end-to-end delay of <b>35 ms</b> by utilizing high-capacity "
        "100 Mbps backup paths via Feasible Successor. BGP, governed by AS-hop minimization, rerouted through legacy 10 Mbps links, causing end-to-end "
        "delay to spike to <b>64 ms</b> with a 90% loss in bottleneck bandwidth capacity.",
        body_style
    ))
    story.append(Paragraph(
        "<b>3. Algorithmic Convergence Scaling Over Large Network Diameters (N = 6 to 100):</b><br/>"
        "As demonstrated in Figure 1 (Left Panel), when a Feasible Successor is present in the topology table, DUAL achieves near flat-line recovery "
        "(5 - 45 ms) independent of network scale. In contrast, BGP route convergence exhibits heavy scaling penalties (1,200 - 10,000 ms) "
        "due to TCP session state overhead, Minimum Route Advertisement Interval (MRAI) timers, and BGP path-hunting delays.",
        body_style
    ))

    story.append(Paragraph("6. Engineering Conclusion & Protocol Selection Matrix", h1_style))
    matrix_headers = [
        Paragraph("Evaluation Dimension", table_header_style),
        Paragraph("DUAL (EIGRP)", table_header_style),
        Paragraph("Path Vector (BGP)", table_header_style),
        Paragraph("Recommended Engineering Context", table_header_style)
    ]
    matrix_rows = [
        [Paragraph("Convergence Speed", table_cell_bold), Paragraph("Sub-second (< 5 ms via FS)", table_cell_style), Paragraph("Seconds to Minutes (MRAI bounded)", table_cell_style), Paragraph("DUAL for latency-critical campus/LAN/WAN", table_cell_style)],
        [Paragraph("Loop Prevention", table_cell_bold), Paragraph("Feasibility Condition (RD < FD)", table_cell_style), Paragraph("Explicit AS_PATH Attribute", table_cell_style), Paragraph("BGP for inter-AS policy & loop detection", table_cell_style)],
        [Paragraph("Metric Sensitivity", table_cell_bold), Paragraph("Bandwidth + Latency Composite", table_cell_style), Paragraph("Policy (LocalPref, AS-Path, MED)", table_cell_style), Paragraph("DUAL for performance; BGP for policy", table_cell_style)],
        [Paragraph("Scalability Limits", table_cell_bold), Paragraph("Moderate (Enterprise Core / WAN)", table_cell_style), Paragraph("Global Internet Scale (> 900k routes)", table_cell_style), Paragraph("BGP for global autonomous transit", table_cell_style)],
    ]
    t_matrix = Table([matrix_headers] + matrix_rows, colWidths=[110, 120, 132, 160])
    t_matrix.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0F172A")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
    ]))
    story.append(t_matrix)

    # References
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "<b>References:</b> [1] RFC 7868: Cisco's Enhanced Interior Gateway Routing Protocol (EIGRP). "
        "[2] RFC 4271: A Border Gateway Protocol 4 (BGP-4). "
        "[3] Garcia-Lunes-Aceves, J. J. (1993). Loop-Free Routing Using Diffusing Computations. IEEE/ACM Trans. Networking.",
        ParagraphStyle('RefStyle', parent=styles['Normal'], fontName='Helvetica', fontSize=7, leading=9.5, textColor=colors.HexColor("#64748B"))
    ))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] Successfully generated methodology PDF: {output_filename}")


if __name__ == "__main__":
    create_methodology_pdf()
