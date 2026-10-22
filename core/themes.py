#This page controls the theme button in header

#--------light theme------------------------------------------------------------------------

light_theme = """

.page-header {
    display:flex;
    justify-content:space-between;
    align-items:center;
    width:100%;
    margin-bottom:20px;
    padding-bottom: 10px;
    border-bottom: 1px solid #EAEBEB;
}

body {
    background-color: #F7F9FB;
    /* background-color: #FFFFFF;                    too white*/
    color: #000000;
}

.card {
    background-color: #F7F9FB;
    color: #000000;
}
"""

#--------dark theme------------------------------------------------------------------------

dark_theme = """

body.dark-mode {
    background-color: #1B2430;
    color: #F7F9FB;
}

body.dark-mode .page-header {
    display:flex;
    justify-content:space-between;
    align-items:center;
    width:100%;
    margin-bottom:20px;
    border-bottom: 1px solid #445069;
    padding-bottom: 10px;
}

body.dark-mode .btn-primary {
    color: #F7F9FB !important;
}

body.dark-mode .card {
    background-color: #27374D;
    color: #F7F9FB;
    border-color: #445069;
}

body.dark-mode .nav-card:hover {
    background-color: #34495E;
    border-color: #59C0E9;
}
"""

#-----------------------------------------------------------------------------------------
#----------Color palette/theme for each project-------------------------------------------

def project_theme_css(palette):

    return f"""
    
/* --------------------Page--------------------------------------------- */

    body,
    button,
    input,
    textarea,
    select,
    .card,
    .card-header {{

        background-color: {palette["background"]};
        font-family: Arial, sans-serif;
        color: #212529;
        text-align: justify;
    }}
    
    .body-text {{

        color: {palette["text"]};
        font-size: 1rem;
        line-height: 1.6;
        text-align: justify;
    }}

/*-------------------Banner used for project name + project subtitle + logo--------------------------------*/
    
    .project-banner {{

        background-color: {palette["primary"]};
        position: relative;
        min-height: 360px;
        padding: 60px 80px;
        margin-top: 20px;
        margin-bottom: 40px;
        border: none;
        border-radius: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.10);
        overflow: hidden;
        text-align: center;

    }}
    
    .project-banner img {{
        position: absolute;
        top: 25px;
        left: 35px;
        height: 120px;
        width: auto;
    }}

    .project-title {{
    
        color: {palette["white"]};
        font-size: 3.5rem;
        font-weight: 500;
        margin-bottom: 15px;
        padding-top: 15px;
    }}

    .project-subtitle {{
    
        color: {palette["white"]};
        font-weight: 500;
        margin-top: 15px;
        margin-bottom: 0;
    }}
    
/*-------------------section heading used for introduction + how to use this app--------------------------------*/
    
    .section-heading {{
    
        color: {palette["primary"]};
        font-weight: 700;
        margin-bottom: 10px;

    }}
    
/*-------------------note text on each page----------------------------------------------------------------------*/
    
    .note-text {{

        color: {palette["primary"]};
        font-weight: 500;
    }}

/*-------------project-card used for navigation cards + Decision cards-------------------------------------------*/
    
    .project-card {{
    
        position: relative;
        background-color: {palette["white"]};
        border: 2px solid {palette["border"]};
        border-radius: 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        transition: all 0.2s ease;
        cursor: pointer;
        margin-bottom: 20px;
        min-height: 180px;
        padding: 20px;
    }}
    
    .card-title {{
    
        color: {palette["primary"]};
        font-weight: 600;
    }}
    
    .card-description {{
    
        color: {palette["text"]};
    }}
    
    
/*-----Info card manages the information card on the landing page-----------------------*/
    
    .info-card {{
    
        background-color: {palette["white"]};
        border: 2px solid {palette["border"]};
        border-radius: 20px;
        color: {palette["text"]};
        font-size: 1rem;
        line-height: 1.6;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        margin-bottom: 20px;
        padding: 20px;
    }}
    
/*---------------Hover effect for all pages &-----------------------------------------------------------------------
----------Theme for all other pages except the landing page(it has its own theme on top)------------------------*/
    
    .page-title {{
    
        color: {palette["primary"]};
        font-weight: 700;
    }}
    
    .card-header {{
    
        color: {palette["primary"]};
        font-weight: 600;
        background-color: {palette["white"]};
        border-bottom: 1px solid {palette["border"]};
    }}
    
    .page-card {{
    
        background-color: {palette["white"]};
        border: 2px solid {palette["border"]};
        border-radius: 20px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
        padding: 20px;
        margin-bottom: 20px;
    }}
    
    .project-card:hover,
    .criterion-card:hover {{
    
        background-color: {palette["background"]};
        border-color: {palette["primary"]} !important;
        color: {palette["primary"]} !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}
    
/*----------------Criteria Cards----------------------------------------------------------------------------*/
    
    .criterion-card {{
    
        background-color: {palette["white"]};
        border: 2px solid {palette["border"]};
        border-radius: 15px;
        color: {palette["primary"]};
        font-weight: 600;
        transition: all 0.2s ease;
    }}
    
    .criterion-card.btn,
    .criterion-card.btn:visited {{

    background-color: {palette["white"]} !important;
    color: {palette["primary"]} !important;
    border-color: {palette["border"]} !important;
    }}

    .criterion-card.btn:hover,
    .criterion-card.btn:focus,
    .criterion-card.btn:active {{
    
        background-color: {palette["background"]} !important;
        color: {palette["primary"]} !important;
        border-color: {palette["primary"]} !important;
    
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}
    
/*--------------------Buttons----------------------------------------------------------------------------------------------*/
    
    .btn-primary {{
    
        background-color: {palette["primary"]};
        border-color: {palette["primary"]};
        color: {palette["white"]};
    }}
    
    .btn-primary:hover {{
    
        background-color: #2A8B77;
        border-color: #2A8B77;
    }}
    
    .download-button {{
    
        background-color: {palette["primary"]} !important;
        border-color: {palette["primary"]} !important;
        color: {palette["white"]} !important;
        width: auto !important;
        display: inline-block !important;
    }}
    
/*--------------------Results page navigation cards--------------------------------------------------------------------------------*/
    
    .results-nav-card {{
    
        background-color: {palette["white"]};
        border: 2px solid {palette["border"]};
        border-radius: 15px;
        padding: 25px;
        font-size: 0.95rem;
        text-align: center;
        width: 140px;
        min-height: 80px;
        color: {palette["primary"]};
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    
    .results-nav-card.btn,
    .results-nav-card.btn:visited {{
    
        background-color: {palette["white"]} !important;
        color: {palette["primary"]} !important;
        border-color: {palette["border"]} !important;
    }}
    
/*-----------------------------bootstrap override for results card------------------------------------------------------*/
    
    .results-nav-card.btn:hover,
    .results-nav-card.btn:focus,
    .results-nav-card.btn:active {{
    
        background-color: {palette["background"]} !important;
        color: {palette["primary"]} !important;
        border-color: {palette["primary"]} !important;
    
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}
    
    .results-nav-card .card-icon {{
    
        font-size: 1.4rem;
    }}
    
    """

    
