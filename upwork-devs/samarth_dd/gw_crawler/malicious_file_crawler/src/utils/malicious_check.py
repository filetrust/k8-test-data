import os

from src.virus_total import Virustotal


class MaliciousCheck:

    allowed_Types = [".doc", ".pdf", ".ppt"]

    @staticmethod
    def check_malicious(file_path):
        vt = Virustotal(os.environ['VIRUS_TOTAL_KEY'])
        response = vt.file_scan(file_path)
        return response

