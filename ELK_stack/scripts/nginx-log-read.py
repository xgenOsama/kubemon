import re
import shlex
import pandas as pd
from datetime import datetime
from elasticsearch7 import Elasticsearch
import uuid
es = Elasticsearch("http://localhost:9200")

class Parser:
    IP = 0
    TIME = 3
    TIME_ZONE = 4
    REQUESTED_URL = 5
    STATUS_CODE = 6
    USER_AGENT = 9
    ES_INDEX = "python-nginx-index"

    def parse_line(self, line):
        try:
            line = re.sub(r"[\[\]]", "", line)
            data = shlex.split(line)
            id = uuid.uuid4()
            result = {
                "id": id,
                "ip": data[self.IP],
                "time": data[self.TIME],
                "status_code": data[self.STATUS_CODE],
                "requested_url": data[self.REQUESTED_URL],
                "user_agent": data[self.USER_AGENT],
            }
            print(result)
            print(result['id'])
            self.send_to_es(result)
            return result
        except Exception as e:
            raise e
    def send_to_es(self,data):
        try:
            resp = es.index(index=self.ES_INDEX, id=data['id'], document=data)
        except Exception as e:
            raise e


if __name__ == "__main__":
    parser = Parser()
    LOG_FILE = "nginx.log"
    with open(LOG_FILE, "r") as f:
        log_entries = [parser.parse_line(line) for line in f]

    logs_df = pd.DataFrame(log_entries)
    print(logs_df)