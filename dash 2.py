import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback

df = pd.read_csv("pink morsels.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date").reset_index(drop=True)

app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        html.H1("Pink Morsel Sales Dashboard", className="title"),
        html.P("Elegant sales overview by region and date", className="subtitle")
    ], className="header"),

    html.Div([
        html.Div([
            html.Label("Filter by Region", className="label"),
            dcc.Dropdown(
                id="region-dropdown",
                options=[{"label": "All Regions", "value": "All"}] +
                        [{"label": r, "value": r} for r in sorted(df["Region"].dropna().unique())],
                value="All",
                clearable=False,
                className="dropdown"
            )
        ], className="control-box")
    ], className="controls"),

    dcc.Graph(id="sales-line-chart"),
    dcc.Graph(id="sales-pie-chart"),

    html.Div(id="stats-cards", className="stats-row")
], className="page")


@callback(
    [Output("sales-line-chart", "figure"),
     Output("sales-pie-chart", "figure"),
     Output("stats-cards", "children")],
    [Input("region-dropdown", "value")]
)
def update_dashboard(region):
    filtered = df.copy()
    if region != "All":
        filtered = filtered[filtered["Region"] == region]

    daily = filtered.groupby("Date", as_index=False)["Sales"].sum()
    region_sales = filtered.groupby("Region", as_index=False)["Sales"].sum()

    line_fig = px.line(
        daily, x="Date", y="Sales",
        markers=True,
        title="Daily Sales Trend"
    )
    line_fig.update_traces(line_color="#2563eb", line_width=3)
    line_fig.update_layout(
        template="plotly_white",
        height=500,
        margin=dict(l=30, r=30, t=60, b=30),
        title_x=0.5
    )

    pie_fig = px.pie(
        region_sales,
        names="Region",
        values="Sales",
        hole=0.45,
        title="Sales Share by Region"
    )
    pie_fig.update_traces(textposition="inside", textinfo="percent+label")
    pie_fig.update_layout(
        template="plotly_white",
        height=500,
        margin=dict(l=30, r=30, t=60, b=30),
        title_x=0.5
    )

    total_sales = filtered["Sales"].sum()
    avg_sales = filtered["Sales"].mean()
    peak_sales = filtered["Sales"].max()
    first_sales = daily["Sales"].iloc[0] if not daily.empty else 0
    last_sales = daily["Sales"].iloc[-1] if not daily.empty else 0
    growth = ((last_sales - first_sales) / first_sales * 100) if first_sales else 0

    cards = [
        html.Div([html.H3(f"${total_sales:,.0f}"), html.P("Total Sales")], className="card"),
        html.Div([html.H3(f"${avg_sales:,.0f}"), html.P("Average / Day")], className="card"),
        html.Div([html.H3(f"${peak_sales:,.0f}"), html.P("Peak Sales")], className="card"),
        html.Div([html.H3(f"{growth:+.1f}%"), html.P("Growth")], className="card"),
    ]

    return line_fig, pie_fig, cards


if __name__ == "__main__":
    app.run_server(debug=True)