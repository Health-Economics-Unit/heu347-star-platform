from shiny import ui
from modules.components import decision_card, page_navigation

decision_page = ui.div(

     ui.h2("🎯 Decision"),
     ui.br(),
     ui.p(
          "Define the decision context before building your prioritisation model. Consider the problem you are trying to address, "
          "the outcomes you hope to achieve, the population or services affected, and the stakeholders who should be involved "
          "in the decision-making process. Different types of decisions "
          "require different evidence, criteria, and stakeholder input. Select the decision type that best "
          "reflects your scenario from the options below. If none are suitable, select 'Other'. "
          "The categories are based on common applications of MCDA reported in the literature "
          "(Gongora-Salazar et al., 2023)."
     ),

#-------------------Decision overview---------------------------------------------------------

    ui.card(

        ui.card_header("1. Decision Context"),

        ui.layout_columns(

            ui.input_text_area(
                "decision_title",
                "Decision title ",
                rows=6,
                placeholder="Cancer Service Prioritisation 2027/28"
            ),

            ui.input_text_area(
                "decision_description",
                "Decision description/objectives *",
                rows=6,
                placeholder=(
                    "Provide a brief description of the decision "
                    "that needs to be made."
                )
            ),

            col_widths=(3, 9)
        )
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
                "resource_allocation",
                "💰 Resource Allocation",
                "Allocate resources across options within a fixed budget."
            ),

            decision_card(
                "priority_setting",
                "⚖️ Priority Setting",
                "Rank options based on value and impact."
            ),

        #     decision_card(
        #         "clinical_decision_making",
        #         "🩺 Clinical Decision Making",
        #         "Compare clinical options and support treatment or care pathway decisions."
        #     ),
        #
        #
            decision_card(
                "other_decision",
                "🧩 Other",
                "Define a custom decision context.",
            )
        ),

        ui.output_ui("selected_decision_type"),
    ),

    ui.br(),

#----------------------Decision page navigation---------------------------------------------------------

    page_navigation(
        save_button_id="save_decision",
        continue_button_id="save_continue_decision"
    )
)