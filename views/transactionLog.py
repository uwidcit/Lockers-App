from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify,flash,url_for
from views.forms import TransactionAdd,SearchForm
from datetime import datetime
from controllers import (
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
            return redirect(url_for('.manage_transaction'))
        flash('Success')
        return redirect(url_for('.manage_transaction'))

@transactionLog_views.route('/transactionLog/all',methods=['GET'])
def return_all_transactions():
    return jsonify(get_all_transactions()),200

@transactionLog_views.route('/transactionLog/<id>', methods=['GET'])
def get_transaction(id):
    transaction = get_transaction_id(id)

    if not transaction:
        return jsonify({"Message": "Transaction not found"}),404
    return jsonify(transaction.toJSON()),200

@transactionLog_views.route('/transactionLog', methods=['GET'])
def manage_transaction():
    num_pages = get_num_transactions_page(7)
    transaction_data = get_transactions_by_offset(7, 1)
    previous = 1
    next = previous + 1
    form = TransactionAdd()

    return render_template('transactionLog.html', transaction_data = transaction_data, form = TransactionAdd(), search=SearchForm(),searchMode=False, num_pages= num_pages,current_page=1, next=next, previous= previous)

@transactionLog_views.route('/transactionLog/page/<offset>', methods=['GET'])
def manage_transaction_pages_multi(offset):
    offset = int(offset)
    num_pages = get_num_transactions_page(7)
    transaction_data = get_transactions_by_offset(7, offset)

    if offset - 1 <=0:
        previous = 1
        offset = 1
    else:
        previous = offset - 1
    if offset + 1 >= num_pages:
        next = num_pages
    else:
        next = offset + 1
        form = TransactionAdd()
        return render_template('transactionLog.html', transaction_data = transaction_data, form = TransactionAdd(), search=SearchForm(),searchMode=False, num_pages= num_pages,current_page=1, next=next, previous= previous)

@transactionLog_views.route('/transactionLog/search/', methods=['GET'])
def search_transaction_page():
    form = SearchForm()
    if form.validate_on_submit:
        query = request.args.get('search_query')
        transaction_data = search_transaction(query,7, 1)
        if transaction_data:
            previous = 1
            next = previous + 1
            form = TransactionAdd()
            return render_template('transactionLog.html', transaction_data = transaction_data['data'], form = TransactionAdd(), search=SearchForm(),searchMode=False, num_pages= transaction_data['num_pages'],current_page=1, next=next, previous= previous)
        return redirect(url_for('.manage_transaction'))

@transactionLog_views.route('/transactionLog/search/page/<offset>', methods=['GET'])
def search_transaction_page_multi(offset):
    offset = int(offset)
    form = SearchForm()
    if form.validate_on_submit:
        query = request.args.get('search_query')
        transaction_data = search_transaction(query,7, offset)
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
