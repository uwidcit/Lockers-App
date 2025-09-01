from flask import Response, Blueprint, send_file, redirect, render_template,jsonify, request, send_from_directory,flash,url_for
from App.controllers import get_current_user
from datetime import datetime,timedelta
report_views = Blueprint('report_views', __name__, template_folder='../templates')
from fpdf import FPDF
from flask_login import login_required
from App.views.admin import admin_only

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
@admin_only
def report_page():
    return render_template('report.html')

@report_views.route('/api/report/pdf', methods=['POST'])
@login_required
@admin_only
def transactions_report():
    json_start_date = request.json.get('start_date')
    json_end_date = request.json.get('end_date')
    try:
        start_date = datetime.strptime(json_start_date,'%Y-%m-%d')
        end_date = datetime.strptime(json_end_date,'%Y-%m-%d')
        start_date = start_date.replace(hour=0,minute=0,second=0)
        end_date = end_date.replace(hour=23,minute=59,second=59)
        if start_date > end_date:
            return jsonify({"Message": "Invalid date entered"}),400
    except Exception as e:
        return jsonify({"Message": str(e)}),400
    cumalative_amount = 0
    cumalative_length = 0
    cumalative_late = 0
    cumalative_additional = 0
    if start_date.month < 8:
        semester_start = start_date.year-1
    else:
        semester_start = start_date.year
    semester_end = end_date.year

    rents = get_rents_range(start_date,end_date)
    returns = get_rents_returned_range(start_date,end_date)
    page_title = 'Student Activity Center (SAC) Locker Rentals Report: Academic Year '+str(semester_start)+'/'+str(semester_end)
    period = "Period: "+datetime.strftime(start_date,'%Y-%m-%d')+" to "+datetime.strftime(end_date,'%Y-%m-%d')
    pdf = FPDF()
    pdf.add_page()
    page_width = pdf.w - 2 * pdf.l_margin
    pg_width = 38.1
    pdf.set_font('Times','B',14.0) 
    pdf.cell(page_width, 0.0, page_title, align='C',ln=1)
    pdf.ln(10)
    pdf.set_font('Times', '', 12)
    pdf.cell(page_width, 0.0, period, align='C',ln=1)
    pdf.ln(10)
    pdf.set_draw_color(0, 0, 0)
    pdf.set_fill_color(255, 255, 255)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(page_width, 9, "Active", align='C',ln=1, border=1)
    for rent in rents:
        pdf.cell(page_width,9,rent.capitalize(),1,1,"L",1)
        pdf.cell(pg_width,9,"",True,0)
        pdf.cell(pg_width,9,"No. of Rents",True,0)
        pdf.cell(pg_width,9,"Revenue",True,0)
        pdf.cell(pg_width,9,"Late Fees",True,0)
        pdf.cell(pg_width,9,"Additional Fees",True,1)
        for r in rents[rent]:
            pdf.cell(pg_width,9,r,True,0)
            pdf.cell(pg_width,9,str(rents[rent][r]["length"]),True,0)
            pdf.cell(pg_width,9,"$"+str("{:.2f}".format(rents[rent][r]["amount"])),True,0)
            pdf.cell(pg_width,9,"$"+str("{:.2f}".format(rents[rent][r]["late_fees"])),True,0)
            pdf.cell(pg_width,9,"$"+str("{:.2f}".format(rents[rent][r]["additional_fees"])),True,1)
        cumalative_length = cumalative_length + rents[rent]["Total"]["length"]
        cumalative_amount = cumalative_amount + rents[rent]["Total"]["amount"]
        cumalative_late = cumalative_late + rents[rent]["Total"]["late_fees"]
        cumalative_additional = cumalative_additional+ rents[rent]["Total"]["additional_fees"]
        pdf.cell(page_width,9,"",1,1,"L",1)
    pdf.cell(page_width, 9, "Completed", align='C',ln=1, border=1)
    for rent in returns:
        pdf.cell(page_width,9,rent.capitalize(),1,1,"L",1)
        pdf.cell(pg_width,9,"",True,0)
        pdf.cell(pg_width,9,"No. of Rents",True,0)
        pdf.cell(pg_width,9,"Revenue",True,0)
        pdf.cell(pg_width,9,"Late Fees",True,0)
        pdf.cell(pg_width,9,"Additional Fees",True,1)
        for r in returns[rent]:
            pdf.cell(pg_width,9,r,True,0)
            pdf.cell(pg_width,9,str(returns[rent][r]["length"]),True,0)
            pdf.cell(pg_width,9,"$"+str("{:.2f}".format(returns[rent][r]["amount"])),True,0)
            pdf.cell(pg_width,9,"$"+str("{:.2f}".format(returns[rent][r]["late_fees"])),True,0)
            pdf.cell(pg_width,9,"$"+str("{:.2f}".format(returns[rent][r]["additional_fees"])),True,1)
        cumalative_length = cumalative_length + returns[rent]["Total"]["length"]
        cumalative_amount = cumalative_amount + returns[rent]["Total"]["amount"]
        cumalative_late = cumalative_late + returns[rent]["Total"]["late_fees"]
        cumalative_additional = cumalative_additional + returns[rent]["Total"]["additional_fees"]
        pdf.cell(page_width,9,"",1,1,"L",1)
    pdf.cell(pg_width,9,"Cumalative Total: ",True,0)
    pdf.cell(pg_width,9,str(cumalative_length),True,0)
    pdf.cell(pg_width,9,"$"+str("{:.2f}".format(cumalative_amount)),True,0)
    pdf.cell(pg_width,9,"$"+str("{:.2f}".format(cumalative_late)),True,0)
    pdf.cell(pg_width,9,"$"+str("{:.2f}".format(cumalative_additional)),True,0)
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=transaction_report.pdf'})

@report_views.route('/api/report/period', methods=['POST'])
@login_required
def get_period_report():
    json_start_date = request.json.get('start_date')
    json_end_date = request.json.get('end_date')
    try:
        start_date = datetime.strptime(json_start_date,'%Y-%m-%d')
        end_date = datetime.strptime(json_end_date,'%Y-%m-%d')
        start_date = start_date.replace(hour=0,minute=0,second=0)
        end_date = end_date.replace(hour=23,minute=59,second=59)
        if start_date > end_date:
            return jsonify({"Message": "Invalid date entered"}),400
    except Exception as e:
        return jsonify({"Message": str(e)}),400
    rents = get_rents_range(start_date,end_date)
    returns = get_rents_returned_range(start_date,end_date)
    data = {
        "start_date": datetime.strftime(start_date,'%Y-%m-%d'),
        "end_date":datetime.strftime(end_date,'%Y-%m-%d'),
        "rents": rents,
        "returns":returns
    }
    
    
    return jsonify(data),200