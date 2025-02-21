import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import webbrowser

# Mintaadatok
data = {
    "Sector": ["Tech", "Tech", "Finance", "Finance"],
    "Industry": ["Software", "Hardware", "Banking", "Insurance"],
    "Stock_Label": ["AAPL", "MSFT", "JPM", "BRK"],
    "Market Cap": [2500, 2200, 400, 700],
    "Change": [1.2, -0.5, 0.8, -0.2],
    "Link": [
        "https://finance.yahoo.com/quote/AAPL",
        "https://finance.yahoo.com/quote/MSFT",
        "https://finance.yahoo.com/quote/JPM",
        "https://finance.yahoo.com/quote/BRK"
    ]
}

df = pd.DataFrame(data)

# Treemap létrehozása
fig = px.treemap(
    df,
    path=['Sector', 'Industry', 'Stock_Label'],
    values='Market Cap',
    color='Change',
    color_continuous_scale='RdYlGn',
    title='Stock Market Heatmap',
    hover_data={'Stock_Label': True, 'Market Cap': True, 'Change': True}
)

# Dash app inicializálása
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='treemap', figure=fig),
    html.Div(id='output')
])

# Callback a kattintási eseményhez
@app.callback(
    Output('output', 'children'),
    [Input('treemap', 'clickData')]
)
def display_click_data(clickData):
    if clickData:
        stock_label = clickData['points'][0]['label']  # Az elem neve
        link = df[df["Stock_Label"] == stock_label]["Link"].values[0]  # Megfelelő link kinyerése
        webbrowser.open_new_tab(link)  # Link megnyitása új böngészőablakban
        return f"Megnyitott link: {link}"
    return "Kattints egy részvényre!"

# Dash szerver futtatása
if __name__ == '__main__':
    app.run_server(debug=True)
