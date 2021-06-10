import graphene
import crud_app.crud_api.schema

class Query(crud_app.crud_api.schema.Query, graphene.ObjectType):
    pass

class Mutation(crud_app.crud_api.schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query = Query, mutation = Mutation)
