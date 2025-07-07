# Import libraries
from flask import Flask, redirect, request, render_template, url_for

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': 200},
    {'id': 3, 'date': '2024-06-07', 'amount': 500},
    {'id': 4, 'date': '2021-06-12', 'amount': 700},
    {'id': 5, 'date': '2025-06-21', 'amount': 800},
    {'id': 6, 'date': '2022-06-30', 'amount': 140}
]

# Read operation


@app.route("/")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)

# Create operation
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == 'POST':
        transaction = {
            'id': len(transactions) + 1,
            'date': request.form['date'],
            'amount': int(request.form['amount'])
        }
        transactions.append(transaction)
        return redirect(url_for("get_transactions"))
    else: 
        return render_template("form.html")


# Update operation
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method == 'POST':
        date = request.form['date']
        amount = int(request.form['amount'])
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date
                transaction['amount'] = amount
                break
        return redirect(url_for("get_transactions"))

    for transaction in transactions:
        if transaction['id'] == transaction_id:
            return render_template("edit.html", transaction=transaction)
    return {"message": "Transaction not found"}, 404


# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)
            break
    return redirect(url_for("get_transactions"))

# search operation
@app.route("/search", methods=["GET", "POST"])
def search(): 
    if request.method == "POST":
        min_amount = request.form["min_amount"]
        max_amount = request.form["max_amount"]
        result = []
        for transaction in transactions:
            if (transaction['amount'] >= int(min_amount) and transaction['amount'] <= int(max_amount)):
                result.append(transaction)
        return render_template("transactions.html", transactions=result)
    else :      
        return render_template("search.html")



# Run the Flask app
if __name__ == "__main__":
    app.run(port=8000, debug=True)
