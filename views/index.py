from flask import Blueprint, redirect, render_template, request, send_from_directory,flash,url_for

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')

@index_views.app_errorhandler(400)
def render_not_found(e):
    flash('Page not found')
    print(e)
    return redirect(url_for("locker_views.manage_lockers"))


@index_views.app_errorhandler(500)
def render_not_found(e):
    flash('You did something wrong :(')
    print(e)
    return redirect(url_for("locker_views.manage_lockers"))

@index_views.route('/flaskwebgui-dumb-request-for-middleware-keeping-the-server-online', methods=['GET'])
def empty_function():
    return {},200
