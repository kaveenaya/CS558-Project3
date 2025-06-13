import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import networkx as nx

# ========== Prepare Data ==========

# Road condition data by county and month
months = pd.date_range('2024-01-01', periods=12, freq='ME')
counties = ['Multnomah', 'Lane', 'Benton', 'Jackson', 'Deschutes']
road_risk_values = [1, 2, 1.5, 2.5, 1.2]

road_data = pd.DataFrame({
    'month': months.repeat(len(counties)),
    'county': counties * len(months),
    'road_risk': road_risk_values * len(months)
})

# Natural disaster data (e.g., wildfire risk)
disaster_data = pd.DataFrame({
    'county': counties,
    'wildfire_risk': [2, 4, 1, 5, 3]
})

# Merge for dashboard use
merged_data = road_data.merge(disaster_data, on='county')

# ========== Uncertainty data (example) ==========
# Let's say uncertainty is related to weather volatility
import numpy as np
np.random.seed(42)
merged_data['uncertainty'] = np.random.uniform(0.1, 0.5, len(merged_data))

# ========== Causal Factor Network ==========
G = nx.DiGraph()
G.add_edges_from([
    ('Road Conditions', 'Travel Safety'),
    ('Wildfire Risk', 'Travel Safety'),
    ('Weather Volatility', 'Uncertainty'),
    ('Uncertainty', 'Travel Safety'),
])

pos = nx.spring_layout(G)

edge_x = []
edge_y = []
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_x.extend([x0, x1, None])
    edge_y.extend([y0, y1, None])

edge_trace = go.Scatter(
    x=edge_x, y=edge_y,
    line=dict(width=2, color='#888'),
    hoverinfo='none',
    mode='lines')

node_x = []
node_y = []
for node in G.nodes():
    x, y = pos[node]
    node_x.append(x)
    node_y.append(y)

node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers+text',
    hoverinfo='text',
    marker=dict(
        showscale=False,
        color='lightblue',
        size=30,
        line_width=2),
    text=list(G.nodes()),
    textposition="bottom center"
)

# ========== Dash App Setup ==========

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Oregon Low-Risk Destination Dashboard"),
    dcc.Dropdown(
        id='county-dropdown',
        options=[{'label': c, 'value': c} for c in counties],
        value='Multnomah',
        clearable=False
    ),
    dcc.Graph(id='road-risk-trend'),
    dcc.Graph(id='wildfire-risk-bar'),
    dcc.Graph(id='causal-network'),
    html.Div(id='uncertainty-info')
])

# ========== Callbacks ==========

@app.callback(
    Output('road-risk-trend', 'figure'),
    Output('wildfire-risk-bar', 'figure'),
    Output('causal-network', 'figure'),
    Output('uncertainty-info', 'children'),
    Input('county-dropdown', 'value')
)
def update_dashboard(selected_county):
    filtered = merged_data[merged_data['county'] == selected_county]

    # Road risk trend line plot
    fig_road = px.line(filtered, x='month', y='road_risk',
                       title=f'Road Risk Trend in {selected_county}',
                       labels={'month':'Month', 'road_risk':'Road Risk Level'})

    # Wildfire risk bar chart (static since by county only)
    fig_wildfire = px.bar(disaster_data, x='county', y='wildfire_risk',
                          title='Wildfire Risk by County',
                          labels={'county':'County', 'wildfire_risk':'Wildfire Risk Level'})
    fig_wildfire.update_traces(marker_color='firebrick')
    fig_wildfire.update_layout(xaxis={'categoryorder':'total descending'})

    # Causal network graph
    fig_causal = go.Figure(data=[edge_trace, node_trace])
    fig_causal.update_layout(
        title='Causal Factor Network',
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20,l=5,r=5,t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )

    # Show uncertainty info for selected county averaged over months
    uncertainty_avg = filtered['uncertainty'].mean()
    uncertainty_text = f"Average uncertainty due to weather volatility in {selected_county}: {uncertainty_avg:.2f}"

    return fig_road, fig_wildfire, fig_causal, uncertainty_text

if __name__ == '__main__':
    app.run(debug=True)
