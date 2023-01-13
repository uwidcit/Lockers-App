from flask import Blueprint, redirect, render_template, request, send_from_directory,jsonify,flash,url_for


from controllers import (
    get_all_logs
    )

log_views = Blueprint('log_views', __name__, template_folder='../templates')

@log_views.route('/log', methods=['GET'])
def Log():
    return render_template('log.html', log = get_all_logs())

