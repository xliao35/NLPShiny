from shiny import App, render, ui, reactive
project_info_sec = ui.tags.html(
    ui.div(class_ = 'projectinfosec', children=[
        ui.h5("Information On This Site"),
        ui.tags.ul(children=[
            ui.tags.li("Community Overview:", children=[
                ui.p("Providing basic summary and visualization about uploaded data")
            ]),
            ui.tags.li("Project Language:", children=[
                ui.p("Providing visualizations and narrative summaries of how different tokens evolves")
            ]),
            ui.tags.li("User Language:", children=[
                ui.p("Providing visualizations and narrative summaries of how individuals’ language evolves in the project.")
            ]),
        ]),
        ui.tags.hr()
    ]
    )  
)