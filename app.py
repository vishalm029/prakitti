from flask import Flask, render_template, redirect, session

app = Flask(__name__)
app.secret_key = "prakritti_secret_key"

# PRODUCTS (3 SOAPS ONLY)
products = [
    {
        "id": 1,
        "name": "Aloe Vera Soap",
        "price": 120,
        "image": "aloevera.jpeg",
        "desc": "Hydrating herbal soap for soft & glowing skin."
    },
    {
        "id": 2,
        "name": "Haldi & Chandan Soap",
        "price": 120,
        "image": "haldi_chandan.jpeg",
        "desc": "Traditional ayurvedic blend for radiant skin."
    },
    {
        "id": 3,
        "name": "Neem Tulsi Soap",
        "price": 120,
        "image": "neem.jpeg",
        "desc": "Antibacterial soap for healthy & clear skin."
    }
]


# HOME
@app.route("/")
def home():
    return render_template("index.html", products=products)


# ADD TO CART
@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    session.setdefault("cart", []).append(id)
    session.modified = True
    return redirect("/cart")


# CART PAGE
@app.route("/cart")
def cart():
    cart_items = []
    total = 0

    for pid in session.get("cart", []):
        for p in products:
            if p["id"] == pid:
                cart_items.append(p)
                total += p["price"]

    return render_template("cart.html", cart=cart_items, total=total)


# CHECKOUT (ORDER REQUEST PAGE)
@app.route("/checkout")
def checkout():
    cart_ids = session.get("cart", [])
    if not cart_ids:
        return redirect("/cart")

    total = sum(p["price"] for p in products if p["id"] in cart_ids)

    return render_template("checkout.html", total=total)


# SUCCESS PAGE
@app.route("/success")
def success():
    session.pop("cart", None)
    return render_template("success.html")


if __name__ == "__main__":
    app.run(debug=True)
