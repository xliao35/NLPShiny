from shiny import App, render, ui, reactive
project_header = ui.div(class_ = "projectdesc", children = [
    ui.br(),
    ui.p("In this project, we review, detect, and summarize the change in users' language patterns from comments"),
    ui.p("By analyzing those comments with NLP methodologies, we aim to define a common trend of word usage when expressing an idea in the community")
])