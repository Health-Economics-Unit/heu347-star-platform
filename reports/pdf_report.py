from io import BytesIO
from pathlib import Path
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import textwrap
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, Image)
from matplotlib.ticker import FuncFormatter

def generate_pdf_report(
    project_name,
    project_subtitle,
    project_footername,
    project_logo,
    project_colour,
    chart_colours,
    decision,
    options,
    criteria,
    weights,
    scores,
    results,
    project_root
):

    pdf_buffer = BytesIO()

    document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=landscape(A4),
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title=f"{project_name} - Decision Analysis Report",
        author=project_footername
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=27,
        textColor=colors.HexColor(project_colour),
        alignment=TA_CENTER,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        "ReportSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=13,
        leading=17,
        textColor=colors.HexColor(project_colour),
        alignment=TA_CENTER,
        spaceAfter=16
    )

    heading_style = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=colors.HexColor(project_colour),
        spaceBefore=8,
        spaceAfter=10
    )

    subheading_style = ParagraphStyle(
        "Subheading",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        textColor=colors.HexColor(project_colour),
        spaceBefore=5,
        spaceAfter=5
    )

    body_style = ParagraphStyle(
        "BodyText",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        spaceAfter=6
    )

    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=body_style,
        fontName="Helvetica-Bold",
        textColor=colors.white,
        alignment=TA_CENTER
    )

    note_style = ParagraphStyle(
        "NoteStyle",
        parent=body_style,
        textColor=colors.HexColor(project_colour),
        borderColor=colors.HexColor(project_colour),
        borderWidth=0.7,
        borderPadding=8,
        backColor=colors.HexColor("#F3F5F4"),
        spaceBefore=6,
        spaceAfter=10
    )

    story = []


    #-----------------------------------------------------------------------------------------------
    # Cover page------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------


    logo_path = Path(project_root) / "assets" / project_logo

    if project_logo:

        logo_path = (
                Path(project_root)
                / "assets"
                / project_logo
        )

        if logo_path.is_file():
            logo = Image(
                str(logo_path),
                width=32 * mm,
                height=32 * mm,
                kind="proportional"
            )

            logo.hAlign = "CENTER"

            story.append(logo)
            story.append(Spacer(1, 8 * mm))

    story.append(
        Paragraph(
            project_name,
            title_style
        )
    )

    story.append(
        Paragraph(
            project_subtitle,
            subtitle_style
        )
    )

    story.append(Spacer(1, 10 * mm))

    story.append(
        Paragraph(
            "Decision Analysis Report",
            heading_style
        )
    )

    story.append(
        Paragraph(
            f"Generated: {datetime.now():%d %B %Y at %H:%M}",
            body_style
        )
    )

    story.append(
        Paragraph(
            project_footername,
            body_style
        )
    )

    story.append(PageBreak())

    #-----------------------------------------------------------------------------------------------
    # 1. Decision context --------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------


    story.append(
        Paragraph(
            "1. Decision Context",
            heading_style
        )
    )

    decision_title = decision.get(
        "decision_title",
        ""
    ) or "Not provided"

    decision_description = decision.get(
        "decision_description",
        ""
    ) or "Not provided"

    decision_type = decision.get(
        "decision_type",
        ""
    ) or "Not selected"

    is_star_mcda = (
            decision_type == "STAR - MCDA"
    )

    decision_data = [
        [
            Paragraph("<b>Field</b>", table_header_style),
            Paragraph("<b>Client response</b>", table_header_style)
        ],
        [
            Paragraph("Decision title", body_style),
            Paragraph(str(decision_title), body_style)
        ],
        [
            Paragraph("Decision description/objectives", body_style),
            Paragraph(str(decision_description), body_style)
        ],
        [
            Paragraph("Decision type", body_style),
            Paragraph(str(decision_type), body_style)
        ]
    ]

    decision_table = Table(
        decision_data,
        colWidths=[55 * mm, 190 * mm],
        repeatRows=1
    )

    apply_standard_table_style(
        decision_table,
        project_colour
    )

    story.append(decision_table)
    story.append(Spacer(1, 8 * mm))

    #------------------------------------------------------------------------------------------------
    # 2. Options------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------

    story.append(
        Paragraph(
            "2. Options",
            heading_style
        )
    )

    if options:

        option_data = [
            [
                Paragraph("<b>Option</b>", table_header_style)
            ]
        ]

        option_data.extend(
            [
                [
                    Paragraph(
                        str(option["name"]),
                        body_style
                    )
                ]
                for option in options
            ]
        )

        options_table = Table(
            option_data,
            colWidths=[245 * mm],
            repeatRows=1
        )

        apply_standard_table_style(
            options_table,
            project_colour
        )

        story.append(options_table)

    else:

        story.append(
            Paragraph(
                "No options were recorded.",
                body_style
            )
        )

    story.append(Spacer(1, 8 * mm))

    #------------------------------------------------------------------------------------------------
    # 3. Criteria------------------------------------------------------------------------------------------------
    #----------------------------------------------------------------------------------------------------

    story.append(
        Paragraph(
            "3. Criteria",
            heading_style
        )
    )

    if criteria:

        criteria_data = [
            [
                Paragraph("<b>Criterion</b>", table_header_style)
            ]
        ]

        criteria_data.extend(
            [
                [
                    Paragraph(
                        str(criterion["name"]),
                        body_style
                    )
                ]
                for criterion in criteria
            ]
        )

        criteria_table = Table(
            criteria_data,
            colWidths=[245 * mm],
            repeatRows=1
        )

        apply_standard_table_style(
            criteria_table,
            project_colour
        )

        story.append(criteria_table)

    else:

        story.append(
            Paragraph(
                "No criteria were recorded.",
                body_style
            )
        )

    story.append(PageBreak())

    #------------------------------------------------------------------------------------------------------
    # 4. Weighting------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------

    story.append(
        Paragraph(
            "4. Criterion Weighting",
            heading_style
        )
    )

    story.append(
        Paragraph(
            (
                "The weights represent the relative importance "
                "assigned to each criterion. The normalised weights are "
                "expressed as percentages and sum to 100%."
            ),
            note_style
        )
    )

    weight_data = [
        [
            Paragraph("<b>Criterion</b>", table_header_style),
            Paragraph("<b>Weight</b>", table_header_style),
            Paragraph("<b>Normalised weight</b>", table_header_style)
        ]
    ]

    for item in weights.values():

        weight_data.append(
            [
                Paragraph(
                    str(item["criterion"]),
                    body_style
                ),
                f"{item['raw_weight']:.0f}",
                f"{item['normalised_weight']:.1%}"
            ]
        )

    total_raw_weight = sum(
        item["raw_weight"]
        for item in weights.values()
    )

    weight_data.append(
        [
            Paragraph("<b>Total</b>", body_style),
            f"{total_raw_weight:.0f}",
            "100.0%" if weights else "0.0%"
        ]
    )

    weight_table = Table(
        weight_data,
        colWidths=[
            145 * mm,
            50 * mm,
            50 * mm
        ],
        repeatRows=1
    )

    apply_standard_table_style(
        weight_table,
        project_colour
    )

    story.append(weight_table)
    story.append(Spacer(1, 8 * mm))

    #------------------------------------------------------------------------------------------------------
    # 5. Scores matrix ------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------

    story.append(
        Paragraph(
            "5. Option Scores",
            heading_style
        )
    )

    criterion_ids = [
        criterion["id"]
        for criterion in criteria
    ]

    criterion_names = {
        criterion["id"]: criterion["name"]
        for criterion in criteria
    }

    scores_header = [
        Paragraph("<b>Option</b>", table_header_style)
    ]

    scores_header.extend(
        Paragraph(
            f"<b>{criterion_names[criterion_id]}</b>",
            table_header_style
        )
        for criterion_id in criterion_ids
    )

    scores_data = [scores_header]

    for option_data in scores.values():

        row = [
            Paragraph(
                str(option_data["option"]),
                body_style
            )
        ]

        for criterion_id in criterion_ids:

            criterion_score = (
                option_data
                .get("criteria_scores", {})
                .get(criterion_id, {})
                .get("score", 0)
            )

            row.append(
                f"{criterion_score:.0f}"
            )

        scores_data.append(row)

    score_column_width = (
        180 * mm / max(len(criterion_ids), 1)
    )

    scores_table = Table(
        scores_data,
        colWidths=[
            65 * mm
        ] + [
            score_column_width
            for _ in criterion_ids
        ],
        repeatRows=1
    )

    apply_standard_table_style(
        scores_table,
        project_colour
    )

    story.append(scores_table)
    story.append(PageBreak())

    # ------------------------------------------------------------------------------------------------------
    # 6. Decision Matrix
    # ------------------------------------------------------------------------------------------------------

    story.append(
        Paragraph(
            "6. Decision Matrix",
            heading_style
        )
    )

    if results:

        result_criteria = list(
            results[0]
            .get("weighted_scores", {})
            .keys()
        )

        # ---------------- Header ----------------

        results_header = [
            Paragraph(
                "<b>Option</b>",
                table_header_style
            )
        ]

        results_header.extend(
            Paragraph(
                f"<b>{criterion}</b>",
                table_header_style
            )
            for criterion in result_criteria
        )

        results_header.append(
            Paragraph(
                "<b>Benefit Score</b>",
                table_header_style
            )
        )

        if is_star_mcda:

            results_header.append(
                Paragraph(
                    "<b>Total Benefit</b>",
                    table_header_style
                )
            )

            results_header.append(
                Paragraph(
                    "<b>Total Cost</b>",
                    table_header_style
                )
            )

            results_header.append(
                Paragraph(
                    "<b>VFM Ratio (£ per benefit)</b>",
                    table_header_style
                )
            )

        results_header.append(
            Paragraph(
                "<b>Rank</b>",
                table_header_style
            )
        )

        results_data = [results_header]

        # ---------------- Rows ----------------

        for result in results:

            result_row = [
                Paragraph(
                    str(result.get("option", "")),
                    body_style
                )
            ]

            # Weighted criterion values
            result_row.extend(
                f"{float(result.get('weighted_scores', {}).get(criterion, 0) or 0):.2f}"
                for criterion in result_criteria
            )

            # Benefit Score
            result_row.append(
                f"{float(result.get('benefit_score', 0) or 0):.2f}"
            )

            if is_star_mcda:

                # Total Benefit
                result_row.append(
                    f"£{float(result.get('total_benefit', 0) or 0):,.2f}"
                )

                # Total Cost
                result_row.append(
                    f"£{float(result.get('cost', 0) or 0):,.2f}"
                )

                # VFM Ratio
                vfm_ratio = result.get("vfm_ratio")

                try:
                    numeric_vfm = float(vfm_ratio)
                    valid_vfm = np.isfinite(numeric_vfm)
                except (TypeError, ValueError):
                    numeric_vfm = None
                    valid_vfm = False

                if valid_vfm:
                    result_row.append(
                        f"£{numeric_vfm:,.2f}"
                    )
                else:
                    result_row.append(
                        "Worst VFM"
                    )

            # Rank
            result_row.append(
                str(result.get("rank", ""))
            )

            results_data.append(result_row)

        # Always derive the column count from the actual header
        total_result_columns = len(results_header)

        # Full usable table width: 245 mm
        option_column_width = 42 * mm
        remaining_width = 203 * mm

        other_column_width = (
            remaining_width
            / max(total_result_columns - 1, 1)
        )

        results_table = Table(
            results_data,
            colWidths=[
                option_column_width
            ] + [
                other_column_width
                for _ in range(total_result_columns - 1)
            ],
            repeatRows=1,
            hAlign="LEFT"
        )

        apply_standard_table_style(
            results_table,
            project_colour
        )

        # Keep the heading and table near each other where possible
        story.append(results_table)
        story.append(Spacer(1, 8 * mm))

    else:

        story.append(
            Paragraph(
                "No calculated results were available.",
                body_style
            )
        )

    story.append(PageBreak())

    # ------------------------------------------------------------------------------------------------------
    # 7. Visualisation
    # ------------------------------------------------------------------------------------------------------

    if results:

        # STAR-MCDA
        if is_star_mcda:

            story.append(
                Paragraph(
                    "7. Visualisation",
                    heading_style
                )
            )

            story.append(
                Paragraph(
                    (
                        "Each coloured area represents an intervention. "
                        "Interventions are ordered by value for money and plotted "
                        "cumulatively by total cost and total benefit. The width of "
                        "each area represents total cost, while its height represents "
                        "total benefit. Interventions with a lower cost per unit of "
                        "benefit indicate better value for money."
                    ),
                    body_style
                )
            )

            frontier_chart_buffer = create_efficiency_frontier_chart(
                results=results,
                chart_colours=chart_colours,
                project_colour=project_colour
            )

            frontier_image = Image(
                frontier_chart_buffer,
                width=235 * mm,
                height=120 * mm
            )

            frontier_image.hAlign = "CENTER"

            story.append(frontier_image)

        # MCDA
        else:

            story.append(
                Paragraph(
                    "7. Visualisation",
                    heading_style
                )
            )

            chart_buffer = create_results_chart(
                results=results,
                chart_colours=chart_colours,
                project_colour=project_colour
            )

            chart_image = Image(
                chart_buffer,
                width=240 * mm,
                height=125 * mm
            )

            chart_image.hAlign = "CENTER"

            story.append(chart_image)

    #------------------------------------------------------------------------------------------------------
    # Generate PDF----------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------

    document.build(
        story,
        onFirstPage=lambda canvas, doc: add_page_footer(
            canvas,
            doc,
            project_footername,
            project_colour
        ),
        onLaterPages=lambda canvas, doc: add_page_footer(
            canvas,
            doc,
            project_footername,
            project_colour
        )
    )

    pdf_buffer.seek(0)

    return pdf_buffer


def apply_standard_table_style(
    table,
    project_colour
):

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(project_colour)
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold"
                ),
                (
                    "ALIGN",
                    (1, 1),
                    (-1, -1),
                    "CENTER"
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE"
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.HexColor("#C9DEDA")
                ),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [
                        colors.white,
                        colors.HexColor("#F3F5F4")
                    ]
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6
                )
            ]
        )
    )

#---------------------------Chart on the pdf report-------------------------------

def create_results_chart(
    results,
    chart_colours,
    project_colour
):

    chart_buffer = BytesIO()

    criterion_names = list(
        results[0]["weighted_scores"].keys()
    )

    option_names = [
        result["option"]
        for result in results
    ]

    wrapped_option_names = [
        "\n".join(textwrap.wrap(name, width=18))
        for name in option_names
    ]

    positions = np.arange(
        len(option_names)
    )

    bottom_values = np.zeros(
        len(option_names)
    )

    fig, ax = plt.subplots(
        figsize=(12, 5.5)
    )

    for index, criterion_name in enumerate(
        criterion_names
    ):

        criterion_values = [
            result["weighted_scores"].get(
                criterion_name,
                0
            )
            for result in results
        ]

        ax.bar(
            positions,
            criterion_values,
            bottom=bottom_values,
            label=criterion_name,
            color=chart_colours[
                index % len(chart_colours)
            ],
            width=0.65
        )

        bottom_values += np.array(
            criterion_values
        )

    for index, result in enumerate(results):

        ax.text(
            index,
            result["benefit_score"] + 1,
            f"{result['benefit_score']:.2f}",
            ha="center",
            va="bottom",
            fontweight="bold",
            color=project_colour
        )

    ax.set_title(
        "Contribution of Criteria to Overall Benefit Score",
        fontsize=14,
        fontweight="bold",
        color=project_colour,
        pad=15
    )

    ax.set_xlabel("Options")
    ax.set_ylabel("Weighted score")

    ax.set_xticks(positions)
    ax.set_xticklabels(wrapped_option_names, fontsize=10)

    ax.legend(
        title="Criteria",
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
        frameon=False
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.3
    )

    ax.set_axisbelow(True)

    fig.tight_layout()
    plt.subplots_adjust(bottom=0.25)

    fig.savefig(
        chart_buffer,
        format="png",
        dpi=180,
        bbox_inches="tight"
    )

    plt.close(fig)

    chart_buffer.seek(0)

    return chart_buffer

# ----------------STAR-MCDA Efficiency Frontier for PDF-------------------------------

def create_efficiency_frontier_chart(
    results,
    chart_colours,
    project_colour
):

    chart_buffer = BytesIO()

    if not results:

        fig, ax = plt.subplots(
            figsize=(12, 5.5)
        )

        ax.text(
            0.5,
            0.5,
            "No STAR-MCDA results available.",
            ha="center",
            va="center",
            transform=ax.transAxes
        )

        ax.axis("off")

        fig.savefig(
            chart_buffer,
            format="png",
            dpi=180,
            bbox_inches="tight"
        )

        plt.close(fig)
        chart_buffer.seek(0)

        return chart_buffer

    def get_vfm_sort_value(result):

        vfm_ratio = result.get("vfm_ratio")

        try:
            numeric_vfm = float(vfm_ratio)
        except (TypeError, ValueError):
            return float("inf")

        if not np.isfinite(numeric_vfm):
            return float("inf")

        return numeric_vfm

    # Lowest cost per unit of benefit first.
    # Missing or invalid VFM values appear last.
    ordered_results = sorted(
        results,
        key=get_vfm_sort_value
    )

    cumulative_cost = 0.0
    cumulative_benefit = 0.0

    fig, ax = plt.subplots(
        figsize=(12, 5.5)
    )

    for index, result in enumerate(ordered_results):

        option_name = str(
            result.get("option", "")
        )

        total_cost = float(
            result.get("cost", 0) or 0
        )

        benefit_score = float(
            result.get("benefit_score", 0) or 0
        )

        total_benefit = float(
            result.get("total_benefit", 0) or 0
        )

        vfm_ratio = result.get("vfm_ratio")

        start_cost = cumulative_cost
        start_benefit = cumulative_benefit

        cumulative_cost += total_cost
        cumulative_benefit += total_benefit

        colour = chart_colours[
            index % len(chart_colours)
        ]

        # Base represents total cost.
        # Height represents total benefit.
        ax.fill(
            [
                start_cost,
                cumulative_cost,
                cumulative_cost
            ],
            [
                start_benefit,
                start_benefit,
                cumulative_benefit
            ],
            color=colour,
            alpha=0.8,
            label=option_name
        )

        try:
            numeric_vfm = float(vfm_ratio)
            valid_vfm = np.isfinite(numeric_vfm)
        except (TypeError, ValueError):
            numeric_vfm = None
            valid_vfm = False

        if valid_vfm:
            vfm_text = f"£{numeric_vfm:,.2f} per benefit"
        else:
            vfm_text = "Worst VFM"

        # Position the label inside its intervention triangle.
        label_x = start_cost + (total_cost * 0.68)
        label_y = start_benefit + (total_benefit * 0.30)

        option_label = (
            f"{option_name}\n"
            f"Total Cost: £{total_cost:,.2f}\n"
            f"Benefit Score: {benefit_score:,.2f}\n"
            f"Total Benefit: £{total_benefit:,.2f}\n"
            f"VFM Ratio: {vfm_text}"
        )

        ax.text(
            label_x,
            label_y,
            option_label,
            ha="center",
            va="center",
            fontsize=7,
            color="#1F1F1F",
            bbox={
                "boxstyle": "round,pad=0.25",
                "facecolor": "white",
                "edgecolor": colour,
                "alpha": 0.9
            }
        )

        # Make axes start exactly at zero, matching the app chart
        ax.set_xlim(
            left=0,
            right=cumulative_cost * 1.05
        )

        ax.set_ylim(
            bottom=0,
            top=cumulative_benefit * 1.05
        )

        # Remove Matplotlib's automatic axis padding
        ax.margins(
            x=0,
            y=0
        )

    ax.set_title(
        "Efficiency Frontier",
        fontsize=14,
        fontweight="bold",
        color=project_colour,
        pad=15
    )

    ax.set_xlabel(
        "Cumulative Cost (£)"
    )

    ax.set_ylabel(
        "Cumulative Total Benefit"
    )

    ax.xaxis.set_major_formatter(
        FuncFormatter(
            lambda value, position: f"£{value:,.0f}"
        )
    )

    ax.yaxis.set_major_formatter(
        FuncFormatter(
            lambda value, position: f"{value:,.0f}"
        )
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.grid(
        axis="both",
        linestyle="--",
        alpha=0.2
    )

    ax.set_axisbelow(True)

    ax.legend(
        title="Interventions",
        bbox_to_anchor=(1.02, 1),
        loc="upper left",
        frameon=False
    )

    fig.tight_layout()

    fig.savefig(
        chart_buffer,
        format="png",
        dpi=180,
        bbox_inches="tight"
    )

    plt.close(fig)
    chart_buffer.seek(0)

    return chart_buffer

#-------------page footer-------------------------------------------------------

def add_page_footer(
    canvas,
    document,
    footer_text,
    project_colour
):

    canvas.saveState()

    canvas.setStrokeColor(
        colors.HexColor(project_colour)
    )

    canvas.line(
        18 * mm,
        12 * mm,
        landscape(A4)[0] - 18 * mm,
        12 * mm
    )

    canvas.setFillColor(
        colors.HexColor(project_colour)
    )

    canvas.setFont(
        "Helvetica",
        8
    )

    canvas.drawString(
        18 * mm,
        7 * mm,
        footer_text
    )

    canvas.drawRightString(
        landscape(A4)[0] - 18 * mm,
        7 * mm,
        f"Page {document.page}"
    )

    canvas.restoreState()