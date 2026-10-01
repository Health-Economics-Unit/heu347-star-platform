# This page contains font style, dashboard css etc

from shiny import ui

#css style for card hover on the all pages
nav_card_style = ui.tags.style("""

.nav-card {
    position: relative;
    min-height: 140px;
    transition: all 0.25s ease;
    border: 1px solid #EAEBEB;
    border-radius: 12px;
}

.nav-card:hover {
    transform: translateY(-5px);
    box-shadow: 0px 8px 20px rgba(0,0,0,0.15);
    border-color: #4085C4;
    background-color: #F4F8FC;
}

.nav-card:active {
    transform: translateY(-2px);
    box-shadow: 0px 4px 10px rgba(0,0,0,0.20);
    background-color: #E8F2FC;
}

""")

