from flask import Response, Blueprint, send_file, redirect, render_template,jsonify, request, send_from_directory,flash,url_for
from App.controllers import get_current_user
from datetime import datetime,timedelta
report_views = Blueprint('report_views', __name__, template_folder='../templates')
from fpdf import FPDF
from flask_login import login_required

from App.controllers import (
    get_all_lockers,
    get_all_transactions,
    get_all_keys,
    get_revenue,
    get_rents_range,
    get_rents_returned_range,
)

@report_views.route('/report', methods=['GET'])
@login_required
def report_page():
    return render_template('report.html')

@report_views.route('/report/transactions', methods=['GET'])
@login_required
def transactions_report():
    transactions_data=get_all_transactions()
    pdf = FPDF()
    pdf.add_page()
    page_width = pdf.w - 2 * pdf.l_margin
    pdf.set_font('Times','B',14.0) 
    pdf.cell(page_width, 0.0, 'Transaction Data', align='C')
    pdf.ln(10)
    pdf.set_font('Courier', '', 12)
    pdf.ln(10)
    pdf.set_font('Courier', '', 12)
    col_width = page_width/4
    pdf.ln(1)	
    th = pdf.font_size
    for row in transactions_data:
        pdf.cell(col_width, th, str(row['id']), border=1)
        pdf.cell(col_width, th, row['rent_id'], border=1)
        pdf.cell(col_width, th, row['currency'], border=1)
        pdf.cell(col_width, th, row['transaction_date'], border=1)
        pdf.cell(col_width, th, row['amount'], border=1)
        pdf.cell(col_width, th, row['description'], border=1)
        pdf.cell(col_width, th, row['receipt_number'], border=1)
        pdf.cell(col_width, th, str(row['type']), border=1)
        pdf.cell(col_width, th, "", border=1)
        pdf.ln(th)

    flash("success")
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=transaction_report.pdf'})


@report_views.route('/report/lockers', methods=['GET'])
@login_required
def lockers_report():
    lockers_data=get_all_lockers()
    pdf = FPDF()
    pdf.add_page()
    page_width = pdf.w - 2 * pdf.l_margin
    pdf.set_font('Times','B',14.0) 
    pdf.cell(page_width, 0.0, 'Locker Data', align='C')
    pdf.ln(10)
    pdf.set_font('Courier', '', 12)
    col_width = page_width/4
    pdf.ln(1)	
    th = pdf.font_size
    for row in lockers_data:
        pdf.cell(col_width, th, row['locker_code'], border=1)
        pdf.cell(col_width, th, row['locker_type'], border=1)
        pdf.cell(col_width, th, row['status'], border=1)
        pdf.cell(col_width, th, row['key'], border=1)
        pdf.cell(col_width, th, str(row['area']), border=1)
        pdf.cell(col_width, th, "", border=1)
        pdf.ln(th)
    flash("success")
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=locker_report.pdf'})


@report_views.route('/report/keys', methods=['GET'])
@login_required
def keys_report():
    keys_data=get_all_keys(6,1)
    pdf = FPDF()
    pdf.add_page()
    page_width = pdf.w - 2 * pdf.l_margin
    pdf.set_font('Times','B',14.0) 
    pdf.cell(page_width, 0.0, 'Transaction Data', align='C')
    pdf.ln(10)
    pdf.set_font('Courier', '', 12)
    col_width = page_width/4
    pdf.ln(1)	
    th = pdf.font_size
    for row in keys_data:
        pdf.cell(col_width, th, row['key_id'], border=1)
        pdf.cell(col_width, th, str(row['masterkey_id']), border=1)
        pdf.cell(col_width, th, row['key_status'], border=1)
        pdf.cell(col_width, th, row['date_added'], border=1)
        pdf.cell(col_width, th, "", border=1)
        pdf.ln(th)

    flash("success")


    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=key_report.pdf'})

@report_views.route('/api/report/monthly', methods=['GET'])
@login_required
def get_daily_report():
    date = datetime.now()
    if  [1,3,5,7,8,10,12].index(date.month):
        e_days = 31
    elif [4,6,9,11].index(date.month):
        e_days = 30
    else:
        import calendar
        if calendar.isleap(date.year):
            e_days = 29
        else:
            e_days = 28
    start_date = datetime(date.year,date.month,1)
    end_date = datetime(date.year,date.month,e_days)
    revenue = get_revenue(start_date,end_date)
    rents = get_rents_range(start_date,end_date)
    returns = get_rents_returned_range(start_date,end_date)
    data = {
        "start_date": datetime.strftime(start_date,'%Y-%m-%d'),
        "end_date":datetime.strftime(end_date,'%Y-%m-%d'),
        "revenue":revenue,
        "num_of_rents":rents,
        "num_of_returns":returns
    }
    
    return jsonify(data),200