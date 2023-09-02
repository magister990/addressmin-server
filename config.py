import os

SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", f"sqlite:///{os.getcwd()}/addressmin.db")

GRAPHQL_TYPE_DEFINITION = f"{os.getcwd()}/schema.graphql"
