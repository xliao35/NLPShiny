from shiny import App, render, ui, reactive
import sys
from . import ProjectHeader, ProjectInfoSec, ProjectInstruction

project_over_view_screen = ui.tags.html(
    ui.div(class_ = "projScreen", children=[
        ProjectHeader.project_header,
        ProjectInfoSec.project_info_sec,
        ProjectInstruction.project_instruction
    ])
)