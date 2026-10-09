#This page contains reusable UI components

from shiny import ui
#from core.constants import app_name, app_subtitle, app_footername
from config.active_project import project_name, project_subtitle, project_footername

#-------------------------reusable application header-----------------------------------------------

def page_header():

    return ui.div(

        ui.input_action_button("go_home","🏠 Home"),
        ui.output_ui("theme_button"),                   #the theme button logic is in app.py

        class_="page-header",
    )
#-------------------------reusable application title-----------------------------------------------

def app_banner():

    return ui.card(

        ui.h1(ui.strong(project_name)),
        ui.h5(project_subtitle),

        style="""
            margin-top:20px;
            padding:25px;
            text-align:center;
        """
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

            ui.h4(title), ui.p(description),

            class_="nav-card"

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

        class_="nav-card"
    )

#-------------------------page navigations save, previous and continue---------------------------------------------------

def page_navigation(
    save_button_id,
    continue_button_id,
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
                "💾 Save",
                class_="btn-outline-primary",
            ),

            ui.input_action_button(
                continue_button_id,
                "Save & Continue →",
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
#-------------------------reusable application footer-----------------------------------------------

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