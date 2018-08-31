from ckan.plugins import toolkit
import os
from ckanext.us_ed_theme.helpers import get_storage_path_for
from ckan.common import response
from ckan.lib import base


class DownloadController(base.BaseController):
    def download_zip(self, zip_id):
        if not zip_id:
            abort(404, toolkit._('Resource data not found'))
        file_name, package_name = zip_id.split('::')
        file_path = get_storage_path_for('temp-us_ed_theme/' + file_name)

        if not os.path.isfile(file_path):
            abort(404, toolkit._('Resource data not found'))

        if not package_name:
            package_name = 'resources'
        package_name += '.zip'

        with open(file_path, 'r') as f:
            response.write(f.read())

        response.headers['Content-Type'] = 'application/octet-stream'
        response.content_disposition = 'attachment; filename=' + package_name
        os.remove(file_path)
