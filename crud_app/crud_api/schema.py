import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from graphql.error.base import GraphQLError
from crud_app.crud_api.models import Actor, Movie, Employee, Project, Sector


class ActorType(DjangoObjectType):
    class Meta:
        model = Actor

class MovieType(DjangoObjectType):
    class Meta:
        model = Movie

class EmployeeType(DjangoObjectType):
    class Meta:
        model = Employee

class ProjectType(DjangoObjectType):
    class Meta:
        model = Project

class SectorType(DjangoObjectType):
    class Meta:
        model = Sector



class Query(ObjectType):
    actor = graphene.Field(ActorType, id = graphene.Int())
    movie = graphene.Field(MovieType, id = graphene.Int())
    employee = graphene.Field(EmployeeType, id = graphene.UUID())
    project = graphene.Field(ProjectType, id = graphene.UUID())
    sector = graphene.Field(SectorType, id = graphene.UUID())

    actors = graphene.List(ActorType)
    movies = graphene.List(MovieType)
    employees = graphene.List(EmployeeType)
    project = graphene.List(ProjectType)
    sector = graphene.List(SectorType)

    def resolve_actor(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Actor.objects.get(pk = id)

        return None

    def resolve_movie(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Movie.objects.get(pk = id)

        return None

    def resolve_employee(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Employee.objects.get(pk = id)

        return None

    def resolve_project(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Project.objects.get(pk = id)

        return None

    def resolve_sector(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Sector.objects.get(pk = id)

        return None



    def resolve_actors(self, info, **kwargs):
        return Actor.objects.all()

    def resolve_movies(self, info, **kwargs):
        return Movie.objects.all()

    def resolve_employees(self, info, **kwargs):
        return Employee.objects.all()

    def resolve_projects(self, info, **kwargs):
        return Project.objects.all()

    def resolve_sectors(self, info, **kwargs):
        return Sector.objects.all()




class ActorInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()

class MovieInput(graphene.InputObjectType):
    id = graphene.ID()
    title_name = graphene.String()
    actors = graphene.List(ActorInput)
    year = graphene.Int()

class EmployeeInput(graphene.InputObjectType):
    first_name = graphene.String()
    middle_name = graphene.String()
    last_name = graphene.String()
    gender = graphene.String()
    address = graphene.String()
    salary = graphene.Decimal()

class ProjectInput(graphene.InputObjectType):
    name = graphene.String()
    location = graphene.String()
    employees = graphene.List(EmployeeInput)

class SectorInput(graphene.InputObjectType):
    name = graphene.String()
    location = graphene.String()





class CreateActor(graphene.Mutation):
    class Arguments:
        input = ActorInput(required = True)

    ok = graphene.Boolean()
    actor = graphene.Field(ActorType)

    @staticmethod
    def mutate(root, info, input = None):
        ok = True
        actor_instance = Actor(name = input.name)
        actor_instance.save()
        return CreateActor(ok = ok, actor = actor_instance)


class CreateMovie(graphene.Mutation):
    class Arguments:
        input = MovieInput(required = True)

    ok = graphene.Boolean()
    movie = graphene.Field(MovieType)

    @staticmethod
    def mutate(root, info, input = None):
        print("input",input)
        ok = True
        actors = []
        for actor_input in input.actors:
            actor = Actor.objects.filter(id = actor_input.id).first()
            print("actor",actors)
            if actor:
                actors.append(actor)
                print("actor",actors)

            else:
                raise GraphQLError("Actor not Found")
        movie_instance = None
        for actor in actors:
            movie_instance = Movie.objects.create(
                title_name = input.title_name,
                year = input.year
            )
            movie_instance.actors.add(Actor.objects.filter(id = actor_input.id).first())
        return CreateMovie(ok = ok, movie = movie_instance)

class CreateEmployee(graphene.Mutation):
    class Arguments:
        input = EmployeeInput(required = True)

    ok = graphene.Boolean()
    employee = graphene.Field(EmployeeType)

    @staticmethod
    def mutate(root, info, input = None):
        print('input : ', input)
        ok = True
        employee_instance = Employee(
            first_name = input.first_name,
            middle_name = input.middle_name,
            last_name = input.last_name,
            gender = input.gender,
            address = input.address,
            salary = input.salary
        )
        employee_instance.save()
        return CreateEmployee(ok = ok, employee = employee_instance)

class CreateProject(graphene.Mutation):
    class Arguments:
        input = ProjectInput(required = True)

    ok = graphene.Boolean()
    project = graphene.Field(ProjectType)

    @staticmethod
    def mutate(root, info, input = None):
        ok = True
        employees = []
        for employee_input in input.employees:
            employee = Employee.objects.filter(id = employee_input.id).first()
            if employee:
                employees.append(employee)
            else:
                raise GraphQLError("Employee not Found")
        project_instance = None
        for employee in employees:
            project_instance = Project.objects.create(
                name = input.name,
                location = input.location
            )
            project_instance.employees.add(Employee.objects.filter(id = employee_input.id).first())
        return CreateProject(ok = ok, project = project_instance)

class CreateSector(graphene.Mutation):
    class Arguments:
        input = SectorInput(required = True)

    ok = graphene.Boolean()
    sector = graphene.Field(SectorType)

    @staticmethod
    def mutate(root, info, input = None):
        ok = True
        sector_instance = Sector(
            name  = input.name,
            location = input.location
        )
        sector_instance.save()
        return CreateSector(ok = ok, sector = sector_instance)




class UpdateActor(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required = True)
        input = ActorInput(required = True)

    ok = graphene.Boolean()
    actor = graphene.Field(ActorType)

    @staticmethod
    def mutate(root, info, id, input = None):
        ok = False
        actor_instance = Actor.objects.get(pk = id)
        if actor_instance:
            ok = True
            actor_instance.name = input.name
            actor_instance.save()
            return UpdateActor(ok = ok, actor = actor_instance)
        return UpdateActor(ok = ok, actor = None)


class UpdateMovie(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required = True)
        input = MovieInput(required = True)

    ok = graphene.Boolean()
    movie = graphene.Field(MovieType)

    @staticmethod
    def mutate(root, info, id, input = None):
        ok = False
        movie_instance = Movie.objects.get(pk = id)
        if movie_instance:
            ok = True
            actors = []
            for actor_input in input.actors:
                actor = Actor.objects.get(pk = actor_input.id)
                if actor is None:
                    return UpdateMovie(ok = False, movie = None)
                actors.append(actor)
            movie_instance.title = input.title
            movie_instance.year = input.year
            movie_instance.save()
            movie_instance.actors.set(actors)
            return UpdateMovie(ok = ok, movie = movie_instance)
        return UpdateMovie(ok = ok, movie = None)

class UpdateEmployee(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required = True)
        input = ActorInput(required = True)

    ok = graphene.Boolean()
    employee = graphene.Field(EmployeeType)

    @staticmethod
    def mutate(root, info, id, input = None):
        ok = False
        employee_instance = Employee.objects.get(pk = id)
        if employee_instance:
            ok = True
            employee_instance.salary = input.salary
            employee_instance.save()
            return UpdateEmployee(ok = ok, employee = employee_instance)
        return UpdateEmployee(ok = ok, employee = None)

class UpdateProject(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required = True)
        input = ProjectInput(required = True)

    ok = graphene.Boolean()
    project = graphene.Field(ProjectType)

    @staticmethod
    def mutate(root, info, id, input = None):
        ok = False
        project_instance = Project.objects.get(pk = id)
        if project_instance:
            ok = True
            employees = []
            for employee_input in input.employees:
                employee = Employee.objects.get(pk = employee_input.id)
                if employee is None:
                    return UpdateProject(ok = False, project = None)
                employees.append(employee)
                project_instance.name = input.name
                project_instance.location = input.location
                project_instance.save()
                project_instance.employees.set(employees)
            return UpdateProject(ok = ok, project = project_instance)
        return UpdateProject(ok = ok, project = None)

class UpdateSector(graphene.Mutation):
    class Arguments:
        id = graphene.UUID(required  = True)
        input = SectorInput(required = True)

    ok = graphene.Boolean()
    sector = graphene.Field(SectorType)

    @staticmethod
    def mutate(root, info, id, input = None):
        ok = False
        sector_instance = Sector.objects.get(pk = id)
        if sector_instance:
            ok = True
            sector_instance.name = input.name
            sector_instance.location = input.location
            sector_instance.save()
            return UpdateSector(ok = ok, sector = sector_instance)
        return UpdateSector(ok = ok, sector = None)


class Mutation(graphene.ObjectType):
    create_actor = CreateActor.Field()
    create_movie = CreateMovie.Field()
    create_employee = CreateEmployee.Field()
    create_project = CreateProject.Field()
    create_sector = CreateSector.Field()

    update_actor = UpdateActor.Field()
    update_movie = UpdateMovie.Field()
    update_employee = UpdateEmployee.Field()
    update_project = UpdateProject.Field()
    update_sector = UpdateSector.Field()



schema = graphene.Schema(query = Query, mutation = Mutation)