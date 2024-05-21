import dash
from dash import Dash, html, dcc, dash_table, Input, Output, callback, State
import dash_bootstrap_components as dbc
import json
import plotly.express as px
import dash_leaflet as dl
from pages.about import dataFrame


dash.register_page(__name__, path='/simulation')

map = dl.Map(
    dl.TileLayer(),
    id="map-output",
    center=[20, 20],  # default values
    zoom=6,
    style={
        "height": 400,
        "width": "95%",
        "margin": "auto",
        "marginTop": "30px",
    },
)

layout = html.Div(children=[
    map,
    html.Div(children=[
        html.Div(children=[
            html.Label('User Provided Fields', className='userProvidedField'),
            html.Div(children=[
                html.Div(children=[
                    html.Div(children=[
                        html.Div(children=[
                            dbc.Label('Latitude', className='header'),
                            dbc.Input(valid='',
                                      id='latitude1', disabled=True)
                        ], className='UserInput'),
                        html.Hr(),
                        html.Div(children=[
                            dbc.Label('Longitude', className='header'),
                            dbc.Input(valid='',
                                      id='longitude1', disabled=True)
                        ], className='UserInput'),
                        html.Hr(),
                        html.Div(children=[
                            dbc.Label('Data', className='header'),
                            dbc.Input(
                                valid='', id='data1', disabled=True)
                        ], className='UserInput'),
                        html.Hr(),
                        html.Div(children=[
                            dbc.Label('Country', className='header'),
                            dbc.Input(
                                valid='', id='country1', disabled=True)
                        ], className='UserInput'),
                        html.Hr(),
                    ], className='formContainer')
                ]),
                html.Div(children='Output generated')
            ], className='inputedFields')
        ], style={'width': '100%'}),
        html.Div(children=[
            html.Label('Country Data', className='userProvidedField'),
            html.Div(children=[
                html.Div(children=[
                    html.Label('Total GDP'),
                    html.Span(children='dfdsf')
                ], className='countryItem'),
                html.Hr(),
                html.Div(children=[
                    html.Label('Total Population'),
                    html.Span(children='dfdsf')
                ], className='countryItem'),
                html.Hr(),
                html.Div(children=[
                    html.Label('Average life Expectancy'),
                    html.Span(children='dfdsf')
                ], className='countryItem'),
                html.Hr(),
            ], className='countryclass')
        ], style={'width': '50%'})
    ], className='inputandcountry'),
    html.Div(children=[
        html.Label('Calculated Bar Chart',
                   className='userProvidedField calculatedBarChart'),
        html.Div(children=[
            dcc.Graph(id='bar-chart')
        ], className='calculatedBarChart')
    ]),
    html.Div(children=[
        html.Label('GDP per capita Over country',
                   className='userProvidedField calculatedBarChart'),
        html.Div(children=[
            dcc.Graph(id='country-bar-chart')
        ], className='calculatedBarChart')
    ])
], id='simulation')


@callback(
    Output('latitude1', 'value'),
    Output('longitude1', 'value'),
    Output('data1', 'value'),
    Output('country1', 'value'),
    Input('session', 'data')
)
def getStoredData(data):
    res = json.loads(data)

    return res['latitude'], res['longitude'], res['data'], res['country']


@callback(
    Output("map-output", "children"),
    Output("map-output", "center"),
    Input('session', 'data')
)
def simulation_map(data):
    res = json.loads(data)
    marker = dl.Marker(
        position=[res['latitude'], res['longitude']],
        children=[dl.Tooltip(
            f"Latitude: {res['latitude']}, Longitude: {res['longitude']}")],
    )
    center = [res['latitude'], res['longitude']]
    return [dl.TileLayer(), marker], center


@callback(
    Output('bar-chart', 'figure'),
    Output('country-bar-chart', 'figure'),
    Input('session', 'data')
)
def update_output(data):
    res = json.loads(data)
    actualDataFrame = dataFrame()
    df = actualDataFrame[actualDataFrame['country'] == res['country']]
    fig = px.bar(df, x=df['year'],
                 hover_data=['continent', 'country', 'pop', 'lifeExp'],
                 y=df['pop'], color=df['lifeExp'],
                 labels={'pop': 'population of' + ' ' + f'{res['country']}'})
    fig1 = px.bar(actualDataFrame, x=actualDataFrame['country'],
                  y=actualDataFrame['gdpPercap'],
                  labels={'gdpPercap': 'GDP Per Capita'})
    return fig,fig1
