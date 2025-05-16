from dash.dependencies import Input, Output, State
import dash
import sys
import os
from dash import html

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ui.ui import app 
@app.callback(
    Output("chat-history", "children"),
    Output("chat-store", "data"),
    Output("query", "value"),
    [Input("submit", "n_clicks"), Input("query", "n_submit")],
    State("query", "value"),
    State("chat-store", "data"),
    prevent_initial_call=True
)
def update_chat(n_clicks, n_submit, query, chat_history):
    if not query:
        return dash.no_update, dash.no_update, ""

    llm_response = "This is a dummy response from the assistant."

    chat_history.append({"role": "user", "text": query})
    chat_history.append({"role": "assistant", "text": llm_response})

    chat_bubbles = []
    for msg in chat_history:
        bubble_style = {
            "user": {
                "backgroundColor": "#DCF8C6",
                "marginLeft": "auto", "marginRight": "10px",
            },
            "assistant": {
                "backgroundColor": "#E4E6EB",
                "marginRight": "auto", "marginLeft": "10px",
            }
        }[msg["role"]]
        chat_bubbles.append(html.P(msg["text"], style={
            **bubble_style,
            "padding": "10px",
            "borderRadius": "10px",
            "maxWidth": "70%",
            "marginTop": "5px"
        }))

    return chat_bubbles, chat_history, "" 

@app.callback(
    Output('upload-box-content', 'children'),
    Input('upload-data', 'filename'),
    prevent_initial_call=True
)
def update_uploaded_files(filenames):
    if not filenames:
        return [
            html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ], style={"marginBottom": "10px"})
        ]

    file_display = [html.Div(f"📄 {name}", style={
        "textAlign": "left",
        "padding": "5px 0",
        "fontSize": "16px",
        "color": "#333"
    }) for name in filenames]

    return [
        html.Div([
            'Uploaded Files:',
        ], style={"fontWeight": "bold", "marginBottom": "10px"}) 
    ] + file_display

app.run()