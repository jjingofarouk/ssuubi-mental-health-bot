class Response:
    def __init__(self, message, analysis):
        self.message = message
        self.analysis = analysis
    
    def to_dict(self):
        return {
            "message": self.message,
            "analysis": self.analysis,
            "priority": "normal"
        }