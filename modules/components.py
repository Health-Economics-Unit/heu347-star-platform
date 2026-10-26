#This page contains reusable UI components
# page header,
# app banner,
# def nav_card(...)
# def decision_card(...)
# def page_navigation(save + save&continue + previous)
# app footer,


from shiny import ui
from config.active_project import project_name, project_subtitle, project_footername, project_logo

CARD_CLASS = "project-card"

#------------------------------------------------------------------------------------------------

#-------------------------reusable application header-----------------------------------------------

def page_header():

    return ui.div(

        ui.input_action_button(
            "go_home",
            "🏠 Home",
            class_ = "header-button"
        ),

        ui.div(

            ui.output_ui(
                "header_load_project",
                class_="header-button"
            ),

            ui.output_ui(
                "theme_button",
                class_="header-button"
            ),

            style="""
                display:flex;
                align-items:center;
                gap:10px;
            """
        ),

        class_="page-header",
    )

#-------------------------reusable application title-----------------------------------------------

def app_banner():

    return ui.card(

        ui.img(
            src=project_logo,
            class_="banner-logo"
        ),

        ui.h1(
            ui.strong(project_name),
            class_="project-title"
        ),

        ui.h3(
            project_subtitle,
            class_="project-subtitle"
        ),

        class_="project-banner"

    )
#-------------------------reusable navigation cards for landing page--------------------------------

def nav_card(button_id, title, description):
    return ui.card(
        ui.input_action_button(
                button_id,
                "",
                style="""
                    position:absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    opacity: 0;
                    cursor: pointer;
                    z-index: 10;
                """
            ),

            ui.h4(title, class_="card-title"), ui.p(description, class_="card-description"),

            class_= CARD_CLASS

        )
#-------------------------reusable cards for decision page-----------------------------------------

def decision_card(button_id, title, description):

    return ui.card(

        ui.input_action_button(
            button_id,
            "",
            style="""
                position:absolute;
                top:0;
                left:0;
                width:100%;
                height:100%;
                opacity:0;
                cursor:pointer;
                z-index:10;
            """
        ),

        ui.h4(title), ui.p(description),

        class_= CARD_CLASS
    )

#-------------------------page navigations save, previous and continue---------------------------------------------------

def page_navigation(
    save_button_id,
    continue_button_id,
    download_button_id,
    previous_button_id=None,
    previous_label=None
):

    left_section = []

    if previous_button_id:

        left_section.append(
            ui.input_action_button(
                previous_button_id,
                f"← {previous_label}"
            )
        )

    return ui.div(

        ui.div(
            *left_section
        ),

        ui.div(

            ui.input_action_button(
                save_button_id,
                "💾 Save",                       #save button
                class_="btn-outline-primary",
            ),

            ui.download_button(
                download_button_id,
                "📥 Export Project",
                class_ = "btn-outline-primary"
            ),


            ui.input_action_button(
                continue_button_id,
                "Save & Continue →",            #save & continue button
                class_="btn-primary",
            ),

            style="""
                display:flex;
                gap:10px;
            """
        ),

        style="""
            display:flex;
            justify-content:space-between;
            align-items:center;
            margin-top:20px;
            margin-bottom:20px;
        """
    )
#-------------------------reusable cards for results page-----------------------------------------------

def results_nav_card(card_id, icon, title):

    return ui.input_action_button(

        card_id,

        ui.div(

            ui.div(
                icon,
                style="font-size:2rem;"
            ),

            ui.p(
                title,
                style="""
                    margin-top:10px;
                    font-weight:600;
                """
            ),

        ),

        class_="results-nav-card"
    )

#-------------------------reusable application footer---------------------------------------------------

def app_footer():

    return ui.div(

        project_footername,

        style="""
            margin-top:auto;
            border-top:1px solid #EAEBEB;
            text-align:center;
            font-size:0.9rem;
            font-weight:500;
            color:#666666;
            padding:8px;
        """
    )