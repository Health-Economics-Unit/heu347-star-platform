from shiny import ui
from modules.components import page_navigation

criteria_page = ui.div(

     ui.br(),
     ui.h1("📌 Criteria", class_="page-title"),
     ui.br(),
     ui.p(
         "Criteria are the measurable factors used to evaluate and compare options. "
         "They should reflect the objectives of the decision and capture all relevant "
         "aspects of value. For example, 'alleviating suffering' is an objective, "
         "while 'reducing disease severity' is a measurable criterion. When selecting "
         "criteria, aim for a concise set that covers the decision comprehensively, "
         "avoids duplication and double counting, and measures distinct aspects of "
         "performance. If your decision relates to resource allocation, costs should "
         "not be included as a criterion as they are considered separately within "
         "the prioritisation process."
     ),
    ui.h6(ui.strong("ℹ️ Note: The criteria below are examples only and are not exhaustive. "
                    "Please select or add criteria that are relevant to your decision"),
                    class_="note-text"),

    ui.br(),

    #----------------Suggested criteria--------------------------------------------------------------------

    ui.card(

        ui.card_header("Choose Criteria"),

        ui.layout_columns(

      ui.input_action_button(
                "add_health_benefit",
                "❤️ Health Benefits",
                class_="criterion-card"
            ),

            ui.input_action_button(
                "add_health_inequalities",
                "⚖️ Impact on Health Inequalities",
                class_="criterion-card"
            ),

            ui.input_action_button(
                "add_safety",
                "🛡️ Safety",
                class_="criterion-card"
            ),

            ui.input_action_button(
                "add_patient_experience",
                "😊 Patient Experience",
                class_="criterion-card"
            ),

            ui.output_ui("cost_criteria_button"),       #displayed only for mcda and not for star-mcda


            col_widths=(3, 3, 3, 3, 3)
        )
    ),


    #----------------Add custom criteria-----------------------------------------------------------

    ui.card(

        ui.card_header("Add Your Own Criterion"),

        ui.output_ui("star_criteria_note"),             #to display the star_cost note

        ui.layout_columns(

            ui.input_text(
                "custom_criteria",
                "Criteria name",
                placeholder = "For example: Quality of Care Delivery"
            ),

            ui.div(
                ui.input_action_button(
                    "add_custom_criteria",
                    "➕ Add Criteria",
                    class_="btn-primary w-100"
                ),

                style="""
                    display:flex;
                    align-items:flex-end;
                    height:100%;
                """
            ),

            col_widths=(9, 3)
        )
    ),


    #----------------Selected criteria --------------------------------------------------------------

    ui.card(

        ui.card_header("Selected Criteria"),

        ui.output_ui("criteria_table")
    ),

    #----------------Page navigation----------------------------------------------------

    page_navigation(
        previous_button_id="back_to_options",
        previous_label="Options page",
        save_button_id="save_criteria",
        continue_button_id="save_continue_criteria"
    )
)