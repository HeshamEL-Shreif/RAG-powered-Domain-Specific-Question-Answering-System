from dash import dcc, html, Dash
import dash_bootstrap_components as dbc
from logger.logging_config import setup_logger



def interface():
    logger = setup_logger(name="ui_logger", level="DEBUG", log_file="./logs/app.log")
    app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.title = "Question Answering System"
    logger.info("Initializing the UI")


    header = html.H1(["Question Answering System"], style={"textAlign": "center",
                                                            "color": "white",
                                                            "fontSize": 35,
                                                            "backgroundColor": "#1F456E",
                                                            "padding": "45px",
                                                            "text-shadow": "2px 2px 2px #000000",
                                                            "font-family": "serif"})
    response_title = dbc.Col([html.H4(["Response"], style={"textAlign": "center", "margin":"10px"})], width=9)

    submit_button = dbc.Button("Submit", style={"backgroundColor": "#2832C2",
                                                "margin": "20px 0px 5px 0px",})
    card = dbc.Card([
        dbc.CardBody([
            html.Div(
                id="chat-history",
                style={
                    "height": "400px",
                    "overflowY": "auto",
                    "padding": "10px",
                    "backgroundColor": "#f4f4f4",
                    "borderRadius": "10px"
                }
            )
        ]),
        dbc.CardFooter([
            dbc.InputGroup([
                dbc.Input(id="query", placeholder="Type your message...", type="text",  n_submit=0,),
                dbc.Button("Send", id="submit", color="primary", n_clicks=0),
            ], style={"width": "100%"})
        ])
    ], style={"margin": "10px", "height": "550px"})

    upload_title = dbc.Col(html.H4(["Upload your documents"], style={"textAlign": "center", "margin":"10px"}), width=3)

    drop_box = dcc.Upload(
                        id='upload-data',
                        children=html.Div(id="upload-box-content", children=[
                            html.Div([
                                'Drag and Drop or ',
                                html.A('Select Files')
                            ], style={"marginBottom": "10px"})
                        ]),
                        style={
                            'width': '100%',
                            'height': '200px',
                            'lineHeight': 'normal',
                            'borderWidth': '2px',
                            'borderStyle': 'dashed',
                            'borderRadius': '10px',
                            'textAlign': 'center',
                            'margin': '10px',
                            'backgroundColor': '#f9f9f9',
                            'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.2)',
                            'overflowY': 'auto',
                            'padding': '10px'
                        },
                        multiple=True
                    )

    upload_submit_button = dbc.Button("Upload", id='upload', size="me-1", className="me-1", style={"margin": "10px 35%",
                                                                                    "backgroundColor": "#2832C2",
                                                                                    "borderStyle":"none",
                  
                                                                                    'width': "30%"})
    card_content = [
    dbc.CardHeader("Uploaded Files"),
    dbc.CardBody(
        [
            dbc.ListGroup(id="uploaded-files-list", children=[])
        ]
    ),
]
    uploaded_files_card  = dbc.Card(card_content, color="success", outline=True, style={"margin": "10px 10px", "height": "200px",
                                                                                        'overflowY': 'auto',
                                                                                        'width': '100%',})   

    app.layout = html.Div(children=[
        dbc.Row([header]),
        dbc.Row([upload_title, response_title]),
        dbc.Row([dbc.Col([drop_box, upload_submit_button, uploaded_files_card], width=3, style={"display": "flex",
                                                                            "flexDirection": "column",
                                                                            "alignItems": "top center",
                                                                            "justifyContent": "top center"}), 
            dbc.Col([card], width=9)]),
        dbc.Row([])
        
    ])

    app.layout.children.extend([
        dcc.Store(id="chat-store", data=[]),
    ])
    logger.info("UI initialized successfully")
    
    return app
