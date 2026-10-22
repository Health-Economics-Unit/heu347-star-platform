#This page will collect score inputs

from shiny import ui
from modules.components import page_navigation

star_cost_page = ui.div(
    ui.br(),

    ui.h1("💷 Costs", class_="page-title"),
    ui.br(),
    ui.p(
          "Enter the estimated cost per person and the number of people "
          "receiving each intervention. The total cost for each "
          "option will be calculated automatically."
    ),

    #------scores matrix-----------------------------------------------------------------------

    ui.br(),
    ui.card(

            ui.card_header("Option Costs"),

            ui.output_ui("cost_matrix"),

            class_="page-card"
        ),

    ui.br(),

    #------page navigation----------------------------------------------------------------------

    page_navigation(
        previous_button_id="back_to_weighting_from_cost",
        previous_label="Weighting page",
        save_button_id="save_costs",
        continue_button_id="save_continue_costs"
    )
)