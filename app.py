import dash
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc

# Drink menu
MENU = {
    "Coffee": 3.00,
    "Tea": 2.50,
    "Water": 1.50,
    "Soda": 2.00,
    "Beer": 4.00
}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "POS System"

app.layout = dbc.Container([
    
    html.H2("Cash Register", className="text-center my-3"),

    # Store cart in memory
    dcc.Store(id="cart-store", data=[]),

    html.H4("Select Drinks"),

    dbc.Row([
        dbc.Col(
            dbc.Button(
                f"{drink} - ${price:.2f}",
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

    html.H3("Total: $0.00", id="total-display", className="mt-3"),

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


# Update cart display + total
@app.callback(
    Output("cart-display", "children"),
    Output("total-display", "children"),
    Input("cart-store", "data")
)
def update_display(cart):
    if not cart:
        return "Cart is empty", "Total: $0.00"

    items = []
    total = 0

    for item in cart:
        price = MENU[item]
        total += price
        items.append(html.Div(f"{item} - ${price:.2f}"))

    return items, f"Total: ${total:.2f}"

server = app.server

if __name__ == "__main__":
    app.run(debug=True)