from flask import Response, Blueprint, send_file, redirect, render_template,jsonify, request, send_from_directory,flash,url_for
from controllers import get_current_user
report_views = Blueprint('report_views', __name__, template_folder='../templates')
from fpdf import FPDF

from controllers import (
    get_all_lockers,
    get_all_transactions,
    get_all_keys,
)

@report_views.route('/report', methods=['GET'])
def report_page():
    return render_template('report.html')

@report_views.route('/report/transactions', methods=['GET'])
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
