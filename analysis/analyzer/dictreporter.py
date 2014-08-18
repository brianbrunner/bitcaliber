from pylint.interfaces import IReporter
from pylint.reporters import BaseReporter

class DictReporter(BaseReporter):

    __implements__ = IReporter
    name = 'dict'
    extension = 'dict'

    def add_message(self, msg_id, location, msg):
        self.msgs.append({
            "msg_id": msg_id,
            "location": {
                "filepath": location[0],
                "module": location[1],
                "method": location[2],
                "line":  location[3],
                "column": location[4]
            },
            "msg": msg
        })

    def display_results(self, sect):
        pass
