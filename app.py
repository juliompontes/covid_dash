import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px


url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
data = pd.read_csv(url)

data.drop(['new_cases_smoothed', 'new_deaths_smoothed', 'total_cases_per_million','new_cases_per_million', 'new_cases_smoothed_per_million',
       'new_deaths_smoothed_per_million', 'reproduction_rate', 'icu_patients',
       'icu_patients_per_million', 'hosp_patients',
       'hosp_patients_per_million', 'weekly_icu_admissions',
       'weekly_icu_admissions_per_million', 'weekly_hosp_admissions',
       'weekly_hosp_admissions_per_million', 'total_tests_per_thousand', 'new_tests_per_thousand',
       'new_tests_smoothed', 'new_tests_smoothed_per_thousand',
       'positive_rate', 'tests_per_case', 'tests_units','new_vaccinations_smoothed',
       'new_vaccinations_smoothed_per_million', 'stringency_index',
       'population_density', 'median_age', 'aged_70_older',
       'cardiovasc_death_rate', 'diabetes_prevalence', 'female_smokers',
       'male_smokers', 'handwashing_facilities', 'hospital_beds_per_thousand',], axis=1, inplace=True)

new_data = data[~data["location"].isin(['Africa', 'Asia', 'Europe', 'European Union', 'International', 'North America', 'Oceania', 'South Africa', 'South America', 'World'])]

all_countries = data.location.unique()

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div([
        html.Div([
            ], className='one-third column'),

        html.Div([
            html.Div([
                html.H2('Covid-19', style={'margin-bottom': '10px', 'color': '#E7E1CF'}),
                html.H5('Covid-19 track dashboard', style={'margin-bottom': '0px', 'color': '#E7E1CF'})
            ])

        ], className='one-half column', id='title'),

        html.Div([
            html.H6('Last Updated: ' + data['date'].iloc[-1], style={'color': '#D48920'})

        ], className='one-third column', id='title1')
    
    ], id='header', className='row flex-display', style={'margin-bottom': '25px'}),

    html.Div([
        html.Div([
            html.H6('Total Cases', style={'textAlign': 'center',
                                           'color': '#E7E1CF'}),
            html.P(f"{data[data['location'] == 'World']['total_cases'].iloc[-1]:,.0f}", style={'textAlign': 'center',
                                    'color': '#D48920',
                                    'fontSize': 35}),

        ], className='card_container three columns'),

html.Div([
            html.H6('Total Deaths', style={'textAlign': 'center',
                                            'color': '#E7E1CF'}),
            html.P(f"{data[data['location'] == 'World']['total_deaths'].iloc[-1]:,.0f}", style={'textAlign': 'center',
                               'color': '#D48920',
                               'fontSize': 35}),

], className='card_container three columns'),

html.Div([
            html.H6('People Vaccinated', style={'textAlign': 'center',
                                            'color': '#E7E1CF'}),
            html.P(f"{data[data['location'] == 'World']['people_vaccinated'].iloc[-1]:,.0f}", style={'textAlign': 'center',
                               'color': '#D48920',
                               'fontSize': 35}),

        ], className='card_container three columns'),

html.Div([
            html.H6('People Fully Vaccinated', style={'textAlign': 'center',
                                            'color': '#E7E1CF'}),
            html.P(f"{data[data['location'] == 'World']['people_fully_vaccinated'].iloc[-1]:,.0f}", style={'textAlign': 'center',
                               'color': '#D48920',
                               'fontSize': 35}),

        ], className='card_container three columns'),

    ], className='row flex-display'),

    html.Div([
        html.Div([
            html.P('Select country:', className='fix_label', style={'color': '#E7E1CF'}),
            dcc.Dropdown(id='countries',
                         multi=False,
                         searchable=True,
                         value='Brazil',
                         placeholder='Select Country',
                         options=[{"label": x, "value": x}for x in all_countries])], className='dcc_compon'),
            dcc.Graph(id='confirmed', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'}),
dcc.Graph(id = 'death', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'}),
dcc.Graph(id = 'vaccinated', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'}),
dcc.Graph(id = 'fully_vaccinated', config={'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'})
         
        ], className="create_container three columns"),
    
        html.Div([
dcc.Graph(id='line_chart', config={'displayModeBar': 'hover'}, style={'margin-top': '0px'}
                    )    
        ], className='create_container four columns'),

html.Div([
dcc.Graph(id='bar_chart', config={'displayModeBar': 'hover'}, style={'margin-top': '0px'}
                    )    
        ], className='create_container four columns')

    ])


@app.callback(Output('confirmed', 'figure'),
              [Input('countries', 'value')])
def update_total_cases(countries):
    return {
        'data': [go.Indicator(
               value = data[data['location'] == countries]['total_cases'].iloc[-1],
               number={'valueformat': ',',
                       'font': {'size': 20}}
        )],

        'layout': go.Layout(
            title={'text': 'Total Cases'},
            font=dict(color='#E7E1CF'),
            paper_bgcolor='#4F4E4F',
            plot_bgcolor='#4F4E4F',
            height = 60,
        )
    }

@app.callback(Output('death', 'figure'),
              [Input('countries', 'value')])
def update_total_deaths(countries):
    return {
        'data': [go.Indicator(
               value = data[data['location'] == countries]['total_deaths'].iloc[-1],
               number={'valueformat': ',',
                       'font': {'size': 20}}
        )],

        'layout': go.Layout(
            title={'text': 'Total Deaths'},
            font=dict(color='#E7E1CF'),
            paper_bgcolor='#4F4E4F',
            plot_bgcolor='#4F4E4F',
            height = 60,
        )
    }

@app.callback(Output('vaccinated', 'figure'),
              [Input('countries', 'value')])
def update_vaccinated(countries):
    return {
        'data': [go.Indicator(
               value = data[data['location'] == countries]['people_fully_vaccinated'].iloc[-1],
               number={'valueformat': ',',
                       'font': {'size': 20}}
        )],

        'layout': go.Layout(
            title={'text': 'People fully vaccinated'},
            font=dict(color='#E7E1CF'),
            paper_bgcolor='#4F4E4F',
            plot_bgcolor='#4F4E4F',
            height = 60,
        )
    }

@app.callback(Output('fully_vaccinated', 'figure'),
              [Input('countries', 'value')])
def update_fully_vaccinated(countries):
    return {
        'data': [go.Indicator(
               value = data[data['location'] == countries]['people_fully_vaccinated'].iloc[-1] / data[data['location'] == countries]['population'].iloc[-1],
               number={'valueformat': '%',
                       'font': {'size': 20}}
        )],

        'layout': go.Layout(
            title={'text': "% of fully vaccinated people"},
            font=dict(color='#E7E1CF'),
            paper_bgcolor='#4F4E4F',
            plot_bgcolor='#4F4E4F',
            height = 60,
        )
    }

@app.callback(Output('line_chart', 'figure'),
              [Input('countries', 'value')])
def line_chart(countries):
    return {
        'data': [go.Scatter(
            x=data[data['location'] == countries]['date'],
            y=data[data['location'] == countries]['new_deaths'],
            name='deaths',
            line=dict(color='#8B0000', width=1)
        ),
            
        ],

        'layout': go.Layout(
            title={'text': 'Deaths per day'},
            titlefont={'color': '#E7E1CF',
                       'size': 20},
            font=dict(color='#E7E1CF'),
            paper_bgcolor='#4F4E4F',
            plot_bgcolor='#4F4E4F',
            hovermode='closest',
            legend={'orientation': 'h',
                    'bgcolor': '#4F4E4F',
                    'xanchor': 'center', 'x': 0.5, 'y': 1.1},
            margin=dict(l=40, r=20, t=100, b=40),
            xaxis=dict(showgrid=True,
                       showticklabels=True,
                       ticks='outside',
                       ),
            yaxis=dict(color='white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       ))
    }

@app.callback(Output('bar_chart', 'figure'),
              [Input('countries', 'value')])
def bar_chart(countries):
    return {
        'data': [go.Scatter(
            x=data[data['location'] == countries]['date'],
            y=data[data['location'] == countries]['new_cases'],
            name='Cases',
            line=dict(color='#90EE90', width=1)
            ),
                 
        ],

        'layout': go.Layout(
            title={'text': 'New cases per day'},
            titlefont={'color': '#E7E1CF',
                       'size': 20},
            font=dict(color='#E7E1CF'),
            paper_bgcolor='#4F4E4F',
            plot_bgcolor='#4F4E4F',
            hovermode='closest',
            legend={'orientation': 'h',
                    'bgcolor': '#4F4E4F',
                    'xanchor': 'center', 'x': 0.5, 'y': 1.1},
            margin=dict(l=40, r=20, t=100, b=40),
            xaxis=dict(showgrid=True,
                       showticklabels=True,
                       ticks='outside',
                       ),
            yaxis=dict(color='white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       ))
    }

if __name__ == '__main__':
    app.run_server(debug=True)
