# This page contains fixed values for the HSE project like project details, landing page details, color palette, chart_colors, theme_css :

#---------------------------------------------------------------------------------------------------------------------
#----------------------Project specific branding-------------------------------------------------------------------------------

project_name = "The Health and Safety Executive's Prioritisation Platform"
#--------------------------------------------------------------------------------------------------
project_subtitle = "MCDA - Multi-Criteria Decision Analysis"
#--------------------------------------------------------------------------------------------------
project_footername = "The Health and Safety Executive (HSE)"
#--------------------------------------------------------------------------------------------------
project_logo = "hse_logo_white.png"


#---------------------------------------------------------------------------------------------------------------------
#------------------------Project specific landing page----------------------------------------------------------------

introduction_title = "Introduction"
#---------------------------------------------------------------------------------------------------------------------

introduction_text = (
            "This application is a decision-support tool that uses criteria to compare, score, "
            "and rank health interventions in a way that is transparent and guided by local stakeholders "
            "in order to prioritise interventions that are value-based and appropriate for the context "
            "within which they are implemented."
)
#--------------------------------------------------------------------------------------------------
how_to_title = "How to use this application"
#--------------------------------------------------------------------------------------------------
how_to_text = ("The Strategic Prioritisation Platform guides users through the "
               "six key stages of Multi-Criteria Decision Analysis (MCDA): "
               "Decision, Options, Criteria, Scores, Weighting, and Results. "
               "Complete each stage in the below sequence to build a transparent, "
               "evidence-based assessment and support robust healthcare decision making.")
#--------------------------------------------------------------------------------------------------------------------
example_title = "Placeholder: Example scenario that will load by default to help the users understand how it works"

#--------------------------------------------------------------------------------------------------------------------

note_text = ("ℹ️ Note: Complete the stages below in sequence, as each stage builds on the information "
             "collected in the previous step.")




#---------------------------------------------------------------------------------------------------------------------
#-------------------------Project specific pages----------------------------------------------------------------------

#---------------------Landing page----------------------------------------------------------------

navigation_cards = [

    {
        "id": "go_decision", "title": "🎯 Decision", "description": "Define objectives"
    },

    {
        "id": "go_options", "title": "📋 Options", "description": "Select interventions"
    },

    {
        "id": "go_criteria", "title": "📌 Criteria", "description": "Choose criteria"
    },

    {
        "id": "go_weighting", "title": "🎚️ Weighting", "description": "Assign weights"
    },

    {
        "id": "go_scores", "title": "📝 Scores", "description": "Score options"
    },

    {
        "id": "go_results", "title": "📊 Results", "description": "Review recommendations"
    }

]


#--------------------------------Project Aesthetics------------------------------------------------------------------
#------------------------Color palette-------------------------------------------------------------------------------

palette = {
    "primary": "#00685A",    #main hse teal - use for banner, navigation active state, primary buttons, cards and charts
    "secondary": "#89B4AE",  #sage green - use for landing page backgrounds, information cards etc
    "accent": "#BFD7D3",     #light teal for borders, hover etc
    "background": "#F3F5F4", #page background, info panels etc
    "border": "#C9DEDA",
    "text": "#234B4B",
    "white": "#FFFFFF"
}

chart_colours = [
    "#0D6B5A",
    "#2A8B77",
    "#5FA59B",
    "#89B4AE",
    "#BFD7D3"
]

#-------------------------Chart colors--------------------------------------------------------------------------------

chart_colours = [
    "#00685A",  # Primary HSE green
    "#2A8B77",
    "#5FA59B",
    "#89B4AE",
    "#BFD7D3"
]

#-------------------------HSE CSS theme-----------------------------------------------------------------------------------

theme_css = """

/* --------------------Page------------------------------- */

body,
button,
input,
textarea,
select,
.card,
.card-header {

    background-color: #F3F5F4;
    font-family: Arial, sans-serif;
    color: #00685A;
    text-align: justify;
}


/*-------------------Banner used for project name + project subtitle + logo--------------------------------*/

.project-banner {

    background-color: #00685A;
    border: none;
    border-radius: 0;
    box-shadow: none;
    min-height: 280px;
    padding: 40px 50px;
    position: relative;
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
}


.project-banner img {
    position: absolute;
    top: 25px;
    left: 35px;
    height: 110px;
    width: auto;
}

.project-title {

    color: #FFFFFF;
    font-weight: 700;
    margin: 0;
    padding-top: 15px;
}

.project-subtitle {

    color: #FFFFFF;
    font-weight: 500;
    margin-top: 15px;
    margin-bottom: 0;
}

/*-------------------section heading used for introduction + how to use this app--------------------------------*/

.section-heading {

    color: #0D6B5A;
    font-weight: 700;
    margin-bottom: 10px;
}

/*-------------project-card used for navigation cards + Decision cards-------------------------------------------*/

.project-card {

    position: relative;
    background-color: #FFFFFF;
    border: 2px solid #C9DEDA;
    border-radius: 20px;
    color: #00685A;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    transition: all 0.2s ease;
    cursor: pointer;
    margin-bottom: 20px;
    min-height: 180px;
    padding: 20px;
}

.project-card:hover {

    transform: translateY(-2px);
    border-color: #0D6B5A;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

/*-----Info card manages the information card on the landing page-------------*/

.info-card {

    background-color: #FFFFFF;
    border: 2px solid #C9DEDA;
    border-radius: 20px;
    color: #00685A;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    margin-bottom: 20px;
    padding: 20px;
}

/*---------------Theme for all other pages now except the landing page(it has its own theme on top)----------*/

.page-title {

    color: #00685A;
    font-weight: 700;
}

.card-header {

    color: #00685A;
    font-weight: 600;
    background-color: #FFFFFF;
}

.page-card {

    background-color: #FFFFFF;
    border: 2px solid #C9DEDA;
    border-radius: 20px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    padding: 20px;
    margin-bottom: 20px;
}

/*----------------Criteria Cards----------------------------------------------------------------------------*/

.criterion-card {

    background-color: #FFFFFF;
    border: 2px solid #C9DEDA;
    border-radius: 15px;
    color: #0D6B5A;
    font-weight: 600;
    transition: all 0.2s ease;
}

.criterion-card:hover {

    background-color: #F3F5F4;
    border-color: #0D6B5A;
}


/*--------------------Buttons--------------------------------------------------------------------------------*/

.btn-primary {

    background-color: #00685A;
    border-color: #00685A;
    color: #FFFFFF;
}

.btn-primary:hover {

    background-color: #2A8B77;
    border-color: #2A8B77;
}

.download-button {

    background-color: #0D6B5A !important;
    border-color: #0D6B5A !important;
    color: white !important;
    width: auto !important;
    display: inline-block !important;
}

"""
