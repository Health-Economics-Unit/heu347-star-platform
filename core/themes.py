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