class Team:
    def __init__(self, name):
        self.name = name

class League:
    def __init__(self):
        self.teams = []

    def add_team(self, team):
        if not any(existing_team.name == team.name for existing_team in self.teams):
            self.teams.append(team)
            return True
        return False


    def update_team(self, old_name, new_name):
        for team in self.teams:
            if team.name == old_name:
                team.name =  new_name
                return True
        return False

    def delete_team(self, name):
        self.teams = [team for team in self.teams if team.name != name]

    def get_teams(self):
        return [team.name for team in self.teams]

    def generate_random_teams(self, amount=1000):
        for i in range(amount):
            self.add_team(Team(f"Team_{i}"))

