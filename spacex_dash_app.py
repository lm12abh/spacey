# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launch_sites = spacex_df['Launch Site'].unique().tolist()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                    {'label': 'All Sites', 'value': 'ALL'},
                                                    {'label': launch_sites[0], 'value': launch_sites[0]},
                                                    {'label': launch_sites[1], 'value': launch_sites[1]},
                                                    {'label': launch_sites[2], 'value': launch_sites[2]},
                                                    {'label': launch_sites[3], 'value': launch_sites[3]},
                                                        ],
                                                value='ALL',
                                                placeholder="elect a Launch Site here",
                                                searchable=True
                                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={i:'{}'.format(i) for i in range(0, 10000, 1000)},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        value_count = spacex_df.groupby('Launch Site')['class'].sum().reset_index(name='counts')
        fig = px.pie(value_count, values='counts', 
        names='Launch Site', 
        title='Total Success Launchrs By Site ' + entered_site)
        return fig
    else:
        counts = spacex_df[spacex_df['Launch Site']==entered_site]['class'].value_counts().reset_index(name='counts')
        fig = px.pie(counts, values='counts', 
        names='index', 
        title='Total Success Launchrs By Site ' + entered_site)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value'))
            
def get_scatter_chart(entered_site, payload):
    if entered_site == 'ALL':
        filtered_df = spacex_df[(spacex_df['Payload Mass (kg)']>=payload[0]) &
                                (spacex_df['Payload Mass (kg)']<=payload[1]) ]
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class', color="Booster Version Category",
                 hover_data=['Launch Site'], 
        title='Correlation between Payload and Success for all Sites')
        return fig
    else:
        filtered_df_2 = spacex_df[(spacex_df['Launch Site']==entered_site) &
                                (spacex_df['Payload Mass (kg)']>=payload[0]) &
                                (spacex_df['Payload Mass (kg)']<=payload[1])]
        fig = px.scatter(filtered_df_2, x='Payload Mass (kg)', y='class', color="Booster Version Category",
                 hover_data=['Launch Site'], 
        title='Correlation between Payload and Success for '+entered_site)
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
