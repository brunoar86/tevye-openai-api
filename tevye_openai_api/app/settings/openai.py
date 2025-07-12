import os


class Vault:

    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.openai_project_id = os.getenv('PROJECT_ID')
        self.openai_organization_id = os.getenv('ORGANIZATION_ID')

    def key(self):
        return self.openai_api_key

    def id(self):
        return self.openai_project_id

    def organization(self):
        return self.openai_organization_id


project = Vault()
