from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify,flash,url_for
from App.views.forms import TransactionAdd,SearchForm
from flask_login import login_required
from datetime import datetime
from App.controllers import (
  add_new_transaction,
  get_student_by_id,
  get_area_choices,
  get_student_current_rental,
  get_all_transactions,
  get_num_transactions_page,
  get_transactions_by_offset,
  get_transaction_id,
  search_transaction
)

transactionLog_views = Blueprint('transactionLog_views', __name__, template_folder='../templates')
page_size = 6

@transactionLog_views.route('/transactionLog/sID=<id>', methods=['GET'])
@login_required
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

@transactionLog_views.route('/transactionLog', methods=['POST'])
@login_required
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

        if t_type == "CREDIT":
            if amount > 0:
                amount = amount * - 1
        else:
            if amount < 0:
                amount = amount * -1

        newTransaction = add_new_transaction (rent_id,currency,transaction_date,amount,description, t_type, receipt_number)
        
        if not newTransaction:
            flash('Error adding transaction')
            return redirect(url_for('.manage_transaction'))
        flash('Success')
        return redirect(url_for('.manage_transaction'))

@transactionLog_views.route('/transactionLog/all',methods=['GET'])
def return_all_transactions():
    return jsonify(get_all_transactions()),200

@transactionLog_views.route('/transactionLog/<id>', methods=['GET'])
@login_required
def get_transaction(id):
    transaction = get_transaction_id(id)

    if not transaction:
        return jsonify({"Message": "Transaction not found"}),404
    return jsonify(transaction.toJSON()),200

@transactionLog_views.route('/transactionLog', methods=['GET'])
@login_required
def manage_transaction():
    num_pages = get_num_transactions_page(page_size)
    transaction_data = get_transactions_by_offset(page_size, 1)
    previous = 1
    next = previous + 1

    return render_template('transactionLog.html', transaction_data = transaction_data, form = TransactionAdd(), search=SearchForm(),searchMode=False, num_pages= num_pages,current_page=1, next=next, previous= previous)

@transactionLog_views.route('/transactionLog/page/<offset>', methods=['GET'])
@login_required
def manage_transaction_pages_multi(offset):
    offset = int(offset)
    num_pages = get_num_transactions_page(page_size)
    transaction_data = get_transactions_by_offset(page_size, offset)

    if offset - 1 <=0:
        previous = 1
        offset = 1
    else:
        previous = offset - 1
    if offset + 1 >= num_pages:
        next = num_pages
    else:
        next = offset + 1
    return render_template('transactionLog.html', transaction_data = transaction_data, form = TransactionAdd(), search=SearchForm(),searchMode=False, num_pages= num_pages,current_page=1, next=next, previous= previous)

@transactionLog_views.route('/transactionLog/search/', methods=['GET'])
@login_required
def search_transaction_page():
    form = SearchForm()
    if form.validate_on_submit:
        query = request.args.get('search_query')
        transaction_data = search_transaction(query,page_size, 1)
        if transaction_data:
            previous = 1
            next = previous + 1
            form = TransactionAdd()
            return render_template('transactionLog.html', transaction_data = transaction_data['data'], form = TransactionAdd(), search=SearchForm(),searchMode=False, num_pages= transaction_data['num_pages'],current_page=1, next=next, previous= previous)
        return redirect(url_for('.manage_transaction'))

@transactionLog_views.route('/transactionLog/search/page/<offset>', methods=['GET'])
@login_required
def search_transaction_page_multi(offset):
    offset = int(offset)
    form = SearchForm()
    if form.validate_on_submit:
        query = request.args.get('search_query')
        transaction_data = search_transaction(query,page_size, offset)
        if transaction_data:
         num_pages = transaction_data['num_pages']
         if offset - 1 <= 0:
                previous = 1
                offset = 1
        else:
            previous = offset - 1
        if offset + 1 >= num_pages:
            next = num_pages
        else:
            next = offset + 1
        form = TransactionAdd()
        return render_template('transactionLog.html', transaction_data = transaction_data['data'], form = TransactionAdd(), search=SearchForm(),searchMode=False, num_pages= transaction_data['num_pages'],current_page=offset, next=next, previous= previous)
    return redirect(url_for('.manage_transaction'))

@transactionLog_views.route('/api/transactionLog', methods=['POST'])
@login_required
def create_new_transaction_api():
        rent_id = request.json.get('rent_id')
        currency = request.json.get('currency')
        transaction_date = datetime.strptime(request.json.get('transaction_date'),'%Y-%m-%dT%H:%M')
        amount = request.json.get('amount')
        description = request.json.get('description')
        t_type =request.json.get('t_type')
        receipt_number = request.json.get('receipt_number')
        
        newTransaction = add_new_transaction (rent_id,currency,transaction_date,amount,description, t_type, receipt_number)
        
        if not newTransaction:
            return jsonify({"error": "Rental not created"}),400
        
        return jsonify(newTransaction.toJSON()),201