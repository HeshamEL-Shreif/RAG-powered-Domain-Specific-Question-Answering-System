from dash.dependencies import Input, Output, State
import dash
import dash_bootstrap_components as dbc
from dash import html
from ui.ui import interface 
from logger.logging_config import setup_logger
import os
import base64
from app.data_handeler import load_documents
from app.rag_pipeline import initiate_models, get_pipeline
from app.response import get_response


UPLOAD_DIRECTORY = "data/upload"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)
logger = setup_logger(name="main logger", level="DEBUG", log_file="./logs/app.log")

def main():
    
    embedding, chat, memory, qa_prompt = initiate_models()
    qa_chain = get_pipeline(
        chat=chat,
        memory=memory,
        qa_prompt=qa_prompt,
        embeddings=embedding
    )
    
    
    app = interface()
    

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
        

        # llm_response = get_response(query, qa_chain)
        llm_response = 'dummy'
        
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
        [Output('upload-box-content', 'children'),
        Output("uploaded-files-list", "children")], 
        [Input('upload-data', 'contents'),
        Input("clear", "n_clicks")],
        [State('upload-data', 'filename')]
    )
    def handle_upload_and_clear(contents, clear_clicks, filenames):
        triggered_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
        saved_files = []
        global qa_chain 
        
        if triggered_id == "clear":
            if os.path.exists(UPLOAD_DIRECTORY):
                for file in os.listdir(UPLOAD_DIRECTORY):
                    os.remove(os.path.join(UPLOAD_DIRECTORY, file))
                logger.info("Cleared uploaded files")

        if contents and filenames and triggered_id == "upload-data":
            for content, filename in zip(contents, filenames):
                try:
                    saved_files.append(html.Div(f"✅ Saved: {filename}", style={
                        "textAlign": "left",
                        "padding": "5px 0",
                        "fontSize": "16px",
                          "color": "#155724"
                       }))
                    if filename.endswith(('.csv', '.txt', '.pdf', '.docx')):
                        _, content_string = content.split(',')
                        decoded = base64.b64decode(content_string)
                        with open(os.path.join(UPLOAD_DIRECTORY, filename), "wb") as f:
                            f.write(decoded)
                        
                        load_documents(os.path.join(UPLOAD_DIRECTORY, filename), embedding)
                        logger.info(f"File saved: {filename}")
                    else:
                        logger.warning(f"Unsupported file type: {filename}")
                        saved_files.append(html.Div(f"❌ Unsupported file type: {filename}", style={
                        "color": "red"
                          }))
                except Exception as e:
                    logger.error(f"Failed to save file {filename}: {e}")
            
            qa_chain = get_pipeline(
                chat=chat,
                memory=memory,
                qa_prompt=qa_prompt,
                embeddings=embedding
            )

        files = os.listdir(UPLOAD_DIRECTORY) if os.path.exists(UPLOAD_DIRECTORY) else []
        file_list_ui = [dbc.ListGroupItem(file) for file in files]

        upload_box = html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ] + saved_files, style={"marginBottom": "10px"})  

        return upload_box, file_list_ui

    app.run()
    
    
if __name__ == "__main__":
    main()
    
    
