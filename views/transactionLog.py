from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify
from forms import TransactionAdd
from controllers import (
  add_new_transaction,
  get_all_transactions,
  get_transaction_id
)

transactionLog_views = Blueprint('transactionLog_views', __name__, template_folder='../templates')

@transactionLog_views.route('/transactionLog', methods=['GET'])
def render_transaction_page():
    return render_template('release_transaction.html', form = TransactionAdd())

@transactionLog_views.route('/transactionLog/view', methods=['GET'])
def transactionLog_page():
    return render_template('transactionLog.html', transaction = get_all_transactions())

@transactionLog_views.route('/transactionLog', methods=['POST'])
def create_new_transaction():
    rent_id = request.json.get('rent_id')
    currency = request.json.get('currency')
    transaction_date = request.json.get('transaction_date')
    amount = request.json.get('amount')
    description = request.json.get('description')
    t_type =request.json.get('t_type')
    

    newTransaction = add_new_transaction (rent_id,currency,transaction_date,amount,description, t_type)

    if not newTransaction:
        return jsonify({"Message": "Error adding transaction"}), 400
    
    return jsonify(newTransaction.toJSON()),201

@transactionLog_views.route('/transactionLog/all',methods=['GET'])
def return_all_transactions():
    return jsonify(get_all_transactions()),200

@transactionLog_views.route('/transactionLog/<id>', methods=['GET'])
def get_transaction(id):
    transaction = get_transaction_id(id)

    if not transaction:
        return jsonify({"Message": "Transaction not found"}),404
    return jsonify(transaction.toJSON()),200
