from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify,flash,url_for
from views.forms import TransactionAdd
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
    form = TransactionAdd()
    if form.validate_on_submit:
        
        rent_id = request.form.get('rent_id')
        currency = request.form.get('currency')
        transaction_date = request.form.get('transaction_date')
        amount = request.form.get('amount')
        description = request.form.get('description')
        t_type =request.form.get('t_type')
        
        newTransaction = add_new_transaction (rent_id,currency,transaction_date,amount,description, t_type)
        
        if not newTransaction:
            flash('Error adding transaction')
            return redirect(url_for('.transactionLog_page'))
        flash('Success')
        return redirect(url_for('.transactionLog_page'))

@transactionLog_views.route('/transactionLog/all',methods=['GET'])
def return_all_transactions():
    return jsonify(get_all_transactions()),200

@transactionLog_views.route('/transactionLog/<id>', methods=['GET'])
def get_transaction(id):
    transaction = get_transaction_id(id)

    if not transaction:
        return jsonify({"Message": "Transaction not found"}),404
    return jsonify(transaction.toJSON()),200
