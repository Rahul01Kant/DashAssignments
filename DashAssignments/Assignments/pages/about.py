from dash import html, dcc, dash_table
import pandas as pd
import json

def get_JsonData():
    file = open('assets/config_about.json')
    json_data = json.load(file)
    return json_data


dfr = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
)
df = dfr[["continent", "country", "pop", "lifeExp"]]

table = dash_table.DataTable(
    id='table',
    data=df.to_dict('records'),
    page_size=15
)

pageSize_dropdown = html.Div(
    children=[
        html.Label('Select Page Size'),
        dcc.Dropdown(options=[10, 15, 20], value=10, id='page_dropdown')
    ])

continent_dropdown = html.Div(
    children=[
        dcc.Dropdown(options=df['continent'].unique(
        ), value='', id='continent_dropdown', placeholder='Select Continent')
    ])

country_dropdown = html.Div(
    children=[
        dcc.Dropdown(options=df['country'].unique(), value='',
                     id='country_dropdown', placeholder='Select country')
    ])

population_rangeSlider = html.Div(
    children=[
        dcc.RangeSlider(
            min=df['pop'].min(),
            max=df['pop'].max(),
            # step=1000000,
            value=[df['pop'].min(), df['pop'].max()],
            id='population_slider')
    ])

lifeExp_rageSlider = html.Div(
    children=[
        dcc.RangeSlider(
            min=df['lifeExp'].min(),
            max=df['lifeExp'].max(),
            # step=1000000,
            value=[df['lifeExp'].min(), df['lifeExp'].max()],
            id='lifeExp_slider'
        )
    ]
)

about_layout = html.Div(
    children=[
        html.H3(children='Introduction to GapMinder', className='intro'),
        html.Div(
            children=[
                html.P(children=get_JsonData()['intro_part1']),
                html.Ol(children=[
                    html.Li(children=get_JsonData()['intro_part1_list1']),
                    html.Li(children=get_JsonData()['intro_part1_list2']),
                    html.Li(children=get_JsonData()['intro_part1_list3']),
                    html.Li(children=get_JsonData()['intro_part1_list4']),
                ])
            ]
        ),
        html.Div(
            children=[
                pageSize_dropdown,
                table,
                html.Div(
                    children=[
                        continent_dropdown,
                        country_dropdown,
                        population_rangeSlider,
                        lifeExp_rageSlider
                    ],
                    className='filters_container'
                )
            ]
        ),
        html.Div(
            children=[
                html.Button(children='Download CSV', id='download_CSV'),
                dcc.Download(id="download")
            ]
        )
    ]
)


def getUpdatedDataFrame(continent, country, popValue, lifeExpValue):
    dataFrame = df.copy(deep=True)
    if not continent and not country and not popValue and not lifeExpValue:
        return dataFrame.to_dict('records')

    if continent:
        dataFrame = dataFrame[dataFrame['continent'] == continent]

    if country:
        dataFrame = dataFrame[dataFrame['country'] == country]

    dataFrame = dataFrame[(popValue[0] <= dataFrame['pop'])
                          & (dataFrame['pop'] <= popValue[1])]
    dataFrame = dataFrame[(lifeExpValue[0] <= dataFrame['lifeExp']) & (
        dataFrame['lifeExp'] <= lifeExpValue[1])]
    return dataFrame


def dataFrame():
    return dfr

def aboutlogout():
    return about_layout
