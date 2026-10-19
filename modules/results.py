#This page will display outputs/results

from shiny import ui
from config.active_project import chart_colours



results_page = ui.div(

    ui.br(),

    ui.h1("Results", class_="page-title"),

    ui.br(),

    ui.p(
        "The results below combine the scores and weights entered "
        "during the decision-making process."
    ),

    ui.p(
        "The Decision Matrix shows the weighted contribution of each "
        "criterion to the overall benefit score for every option. "
        "The Visualisation provides a graphical representation of the same "
        "results to support discussion and decision-making."
    ),

    ui.strong(
        "ℹ️ Note: Results will only appear once options, criteria, "
        "weights and scores have been completed.",
        class_="page-title"
    ),

    ui.br(),
    ui.br(),

    ui.card(

        ui.card_header("How to Interpret the Results"),

        ui.tags.ul(

            ui.tags.li(
                "Criteria columns display weighted scores "
                "(normalised weight × score)."
            ),

            ui.tags.li(
                "Benefit Score is the sum of all weighted "
                "criterion scores for an option."
            ),

            ui.tags.li(
                "Options are ranked according to their "
                "overall Benefit Score."
            ),

            ui.tags.li(
                "Higher Benefit Scores indicate stronger "
                "overall performance against the selected criteria."
            )

        )

    ),

    ui.br(),

     ui.card(

         ui.card_header("Results Summary"),
         ui.output_ui("results_summary"),
         class_="hse-card"

     ),

    ui.card(

        ui.card_header("Decision Matrix"),
        ui.output_ui("decision_matrix"),
        class_="hse-card"

    ),

    ui.br(),

    ui.card(

        ui.card_header("Visualisation"),
         ui.p("Each coloured segment represents the weighted contribution "
              "of a criterion to the overall benefit score. Larger bars "
              "indicate options with higher total benefit scores."
         ),
        ui.output_plot("results_chart", height="600px"),
        class_="page-card"

    ),

#----------------Download button--------------------------------------------------------------

    ui.div(
        ui.download_button(

        "download_report",
        "📄 Download PDF Report",
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