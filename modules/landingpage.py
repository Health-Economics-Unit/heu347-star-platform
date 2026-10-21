from shiny import ui
from modules.components import nav_card
from config.active_project import introduction_title, introduction_text, how_to_title, how_to_text, example_title, note_text
from config.active_project import navigation_cards


landing_page = ui.div(

#------Introduction---------------------------------------------------------------------------------------------------------

ui.card(

    ui.h5(
        ui.strong(introduction_title),
        class_="section-heading"
    ),

    ui.p(
        introduction_text,
        style="text-align:justify;"
    ),

    #class_="info-card"

#------How to use the application-------------------------------------------------------------------------------------------

    ui.h5(
        ui.strong(how_to_title),
        class_="section-heading"
    ),

    ui.p(
        how_to_text,
        style="text-align:justify;"
    ),

    class_="info-card"

),


#------Placeholder for visual-----------------------------------------------------------------------------------------------

    # ui.card(
    #     ui.h5(example_title)
    # ),

#------Note-----------------------------------------------------------------------------------------------------------------

    ui.h6(ui.strong(note_text), class_="note-text"),

ui.br(),

#------Navigation cards layout---------------------------------------------------------------------------------------------------------

    ui.layout_columns(
        *[
            nav_card( item["id"], item["title"], item["description"])
            for item in navigation_cards
        ]
    ),
)