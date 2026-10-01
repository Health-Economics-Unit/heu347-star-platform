#This page contains reusable UI components

from shiny import ui
from core.constants import app_name, app_subtitle, app_footername

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

        ui.h1(ui.strong(app_name)),
        ui.h5(app_subtitle),

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

#-------------------------reusable application footer-----------------------------------------------

def app_footer():

    return ui.div(

        app_footername,

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