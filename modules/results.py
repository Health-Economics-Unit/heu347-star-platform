#This page will display outputs/results

from shiny import ui
from modules.components import results_nav_card

results_page = ui.div(

    ui.br(),

    ui.h1("Results", class_="page-title"),

    #-------Dynamic introductory text + note for MCDA / STAR-MCDA-------------
    #----------How to Interpret the Results-----------------------------
    ui.card(

        ui.card_header("How to Interpret the Results"),

        ui.output_ui("results_interpretation"),

        class_="hse-card"
    ),

    ##---------------Results summary----------------------

    #---------Decision Matrix---------------------------
    ui.card(

        ui.card_header("Decision Matrix"),
        ui.output_ui("decision_matrix"),
        class_="hse-card"

    ),

    #---------Visualisation---------------------------
    ui.card(
        ui.card_header("Visualisation"),

         ui.output_ui("visualisation_description"),

        ui.output_ui("results_chart_container"),
        class_="hse-card"
    ),

#----------------Need to make changes section---------------------------------------------------------

    ui.card(

        ui.card_header("Need to make changes?"),

        ui.p(
            "Return to any stage and update your inputs."
        ),

        ui.layout_columns(

            results_nav_card(
                "edit_options","📋", "Options"
            ),

            results_nav_card(
                "edit_criteria","📌", "Criteria"
            ),

            results_nav_card(
                "edit_weighting","🎚️", "Weighting"
            ),

            results_nav_card(
                "edit_scores","📝", "Scores"
            ),

            ui.output_ui("results_cost_card"),

            col_widths=(1,1,1,1,1),
            gap="10px"

        ),

        class_="hse-card"
    ),

#----------------Download button----------------------------------------------------------------------

    ui.div(
        ui.download_button(

        "download_report",
        "📄 Download Results Report",
        class_="download-button"
        ),

        style="""
                display:flex;
                justify-content:flex-end;
                margin-top:20px;
                margin-bottom:20px;
            """
    )

)