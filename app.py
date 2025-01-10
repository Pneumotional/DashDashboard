import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sqlite3
from datetime import datetime
import io
import base64
import chardet
from dash_iconify import DashIconify

app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP, '/assets/style.css'],  use_pages=True, suppress_callback_exceptions=True)



def create_database():
    conn = sqlite3.connect('insurance_data.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS insurance_transactions (
        [Transaction Date] TEXT, [Policy No] TEXT, [Trans Type] TEXT, 
        Branch TEXT, Class TEXT, [Dr/Cr No] TEXT, [Risk ID] TEXT,
        Insured TEXT, [Intermediary Type] TEXT, Intermediary TEXT,
        Marketer TEXT, WEF TEXT, WET TEXT, CURRENCY TEXT,
        [Sum Insured] REAL, Premium REAL, PAID REAL,
        Year INTEGER, [Month Name] TEXT, Month INTEGER,
        Quarter INTEGER, Weeks INTEGER)''')
    conn.commit()
    conn.close()

# Initialize the Dash app with dark theme and Bootstrap


# Database functions

navbar = dbc.Navbar(
    children=[
        dbc.NavItem(dbc.NavLink("Dashboard", href="/")),
        dbc.NavItem(dbc.NavLink("Brokers", href="/brokers")),
        dbc.NavItem(dbc.NavLink("Agents", href="/agents")),
        dbc.NavItem(dbc.NavLink("Reinsurance", href="/reinsurance")),
        dbc.NavItem(dbc.NavLink("Delete", href="/data")),
    ],
    # brand="Insurance Analytics",
    # brand_href="/",
    color="dark",
    dark=True,
    # className="dark mb-4 bg-dark"
)
# color_mode_switch =  html.Span(
#     [
#         dbc.Label(className="fa fa-moon", html_for="switch"),
#         dbc.Switch( id="switch", value=True, className="d-inline-block ms-1", persistence=True),
#         dbc.Label(className="fa fa-sun", html_for="switch"),
#     ]
# )

app.layout = dbc.Container([
    # color_mode_switch,
    navbar,
dbc.Row([
    dbc.Col([
        html.Div([
            dbc.Card([
                dbc.CardBody([
                    dbc.Switch(
                        id='theme-switch',
                        label=DashIconify(icon="ph:moon-fill", width=20),
                        value=True,
                        className='theme-switch'
                    )
                ])
            ], className='theme-switch-card')
        ], className='theme-switch-container')
    ], width=12)
], className="mb-4"),
        
    dbc.Row([
        dbc.Col(html.H1("Insurance Dashboard", className="text-center text-light mb-4"), width=12)
    ]),
    
    dash.page_container
], fluid=True, className='app-container', id='main-container')


@app.callback(
    [Output('main-container', 'className'),
     Output('class-premium-table', 'style_header'),
     Output('class-premium-table', 'style_cell'),
     Output('weekly-monthly-table', 'style_header'),
     Output('weekly-monthly-table', 'style_cell')
     ],
    [Input('theme-switch', 'value')]
)
def update_theme(dark_mode):
    if dark_mode:
        container_class = 'app-container dark-theme'
        table_header = {
            'backgroundColor': 'rgb(30, 30, 30)',
            'color': 'white',
            
        }
        table_cell = {
            'backgroundColor': 'rgb(50, 50, 50)',
            'color': 'white',
            'border': '1px solid rgb(70, 70, 70)'
        }
    else:
        container_class = 'app-container light-theme'
        table_header = {
            'backgroundColor': 'rgb(240, 240, 240)',
            'color': 'black',
            'fontWeight': 'bold'
        }
        table_cell = {
            'backgroundColor': 'white',
            'color': 'black',
            'border': '1px solid rgb(200, 200, 200)'
        }
    
    return container_class, table_header, table_cell, table_header, table_cell

# app.clientside_callback(
#     """
#     (switchOn) => {
#         document.documentElement.setAttribute("data-bs-theme", switchOn ? "light" : "dark");
#         return window.dash_clientside.no_update
#     }
#     """,
   
#     Output("switch", "id"),
#     Input("switch", "value"),
# )


if __name__ == '__main__':
    create_database()
    app.run_server(debug=True)