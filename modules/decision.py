from shiny import ui
from modules.components import decision_card, page_navigation

decision_page = ui.div(

     ui.h2("🎯 Decision", class_="page-title"),
     ui.br(),
     ui.p(
          "Define the decision context before building your prioritisation model. Consider the problem you are trying to address, "
          "the outcomes you hope to achieve, the population or services affected, and the stakeholders who should be involved "
          "in the decision-making process. Different types of decisions "
          "require different evidence, criteria, and stakeholder input. Select the decision type that best "
          "reflects your scenario from the options below. If none are suitable, select 'Other'. "
          "The categories are based on common applications of MCDA reported in the literature "
          "(Gongora-Salazar et al., 2023).",

    #class_="page-title"
     ),

#-------------------Decision overview---------------------------------------------------------

    ui.card(

        ui.card_header("1. Decision Context"),

        ui.layout_columns(

            ui.input_text_area(
                "decision_title",
                "Decision title ",
                rows=6,
                placeholder="Enter decision title"
            ),

            ui.input_text_area(
                "decision_description",
                "Decision description/objectives *",
                rows=6,
                placeholder=(
                    "Describe the decision to be made, its objectives, and the patient population who will receive or be affected by the interventions being considered. "
                    "For example, deciding how to allocate resources across interventions for people with diabetes."
                )

            ),

            col_widths=(3, 9),
            #class_="card-header"       #to make the title and description heading green
        ),

        class_="page-card"
    ),


#----------------------Decision type---------------------------------------------------------


    ui.card(
        ui.card_header("2. Decision type"),

        ui.p(
            "Select the option that best describes the decision type. "
            "Only one decision type can be selected."
        ),

        ui.layout_columns(

          decision_card(
                "star_mcda",
                "⭐ STAR - MCDA",
                "Structured prioritisation combining STAR and MCDA to compare options, "
                "assess trade-offs and support transparent resource allocation decisions."
            ),

            decision_card(
                "mcda",
                "📊 MCDA",
                "Multi-Criteria Decision Analysis for evaluating and "
                "ranking options against weighted criteria to support evidence-based decision making."
            )

        ),

        ui.output_ui("selected_decision_type"),

        class_="page-card"
    ),

#----------------------Decision page navigation---------------------------------------------------------

    page_navigation(
        save_button_id="save_decision",
        download_button_id="download_project_decision",
        continue_button_id="save_continue_decision"
    )
)