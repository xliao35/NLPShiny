from shiny import App, render, ui, reactive
project_instruction = ui.div(class_ = "projectinst", children = [
    ui.h5("Some Instructions"),
    ui.div(class_ = "dataformat", children = [
        ui.h6("Data formats and example"),
        ui.tags.table(class_ = "table", children=[
            ui.tags.tr(children=[
                ui.tags.th("username"),
                ui.tags.th("user_join_date"),
                ui.tags.th("comment_body"),
                ui.tags.th("comment_created_at"),
            ]),
            ui.tags.tr(children=[
                ui.tags.td("12345"),
                ui.tags.td("2023-05-03T16:00:00.000Z"),
                ui.tags.td("This is an example comment"),
                ui.tags.td("2023-05-05T16:00:00.000Z"),
            ]),
        ]),
        ui.img(class_='image', src = 'sample_data.png', alt='sample image', width='35%')
    ]),
    ui.br(),
    ui.h6("Text mining/Preprocessing options"),
    ui.tags.ul(children=[
            ui.tags.li("Choice of Removing stop words:", children=[
                ui.p("Removing stop words can help model focus on the root words, but it may be problematic if the sentence is affected. ")
            ]),
            ui.tags.li("Choice of Text transformation:", children=[
                ui.p("Stemming is a fast process but it will not reduce each word to their proper base form like lemmatization. However lemmatization is context dependent.")
            ]),
            ui.tags.li("Choice of number removing:", children=[
                ui.p("Removing numbers reduce some distractions, but may lead to some loss of information. ")
            ]),
        ]),
    ui.h6("Date Ranges"),
    ui.tags.hr()
])