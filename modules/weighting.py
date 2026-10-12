#This page will collect weight inputs for each criteria

from shiny import ui
from modules.components import page_navigation

weighting_page = ui.div(
     ui.br(),
     ui.h1("Weighting"),
     ui.br(),
     ui.p(
        "Assign a weight between 0 and 100 to each criterion using "
        "swing weighting. Consider how important a change from the "
        "worst to the best possible performance would be for each "
        "criterion. Assign 100 to the criterion whose improvement "
        "matters most, then assign the remaining criteria values "
        "relative to it."
     ),

     ui.card(

        ui.card_header("Criterion Weights"),

        ui.p(
            "Use the slider or enter a value directly. "
            "Both controls will remain synchronised."
        ),

        ui.output_ui("weighting_controls")
     ),

     ui.card(

        ui.card_header("Weighting Summary"),

        ui.output_ui("weighting_summary")
     ),


     #----------------Page navigation----------------------------------------------------

     page_navigation(
        previous_button_id="back_to_criteria",
        previous_label="Criteria page",
        save_button_id="save_weights",
        continue_button_id="save_continue_weights"
     )
)