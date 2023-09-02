from flask import Flask, redirect, url_for
#from flask_cors import CORS
from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.explorer import ExplorerGraphiQL
from flask import request, jsonify

from config import GRAPHQL_TYPE_DEFINITION
from .queries import query
from .mutations import mutation

app = Flask(__name__)
#CORS(app)

type_defs = load_schema_from_path(GRAPHQL_TYPE_DEFINITION)
schema = make_executable_schema(type_defs, query, mutation)

@app.route('/')
def root_route():
    return redirect(url_for('graphql_playground'))

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    explorer_html = ExplorerGraphiQL().html(None)
    return explorer_html, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()

    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code
