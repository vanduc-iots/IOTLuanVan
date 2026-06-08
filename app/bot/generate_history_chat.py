from google.genai import types


# {role: roleName, parts = []}
class Chat:
    def __init__(self, contents:list):
        self.contents = contents

    def addContent(self, **kwarg) :
        role = kwarg.get("role") 
        content = kwarg.get("content")

        if self.contents:
            self.contents.append(types.Content(role=role, parts=[]))


        
        
