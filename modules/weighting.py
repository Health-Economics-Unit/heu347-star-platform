#This page will collect weight inputs for each criteria

from shiny import ui
from modules.components import page_navigation

weighting_page = ui.div(
     ui.br(),
     ui.h1("Weighting", class_="page-title"),
     ui.br(),

     ui.p("Weighting involves determining the relative importance of each criterion compared with "
        "the other criteria, as well as the importance of the range from the most preferred and least preferred "
        "option for each criterion. This application uses swing weighting, a method widely used in MCDA for its simplicity and practicality. "
        "The approach involves comparing a swing from 0 to 100 on one criterion with a change from 0 to 100 on another criterion. "
        "The criterion for which a swing from 0 to 100 is considered most important is assigned a weight of 100. "
        "All other criteria are then assigned weights relative to this benchmark. "
        "These weights are subsequently normalised and expressed as percentages."),

     ui.p("Assign a weight between 0 and 100 to each criterion using swing weighting. "
        "Consider how important a change from the worst to the best possible performance would be for each "
        "criterion. Assign 100 to the criterion whose improvement matters most, then assign the remaining "
        "criteria values relative to it."
     ),

     ui.card(

        ui.card_header("Criterion Weights"),

        ui.p(
            "Use the slider or enter a value directly. "
            "Both controls will remain synchronised."
        ),

        ui.h6(ui.strong("ℹ️ Note: If all criteria are considered equally important, assign the same weight (i.e. 100) to each criteria."),
              class_="note-text"),

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
        download_button_id="download_project_weighting",
        continue_button_id="save_continue_weights"
     )
)