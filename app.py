from shiny import App, render, ui, reactive
import utils
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys
from components import ProjectOverview
import jinja2

sys.path.insert(0, 'components')

df = pd.DataFrame()
header_ui = ui.div(class_ = "projectdesc", children = [
                        ui.h6("In this project, we review, detect, and summarize the change in users' language patterns from comments"),
                        ui.h6("By analyzing those comments with NLP methodologies, we aim to define a common trend of word usage when expressing a similar idea in the community")
                    ])

app_ui_copy = ui.tags.html(
    ui.tags.head(
        ui.tags.link(rel="stylesheet", href="styles.css")
    ),

    ui.div(class_="container", children=[
        ui.div(class_ = "headbar", children=[
            ui.h4("Social Ontology App"),
            ui.div(class_="header", children=[
                ui.a("About", href = "about.html"),
                ui.a("Information", href = "info.html"),
                ui.a("Survey", href = "survey.html")
            ]),
        ]),

        ui.div(class_ = 'pageContainer', children=[
            ui.div(class_="mainPage", children=[
                ui.div(class_="sidebar", children=[
                    ui.div(class_ = "fileChooser", children = [
                        ui.input_file(
                            "file1",
                            "Choose CSV",
                            multiple=False,
                            accept=["text/csv", "text/comma-separated-values,text/plain", ".csv"],
                        ),
                        ui.input_radio_buttons(
                        "inRadioButtons1", "Choose Methods", ["Stemming", "Lemmatization"]
                        ),
                        ui.input_radio_buttons(
                        "inRadioButtons2", "Stopwords", ["Remove", "Keep"]
                        ),
                        ui.input_radio_buttons(
                        "inRadioButtons3", "Digitals", ["Remove", "Keep"]
                        ),
                    ]),
                ])
            ])
        ])
    ])
)

app_ui = ui.page_fluid(
    ui.tags.head(
        ui.tags.link(rel="stylesheet", href="styles.css")
    ),

    ui.div(class_="container", children=[
        ui.div(class_ = "headbar", children=[
            ui.h4("Social Ontology App"),
            ui.div(class_="header", children=[
                ui.a("About", href = "about.html"),
                ui.a("Information", href = "info.html"),
                ui.a("Survey", href = "survey.html")
            ]),
        ]),

        ui.div(class_ = 'pageContainer', children=[
            ui.div(class_="mainPage", children=[
                ui.div(class_="sidebar", children=[
                    ui.div(class_ = "fileChooser", children = [
                        ui.input_file(
                            "file1",
                            "Choose CSV",
                            multiple=False,
                            accept=["text/csv", "text/comma-separated-values,text/plain", ".csv"],
                        ),
                        ui.input_radio_buttons(
                        "inRadioButtons1", "Choose Methods", ["Stemming", "Lemmatization"]
                        ),
                        ui.input_radio_buttons(
                        "inRadioButtons2", "Stopwords", ["Remove", "Keep"]
                        ),
                        ui.input_radio_buttons(
                        "inRadioButtons3", "Digitals", ["Remove", "Keep"]
                        ),
                    ]),
                ])
            ]),

            ui.div(class_ = "dashboard", children=[
                ui.navset_tab(
                    ui.nav("Project Description",
                        ProjectOverview.project_over_view_screen
                    ),
                    ui.nav("Community Overview",
                        ui.br(),
                        ui.output_text("tab1_summary"),
                        ui.output_plot("tab1_plot")
                    ),
                    ui.nav("Project Language",
                        ui.div(class_="tab2", children=[
                            ui.div(class_="tableContainer", children = [
                                ui.br(),
                                ui.output_table("tab2_table"),
                            ]),
                            ui.div(class_="bottom_menu", children=[
                                ui.input_checkbox_group("bottom1", "Further Analysis Options", ["Token Evolution", "Emergent Token Relationships", "Language Similarity", "Topic Modeling"], inline=True, width='100%'),
                            ])
                        ])
                        # ui.div(class_="tableContainer", children = [
                        #     ui.br(),
                        #     ui.output_table("tab2_table"),
                        #     ui.div(class_="bottom_menu", children=[
                        #         ui.input_radio_buttons("bottom1", "Token Evolution", choices=["Yes", "No"]),
                        #         ui.input_radio_buttons("bottom1", "Emergent Token Relationships", choices=["Yes", "No"]),
                        #         ui.input_radio_buttons("bottom1", "Language Similarity", choices=["Yes", "No"]),
                        #         ui.input_radio_buttons("bottom1", "Topic Modeling", choices=["Yes", "No"])
                        #     ])
                        # ]
                        
                        # ui.output_plot("tab1_plot")
                    ),
                    ui.nav("User Language",
                        ui.br(),
                        # ui.output_text("tab1_summary"),
                        # ui.output_plot("tab1_plot")
                    ),
                )
            ])
        ])
    ])
)

def retrieve_df(input):
    if input.file1() is None:
        return "Please upload a csv file, with 'username', 'comment_body', 'comment_created_at'"
    file_path = input.file1()[0]["datapath"]
    df = pd.read_csv(file_path).head(1000)
    if not utils.checkInput(df):
        return "Wrong Column Pattern\n Desired format is: username, user_join_date,comment_body, comment_created_at"
    return df

def server(input, output, session):
    @output
    @render.text
    def tab1_summary():
        try:
            df = retrieve_df(input)
            if type(df) != str:
            # print(input.inRadioButtons2())
                df = utils.transform(df, input.inRadioButtons1(), input.inRadioButtons2(), input.inRadioButtons3())

                summary = utils.summary(df)
                return summary
            else:
                return df
        except Exception:
            return "Loading the dataset. Please Hang On!"
        # return ui.HTML(df.to_html(classes="table table-striped"))
        

    @output
    @render.plot
    def tab1_plot():
        try:
            df = retrieve_df(input)
            
            df = utils.transform(df, input.inRadioButtons1(), input.inRadioButtons2(), input.inRadioButtons3())
            community_dict = {}
            df = df.fillna('')

            utils.generate_dict(df, community_dict)
            df_community = pd.DataFrame(community_dict) 
                # return ui.HTML(df.to_html(classes="table table-striped"))

            week_samples = list(community_dict.keys())
            token_nums = []
            new_user_nums = []
            comment_nums = []

            for key in community_dict.keys():
                token_nums.append(community_dict.get(key)['tokens_num'])
                new_user_nums.append(community_dict.get(key)['new_users'])
                comment_nums.append(community_dict.get(key)['comments_num'])

            fig, (ax1, ax2, ax3) = plt.subplots(3, sharex=True)
            ax1.plot(week_samples, token_nums, 'tab:orange')
            ax1.set_title('Token Trend')
            ax2.plot(week_samples, new_user_nums, 'tab:green')
            ax2.set_title('User Trend')
            ax3.plot(week_samples, comment_nums, 'tab:red')
            ax3.set_title('Comment Trend')
            plt.tight_layout()
            # plt.plot(week_samples, token_nums, label='Token Trend')
            # plt.plot(week_samples, new_user_nums, label='User Trend')
            # plt.plot(week_samples, comment_nums, label='Comment Trend')
        except:
            return None

    @output
    @render.text
    def tab2_table():
        df = retrieve_df(input)  
        transformed = utils.transform(df, input.inRadioButtons1(), input.inRadioButtons2(), input.inRadioButtons3())
        df_evolve = utils.get_token_evolve('week', transformed)
        return ui.HTML(df_evolve.to_html(classes="table table-striped"))

www_dir = Path(__file__).parent / "www"
print(www_dir)
# app = App(ui=app_ui, server=server, static_assets=www_dir)
app = App(app_ui, server=server, static_assets=www_dir)
