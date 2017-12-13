from django.apps import AppConfig
from material.frontend.apps import ModuleMixin


class PartnerConfig(ModuleMixin, AppConfig):
    name = 'partner'
    icon = '<i class="material-icons">star_border</i>'
