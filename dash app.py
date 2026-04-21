import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback

# Load the generated CSV data
df = pd.read_csv('pink morsels.csv')

# Convert Date to datetime and sort by date
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date').reset_index(drop=True)

# Create Dash app
app = Dash(__name__)

# Layout
app.layout = html.Div([
    # Header
    html.H1("Pink Morsel Sales Visualizer",
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),

    # Line chart
    dcc.Graph(id='sales-line-chart'),

    # Dropdown for filtering by Region
    html.Div([
        html.Label("Filter by Region:", style={'fontSize': 18, 'marginRight': 10}),
        dcc.Dropdown(
            id='region-dropdown',
            options=[{'label': r, 'value': r} for r in sorted(df['Region'].unique())] +
                    [{'label': 'All Regions', 'value': 'All'}],
            value='All',
            style={'width': 300}
        ),
    ], style={'marginBottom': 30}),

    html.Div(id='stats-info', style={'textAlign': 'center', 'fontSize': 14, 'color': '#7f8c8d'})
])


@callback(
    [Output('sales-line-chart', 'figure'),
     Output('stats-info', 'children')],
    [Input('region-dropdown', 'value')]
)
def update_chart(selected_region):
    # Filter data based on selection
    filtered_df = df if selected_region == 'All' else df[df['Region'] == selected_region]

    # Aggregate sales by date
    agg_df = filtered_df.groupby('Date')['Sales'].sum().reset_index()

    # Create line chart
    fig = px.line(agg_df, x='Date', y='Sales',
                  title=f"{'Total' if selected_region == 'All' else selected_region.capitalize()} Pink Morsel Sales Over Time",
                  labels={'Date': 'Date', 'Sales': 'Total Sales ($)'},
                  markers=True)

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Total Sales ($)",
        hovermode='x unified',
        template='plotly_white',
        height=600
    )

    # Stats
    total_sales = filtered_df['Sales'].sum()
    avg_sales = filtered_df['Sales'].mean()
    stats = f"Total Sales: ${total_sales:,.2f} | Avg Daily Sales: ${avg_sales:.2f}"

    return fig, stats


if __name__ == '__main__':
    app.run_server(debug=True)