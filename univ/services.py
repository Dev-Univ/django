from univ.models import Univ


class UnivService:

    def __init__(self, user):
        self.user = user

    def get_univ(self, univ_id):
        return Univ.objects.get(pk=univ_id)

    def get_all_univs(self):
        return Univ.objects.all()
