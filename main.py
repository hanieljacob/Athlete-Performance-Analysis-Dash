import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

df = pd.read_csv("BU-Athletics-Data.csv")
df = df.groupby(['Entering Term', 'US Region', 'ACADINDEX'])[['Last Cumulative BU GPA']].mean().reset_index()

unique_terms = sorted(df['Entering Term'].unique())

region_state_codes = {
    'Midwest': ['IL', 'IN', 'IA', 'KS', 'MI', 'MN', 'MO', 'NE', 'ND', 'OH', 'SD', 'WI'],
    'Northeast': ['CT', 'ME', 'MA', 'NH', 'RI', 'VT', 'NJ', 'NY', 'PA'],
    'South': ['DE', 'FL', 'GA', 'MD', 'NC', 'SC', 'VA', 'WV', 'AL', 'KY', 'MS', 'TN', 'AR', 'LA', 'OK', 'TX'],
    'West': ['AZ', 'CO', 'ID', 'MT', 'NV', 'NM', 'UT', 'WY', 'AK', 'CA', 'HI', 'OR', 'WA']
}

app.layout = html.Div([
    html.H1("Athlete Academic Performance By Entering Term", style={'text-align': 'center'}),
    dcc.Dropdown(id="select_year",
                 options=[{'label': term, 'value': term} for term in unique_terms],
                 multi=False,
                 value='Fall2018',
                 style={'width': "40%"}),
    html.Br(),
    dcc.Graph(id='student_graph', figure={})
])


@app.callback(
    Output(component_id='student_graph', component_property='figure'),
    [Input(component_id='select_year', component_property='value')]
)
def update_graph(selected_year):
    dff = df.copy()
    dff = dff[dff['Entering Term'] == selected_year]
    dff['State Code'] = dff['US Region'].map(lambda x: region_state_codes.get(x, None))
    dff = dff.dropna(subset=['State Code'])
    dff = dff.explode('State Code')
    fig = px.choropleth(data_frame=dff,
                        locationmode='USA-states',
                        locations='State Code',
                        scope='usa',
                        color='Last Cumulative BU GPA',
                        hover_data=['US Region', 'ACADINDEX'],
                        color_continuous_scale=px.colors.sequential.YlOrRd,
                        template='plotly_dark')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
