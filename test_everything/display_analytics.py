from flask import Flask
from flask_cors import CORS
import plotly.express as px
from dash import Dash, html, dash_table, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import os
from invokes import invoke_http
from os import environ
import requests

app = Flask(__name__)
CORS(app)
data_URL = environ.get('retrieve_data_URL') or "http://localhost:5003/data" 

d_app = Dash(__name__, server=app, url_base_pathname="/analytics/", external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions=True)
d_app.layout = html.Div ("")

@app.route("/analytics/<string:restaurant_username>", methods=["GET"])
def display_analytics(restaurant_username):
    restaurant_username = {"restaurant_username":restaurant_username}
    all_data = invoke_http(data_URL, method='GET', json=restaurant_username)
    check_reviews = all_data["data"]["review"]
    if check_reviews != []:
        reviews = all_data["data"]["review"]["reviews"]
        Average_ratings = all_data["data"]["review"]["rating"]
        Total_num_ratings = all_data["data"]["review"]["user_ratings_total"]
        cards =  [dbc.Card(children=[
                dbc.CardHeader([
                        html.H4(str(review["rating"])+" Stars"),
                        html.H4(review["author_name"])
                ])
                ,
                dbc.CardBody(children=[html.P(review["text"])])
                ,]) for review in reviews]
        review_cards = dbc.CardGroup(cards)
        total_reviews = html.H5(Total_num_ratings)
        average_ratings = html.H5(Average_ratings)
    else:
        review_cards = html.H4("No reviews found")
        total_reviews = html.H4("No reviews found")
        average_ratings = html.H4("No ratings found")

        

    reservations = all_data["data"]["reservation"]
    if reservations != []:
        reservations = pd.DataFrame(reservations)
        reservations['reservation_date'] = pd.to_datetime(reservations['reservation_date'])
        reservations = reservations.sort_values("reservation_date")
 
        reservations_num_by_date = reservations.groupby("reservation_date").size().reset_index(name="num_reservations")
        num_customers_by_date = reservations.groupby("reservation_date")["num_of_pax"].agg("sum")
        num_customers_by_date.index = num_customers_by_date.index.date
        num_customers_by_date =  num_customers_by_date.rename_axis("date")
        num_customers_by_date =  num_customers_by_date.reset_index().to_dict("records")
   
        num_customers_by_month = reservations.groupby(pd.Grouper(key="reservation_date", freq="M"))["num_of_pax"].agg("sum")
        num_customers_by_month.index =num_customers_by_month.index.strftime("%B")
        num_customers_by_month =  num_customers_by_month.rename_axis("month")
        num_customers_by_month =  num_customers_by_month.reset_index().to_dict("records")
        fig1 = px.line(reservations_num_by_date , x='reservation_date', y='num_reservations',title='Reservation Time Series with Rangeslider', labels={'reservation_date': "Date", "num_reservations":"Number of Reservations"})
        fig1.update_xaxes(rangeslider_visible=True, rangeselector_buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(step="all")
            ])
            )
        graph = dcc.Graph(figure=fig1, id='num_resr')
        table_cust_day =dash_table.DataTable(data = num_customers_by_date,page_size=6)
        table_cust_month = dash_table.DataTable(data = num_customers_by_month,page_size=6)
    else:
        graph = html.H4("No past reservation data")
        table_cust_day = html.H4("No past reservation customer data")
        table_cust_month = html.H4("No past reservation customer data")

    d_app.layout = html.Div([
        html.Form(
        html.Button("Back to profile", type="submit"),
        action="http://localhost/esd_proj/profile.html",),
        html.Div([html.H4('Number of Reservations',style={'background-color':'#ad2b2d','color':'white','text-align':'center','padding':'10px'}),
        graph],style={'margin':'20px'}),
        html.Div([
        dbc.Row([dbc.Col([html.H4("Number of Customers by reservations (by day)",style={'background-color':'#ad2b2d','color':'white','text-align':'center','padding':'10px'}),
        #dash table
        table_cust_day]),
        dbc.Col([
        html.H4("Number of Customers by reservations (by month)",style={'background-color':'#ad2b2d','color':'white','text-align':'center','padding':'10px'}),
        # #dash table
        table_cust_month
        ])])
        ],style={'margin':'20px'}),
        
        html.Div([html.H4('Most Recent Google Reviews:',style={'background-color':'#ad2b2d','color':'white','text-align':'center','padding':'10px'}),
        review_cards],style={'margin':'20px'}),
        html.Div([
        dbc.Row([dbc.Col([ html.H4("Total number of Google Reviews:",style={'background-color':'#ad2b2d','color':'white','text-align':'center','padding':'10px'}),
        total_reviews]),
        dbc.Col([
        html.H4("Average Rating (Google Reviews):",style={'background-color':'#ad2b2d','color':'white','text-align':'center','padding':'10px'}),
        average_ratings
        ])])
        ],style={'margin':'20px'}),
        
    ])

    return (
            d_app.index()
        ) 

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for displaying analytics...")
    app.run(host="0.0.0.0", port=4020, debug=True)
