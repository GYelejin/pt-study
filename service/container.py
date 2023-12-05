from dependency_injector import containers, providers

from service.modules.services import FileStorageService


# class Repositories(containers.DeclarativeContainer):
#     users = providers.Factory(
#         AttacksRepository,
#     )


class Services(containers.DeclarativeContainer):
    # repositories = providers.DependenciesContainer()

    files = providers.Factory(
        FileStorageService,
        # repository=repositories.files
    )


class Application(containers.DeclarativeContainer):
    # repositories = providers.Container(
    #     Repositories,
    # )

    services = providers.Container(
        Services,
        # repositories=repositories
    )
