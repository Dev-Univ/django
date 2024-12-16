from django.db import transaction

from univ.models import Univ


class UnivService:

    def __init__(self, user):
        self.user = user

    @transaction.atomic
    def get_univ(self, univ_id):
        return Univ.objects.get(pk=univ_id)

    @transaction.atomic
    def get_all_univs(self):
        return Univ.objects.all()
