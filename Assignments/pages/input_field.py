import dash
from dash import Dash, html, dcc, dash_table, Input, Output, callback,State
import dash_bootstrap_components as dbc
import json
from dash.exceptions import PreventUpdate

app = Dash(__name__)

dash.register_page(__name__, path='/inputField')

layout = html.Div(children=[
    html.Div(children=[
    html.Div(children=[
        html.H3(children='User Input',className='tab'),
        html.Div(children=[
            html.Div(children=[
                dbc.Label('Latitude *',className='header'),
                dbc.Input(valid='',placeholder='Latitude Eg:39.54',id='latitude')
            ],className='UserInput'),
            html.Hr(),
            html.Div(children=[
                dbc.Label('Longitude *',className='header'),
                dbc.Input(valid='',placeholder='Longitude Eg:79.54',id='longitude')
            ],className='UserInput'),
            html.Hr(),
            html.Div(children=[
                dbc.Label('Data *',className='header'),
                dbc.Input(valid='',placeholder='Enter Dataset GDP vs (country or year)',id='data')
            ],className='UserInput'),
            html.Hr(),
            html.Div(children=[
                dbc.Label('Country *',className='header'),
                dbc.Input(valid='',placeholder='Enter a Country Name',id='country')
            ],className='UserInput'),
            html.Hr(),
        ],className='formContainer')
        
    ],className='cont'),
    html.Div(children=[
        html.H3(children='Calculated Input',className='tab'),
    ],className='cont')
    ],className='inputFieldContainer'),
    html.Div(children=[
        html.Button(children='SIMULATE',className='btn btn-primary',id='simulate_input_field')],className='simulateButton')
    ]
    )

@callback(
    Output('session', 'data'),
    Input('simulate_input_field','n_clicks'),
    [State('latitude','value'),
    State('longitude','value'),
    State('data','value'),
    State('country','value'),
     ],
    prevent_initial_call=True,
)
def store_data(n_clicks,latitude,longitude,data,country):
    if not n_clicks:
        raise PreventUpdate
    input_field_Data ={
        'latitude': latitude,
        'longitude': longitude,
        'data': data,
        'country': country
    }
    return json.dumps(input_field_Data, indent = 4) 

