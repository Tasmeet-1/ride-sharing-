class RollbackManager:
    def __init__(self):
        self.stack = []
    def save_state(self, snapshot):
        self.stack.append(snapshot)
    def rollback(self):
        if not self.stack:
            return None
        return self.stack.pop()
