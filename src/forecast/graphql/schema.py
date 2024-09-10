import strawberry

from strawberry.fastapi import GraphQLRouter

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"
    @strawberry.field
    def bye(self) -> str:
        return "Goodbye"


schema = strawberry.Schema(Query)
graphql_app = GraphQLRouter(schema)
