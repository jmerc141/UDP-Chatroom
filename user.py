class User:
    def __init__(self, name, client):
        self.username = name
        self.client = client

    def __str__(self):
        return self.username + ' ' + str(self.client)

    def __eq__(self, other):
        return self.client == other.client

    def __hash__(self):
        return id(self)
