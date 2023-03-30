from flask import Blueprint, redirect, render_template,jsonify, request, send_from_directory,flash,url_for
from controllers import get_current_user
report_views = Blueprint('report_views', __name__, template_folder='../templates')
from fpdf import FPDF

from controllers import (
    get_all_lockers,
    get_all_transactions,

)

@report_views.route('/report', methods=['GET'])
def report_page():
    return render_template('report.html')

@report_views.route('/report/transactions', methods=['GET'])
def transaction_report():
    transaction_data=get_all_transactions()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 16)
    for log in transaction_data:
        pdf.cell(w=0, h=10, txt=log, ln=1, align='L')
    pdf.output(f'./transaction_report.pdf', 'F')
    flash("success")
    return render_template('report.html')
