from django.db import transaction

from project.models import TechStack
from team.models import Team, TeamTechStack, Position


class TeamService:

    @transaction.atomic
    def create_team(self, validated_data, user):
        try:
            team = self._create_proejct_with_validated_data(validated_data, user)
            self._create_tech_stacks(team, validated_data.get('tech_stacks', []))
            self._create_positions(team, validated_data.get('positions', []))

            return Team.objects.prefetch_related(
                'tech_stacks__tech_stack',
                'positions'
            ).get(id=team.id)
        except Exception as e:
            raise Exception(f"Failed to create team: {str(e)}")

    @transaction.atomic
    def get_teams(self):
        try:
            return Team.objects.prefetch_related(
                'tech_stacks__tech_stack',
                'positions'
            ).all()
        except Exception as e:
            raise Exception(f"Failed to get teams: {str(e)}")

    @transaction.atomic
    def get_teams_by_user(self, user):
        try:
            return Team.objects.prefetch_related(
                'tech_stacks__tech_stack',
                'positions'
            ).filter(user=user).all()
        except Exception as e:
            raise Exception(f"Failed to get teams by user: {str(e)}")

    def _create_proejct_with_validated_data(self, validated_data, user):
        return Team.objects.create(
            name=validated_data['name'],
            type=validated_data['type'],
            description=validated_data['description'],
            end_date=validated_data['end_date'],
            user=user
        )

    def _create_tech_stacks(self, team, tech_stacks_data):
        if not tech_stacks_data:
            return

        existing_tech_stacks = TechStack.objects.filter(id__in=tech_stacks_data)

        team_tech_stacks = [
            TeamTechStack(
                team=team,
                tech_stack=tech_stack
            ) for tech_stack in existing_tech_stacks
        ]

        TeamTechStack.objects.bulk_create(team_tech_stacks)

    def _create_positions(self, team, positions_data):
        if not positions_data:
            return

        team_positions = [
            Position(
                name=position['name'],
                description=position['description'],
                is_open=position['is_open'],
                team=team
            ) for position in positions_data
        ]

        Position.objects.bulk_create(team_positions)



