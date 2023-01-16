from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify,flash,url_for
from views.forms import TransactionAdd,SearchForm
from datetime import datetime
from controllers import (
  add_new_transaction,
  get_student_by_id,
  get_student_current_rental,
  get_all_transactions,
  get_transaction_id
)

transactionLog_views = Blueprint('transactionLog_views', __name__, template_folder='../templates')

@transactionLog_views.route('/transactionLog/sID=<id>', methods=['GET'])
def render_transaction_page_student(id):
    student = get_student_by_id(id)
    if not student:
        flash("Student doesn't exist")
        return redirect(url_for('student_views.render_manage_student'))
    rent = get_student_current_rental(id)

    if not rent:
        flash("Rental doesn't exist")
        return redirect(url_for('student_views.render_manage_student'))

    form = TransactionAdd()

    form.rent_id.data = rent.id
    form.amount.data = rent.amount_owed

    return render_template('transactionLog.html', form = form)

@transactionLog_views.route('/transactionLog', methods=['GET'])
def transactionLog_page():
    return render_template('transactionLog.html', transaction = get_all_transactions(),form = TransactionAdd(),search = SearchForm())

@transactionLog_views.route('/transactionLog', methods=['POST'])
def create_new_transaction():
    form = TransactionAdd()
    if form.validate_on_submit:
        
        rent_id = request.form.get('rent_id')
        currency = request.form.get('currency')
        transaction_date = datetime.strptime(request.form.get('transaction_date'),'%Y-%m-%dT%H:%M')
        
        amount = request.form.get('amount')
        description = request.form.get('description')
        t_type =request.form.get('t_type')
        receipt_number = request.form.get('receipt_number')
        
        newTransaction = add_new_transaction (rent_id,currency,transaction_date,amount,description, t_type, receipt_number)
        
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
