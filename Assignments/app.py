import dash
from dash import Dash, html, dcc, Input, Output, callback, State
import dash_bootstrap_components as dbc
from flask import Flask
from flask_login import LoginManager, UserMixin, login_user
from pages.register_callbacks import allCallbacks
from dash.exceptions import PreventUpdate
import sqlite3

server = Flask(__name__)
server.config.update(SECRET_KEY='MY_SECRET_KEY')

app = Dash(__name__,
           server=server,
           use_pages=False,
           external_stylesheets=[dbc.themes.BOOTSTRAP],
           suppress_callback_exceptions=True
           )

login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'


class User(UserMixin):
    def __init__(self, username):
        self.id = username


@ login_manager.user_loader
def load_user(username):
    return User(username)


navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("About", href="/about")),
        dbc.NavItem(dbc.NavLink("Input Field", href="/inputField")),
        dbc.NavItem(dbc.NavLink("Simulation", href="simulation")),
        dbc.NavItem(dbc.NavLink("Logout", href="/logout")),
    ],
    # brand="NavbarSimple",
    # brand_href="#",
    color="primary",
    # dark=True,
)

app.layout = html.Div(
    children=[
        dcc.Store(id='session', storage_type='session'),
        dcc.Location(id='url', refresh=False),
        dcc.Location(id='redirect', refresh=True),
        html.Div(children=[
            html.Img(src='assets/tiger_analytics.png',
                     className='company_logo'),
            navbar,
        ], className='topNav_container'),
        html.Div(id='page-content')
    ], )


@app.callback(
    Output('redirect', 'pathname'),
    Output('incorrectCredentials', 'children'),
    Input('loginUser', 'n_clicks'),
    [State('usernameField', 'value'),
     State('passwordField', 'value')
     ],
    prevent_initial_call=True
)
def checkLogin(n_clicks, userName, password):
    if not n_clicks:
        raise PreventUpdate
    # if n_clicks and n_clicks > 0:
    #     if userName == 'test' and password == 'test':
    #         user = User(userName)
    #         login_user(user)
    #         return '/about', dash.no_update
    #     else:
    #         return '/login', 'Incorrect Credentials Try Again'

    # return dash.no_update

    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    command = """CREATE TABLE IF NOT EXISTS users(name TEXT, password TEXT)"""
    cursor.execute(command)
    cursor.execute("INSERT INTO users VALUES ('admin','1234')")
    connection.commit()
    query = "SELECT name,password FROM users where name= '" + \
        userName+"' and password='"+password+"'"
    cursor.execute(query)
    results = cursor.fetchall()
    if len(results) != 0:
        user = User(userName)
        login_user(user)
        return '/about', dash.no_update
    else:
        return '/login', 'Incorrect Credentials Try Again'


allCallbacks()

if __name__ == '__main__':
    app.run(debug=True)
