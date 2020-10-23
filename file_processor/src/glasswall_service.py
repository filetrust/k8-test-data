import logging
import os

import requests

logger = logging.getLogger("GW: GlasswallService")


class GlasswallService:

    @staticmethod
    def get_file(file, filename):
        file = file + "/" + filename
        try:
            return {"file": (filename, open(file, "rb"))}
        except Exception:
            logger.info(f"unable to get file {file}")
            return False

    @staticmethod
    def rebuild(filename, file, mode):
        files = GlasswallService.get_file(file, filename)
        if not files:
            return None
        output = False
        try:
            rebuild_api = os.environ.get('rebuild_api', None)
            response = requests.post(rebuild_api, files=files, data={'mode': mode})
        except Exception as ex:
            logger.info(str(ex))
        else:
            output = response
            if '"message": "failed"' in str(response.content):
                output = None
        return output
