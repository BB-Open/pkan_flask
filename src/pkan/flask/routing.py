from flask import send_file, request
from pkan.flask.websocket import app, DB_MANAGER


@app.route('/download')
def return_files_tut():
    params = {}
    # id empty means full export
    params['id'] = request.args.get('id', default=None, type=str)
    params['format'] = request.args.get('format', default='rdf/xml', type=str)
    params['type'] = request.args.get('type', default='tree', type=str)
    # ignore on type tree, use on type graph
    params['count'] = request.args.get('count', default='3', type=int)
    file_path, file_name, file, mimetype = DB_MANAGER.get_download_file(params)
    try:
        return send_file(file_path, attachment_filename=file_name, mimetype=mimetype)
    except Exception as e:
        return str(e)
