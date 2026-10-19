#This page will collect score inputs

from shiny import ui
from modules.components import page_navigation

scores_page = ui.div(
    ui.br(),
    ui.h1("Scores", class_="page-title"),
    ui.br(),
     ui.p(
          "Score each option against each criterion using a scale from "
          "0 (least preferred) to 100 (most preferred). Where quantitative evidence "
          "is available, values can be rescaled onto a 0–100 scale. Where "
          "evidence is unavailable, scores can be based on expert judgement."
     ),

     ui.p(
          "When using quantitative data, rescale values onto a 0–100 scale. "
          "For example, if three options affect 100, 200 and 300 people "
          "respectively, they could be scored 0, 50 and 100."
     ),

     ui.p(
          "For each criterion, identify the least preferred option (0) and "
          "the most preferred option (100), then score all other options "
          "relative to these anchor points."
     ),

     ui.strong(
          "ℹ️ Note: The scoring matrix is generated automatically from the "
          "Options and Criteria pages. The matrix will only appear once "
          "at least one option and one criterion have been added.",
        class_="page-title"
     ),

    #------scores matrix-----------------------------------------------------------------------

    ui.br(),
    ui.br(),
    ui.output_ui("scores_matrix"),
    ui.br(),

    #------page navigation----------------------------------------------------------------------

    page_navigation(
        previous_button_id="back_to_weighting",
        previous_label="Weighting page",
        save_button_id="save_scores",
        continue_button_id="save_continue_scores"
    )
)