import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

# Drink menu
MENU = {
    "Coca Cola Zero": 2.5,
    "Coca Cola": 2.5,
    "Ice Tea": 2.5,
    "Fanta": 2.5,
    "Spa Rood": 2.5,
    "Spa Blauw": 2.5,
    "Stella": 2.5,
    "Stella 0.0": 2.5,
    "Duvel": 4.0,
    "Leffe Blond": 4.0,
    "Leffe Bruin": 4.0,
    "Witte Wijn": 4.0,
    "Rode Wijn": 4.0,
    "Cava": 4.0,
    "Fles": 20.0,
    "Sportzot": 4.0,
    "Olmi Gember": 4.0,
    "Olmi Beetroot": 4.0,
    "Koffie": 2.5,
    "Thee": 2.5
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "POS System"

app.layout = dbc.Container([

    html.H2("Cash Register", className="text-center my-3"),

    # Store cart
    dcc.Store(id="cart-store", data=[]),

    html.H4("Select Drinks"),

    dbc.Row([
        dbc.Col(
            dbc.Button(
                f"{drink} - €{price:.2f}",
                id={"type": "drink-btn", "index": drink},
                color="primary",
                className="m-1 w-100",
                n_clicks=0
            ),
            xs=6, sm=4, md=3
        )
        for drink, price in MENU.items()
    ]),

    html.Hr(),

    html.H4("Cart"),

    html.Div(id="cart-display"),

    html.H3("Total: €0.00 (0 x €0.50)", id="total-display", className="mt-3"),

    dbc.Button("Clear Cart", id="clear-btn", color="danger", className="mt-2 w-100")

], fluid=True)


# Add drink to cart
@app.callback(
    Output("cart-store", "data"),
    Input({"type": "drink-btn", "index": dash.ALL}, "n_clicks"),
    State("cart-store", "data"),
    prevent_initial_call=True
)
def add_to_cart(n_clicks_list, cart):
    ctx = dash.callback_context
    if not ctx.triggered:
        return cart

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    drink = eval(button_id)["index"]

    cart.append(drink)
    return cart


# Clear cart
@app.callback(
    Output("cart-store", "data", allow_duplicate=True),
    Input("clear-btn", "n_clicks"),
    prevent_initial_call=True
)
def clear_cart(n):
    return []


# Update cart display + total + 50c counter
@app.callback(
    Output("cart-display", "children"),
    Output("total-display", "children"),
    Input("cart-store", "data")
)
def update_display(cart):

    if not cart:
        return "Cart is empty", "Total: €0.00 (0 x €0.50)"

    items = []
    total = 0

    for item in cart:
        price = MENU[item]
        total += price
        items.append(html.Div(f"{item} - €{price:.2f}"))

    # count 50 cent units
    num_50c = int(total / 0.5)

    return items, f"Total: €{total:.2f} ({num_50c} x €0.50)"


server = app.server

if __name__ == "__main__":
    app.run(debug=True)
