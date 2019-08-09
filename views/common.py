import flask

blueprint = flask.Blueprint('common', __name__, template_folder='common')

@blueprint.route('')
