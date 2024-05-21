import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

app = Dash(__name__,
        use_pages=True,
        external_stylesheets=[dbc.themes.BOOTSTRAP])

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("About", href="/about")),
        dbc.NavItem(dbc.NavLink("Input Field", href="/inputField")),
        dbc.NavItem(dbc.NavLink("Simulation", href="simulation")),
        dbc.NavItem(dbc.NavLink("Logout", href="#")),
    ],
    # brand="NavbarSimple",
    # brand_href="#",
    color="primary",
    # dark=True,
)

app.layout = html.Div(
    children=[
        dcc.Store(id='session', storage_type='session'),
        html.Div(children=[
            html.Img(src='assets/tiger_analytics.png',className='company_logo'),
            navbar, 
        ],className='topNav_container'),
        html.Div(
            children=[
                dash.page_container
            ]
        )
], )


if __name__ == '__main__':
    app.run(debug=True)