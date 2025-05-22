from dash.dependencies import Input, Output, State
import dash
import dash_bootstrap_components as dbc
from dash import html
from ui.ui import interface 
from logger.logging_config import setup_logger
import os
import base64

UPLOAD_DIRECTORY = "data/upload"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

def main():
    logger = setup_logger(name="main logger", level="DEBUG", log_file="./logs/app.log")
    app = interface()
    all_files = []
    

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
        logger.info("User sent a query")
        

        llm_response = "This is a dummy response from the assistant."
        
        logger.info("LLM responsed")
        
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
        [Output('upload-box-content', 'children'),  Output("uploaded-files-list", "children")], 
        [Input('upload-data', 'contents'),  Input("upload", "n_clicks")],
        State('upload-data', 'filename'))
    def update_drop_box_upload_files(contents, n_clicks, filenames):
        saved_files = []

        if not n_clicks:
            if contents is None or filenames is None: 
                return [html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ], style={"marginBottom": "10px"})] + saved_files, [dbc.ListGroupItem("No files Yet")]
            for filename in filenames:
                saved_files.append(html.Div(f"{filename}"))
            return [html.Div('Selected Files:', style={"fontWeight": "bold", "marginBottom": "10px"})] + saved_files, [dbc.ListGroupItem("No files Yet")]
            
            
        if n_clicks:
            if contents is None or filenames is None:
                return [html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ], style={"marginBottom": "10px"})], [dbc.ListGroupItem("No files Yet")]
                
            for content, filename in zip(contents, filenames):
                try:
                    content_type, content_string = content.split(',')
                    decoded = base64.b64decode(content_string)

                    file_path = os.path.join(UPLOAD_DIRECTORY, filename)
                    with open(file_path, "wb") as f:
                        f.write(decoded)

                    saved_files.append(html.Div(f"✅ Saved: {filename}", style={
                        "textAlign": "left",
                        "padding": "5px 0",
                        "fontSize": "16px",
                        "color": "#155724"
                    }))
                    logger.info(f"File saved: {file_path}")
                except Exception as e:
                    logger.error(f"Failed to save file {filename}: {e}")
                    saved_files.append(html.Div(f"❌ Failed: {filename}", style={
                        "color": "red"
                    }))
            all_files.extend(filenames)
            saved_files = []
            return [html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ], style={"marginBottom": "10px"})] + saved_files, [dbc.ListGroupItem(file) for file in all_files]    
        

    app.run()
    
    
if __name__ == "__main__":
    main()