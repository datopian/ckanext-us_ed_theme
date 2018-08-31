from ckan.plugins import toolkit
import uuid
from ckanext.us_ed_theme import helpers
import zipfile
import os
from ckan.controllers.admin import get_sysadmins
import requests
from logging import getLogger


SUPPORTED_RESOURCE_MIMETYPES = [
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'application/x-msdownload',
    'application/msword',
    'application/vnd.google-earth.kml+xml',
    'application/vnd.ms-excel',
    'application/msexcel',
    'application/x-msexcel',
    'application/x-ms-excel',
    'application/x-excel',
    'application/x-dos_ms_excel',
    'application/xls',
    'application/x-xls',
    'wcs',
    'application/x-javascript',
    'application/x-msaccess',
    'application/netcdf',
    'text/tab-separated-values',
    'text/x-perl',
    'application/vnd.google-earth.kmz+xml',
    'application/vnd.google-earth.kmz',
    'application/owl+xml',
    'application/x-n3',
    'application/zip',
    'application/gzip',
    'application/x-gzip',
    'application/x-qgis',
    'application/vnd.oasis.opendocument.spreadsheet',
    'application/vnd.oasis.opendocument.text',
    'application/json',
    'image/x-ms-bmp',
    'application/rar',
    'image/tiff',
    'application/vnd.oasis.opendocument.database',
    'text/plain',
    'application/x-director',
    'application/vnd.oasis.opendocument.formula',
    'application/vnd.oasis.opendocument.graphics',
    'application/xml',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/octet-stream',
    'application/xslt+xml',
    'image/svg+xml',
    'application/vnd.ms-powerpoint',
    'application/vnd.oasis.opendocument.presentation',
    'image/jpeg',
    'application/sparql-results+xml',
    'image/gif',
    'application/rdf+xml',
    'application/pdf',
    'text/csv',
    'application/vnd.oasis.opendocument.chart',
    'application/atom+xml',
    'application/x-tar',
    'image/png',
    'application/rss+xml',
    'application/geo+json'
]

log = getLogger(__name__)


@toolkit.side_effect_free
def prepare_zip_resources(context, data_dict):
    """Creates zip archive and stores it under CKAN's storage path.

    :param resources: a list of ids of the resources
    :type resources: list

    :return: a dictionary containing the zip_id of the created archive
    :rtype: dict
    """
    file_name = uuid.uuid4().hex + '.{ext}'.format(ext='zip')
    file_path = helpers.get_storage_path_for('temp-us_ed_theme') + '/' + file_name
    resourceArchived = False
    package_id = None

    try:
        resource_ids = data_dict.get('resources')
        with zipfile.ZipFile(file_path, 'w') as zip:
            for resource_id in resource_ids:
                data_dict = {'id': resource_id}
                resource = toolkit.get_action('resource_show')({}, data_dict)

                url = resource.get('url')
                if resource['url_type'] == 'upload':
                    name = url.split('/')[-1]
                else:
                    name = resource['name']
                    if os.path.splitext(name)[-1] == '':
                        _format = resource['format']
                        if _format:
                            name += '.{ext}'.format(ext=_format.lower())

                if package_id is None:
                    package_id = resource['package_id']

                headers = {'Authorization': get_sysadmins()[0].apikey}
                try:
                    r = requests.get(url, headers=headers)
                except Exception:
                    continue

                content_type = r.headers['Content-Type'].split(';')[0]

                if content_type in SUPPORTED_RESOURCE_MIMETYPES:
                    resourceArchived = True
                    zip.writestr(name, r.content)
    except Exception, ex:
        log.error('An error occured while preparing zip archive. Error: %s' % ex)
        raise

    zip_id = file_name
    try:
        package = toolkit.get_action('package_show')({}, {'id': package_id})
        package_name = package['name']

        zip_id += '::{name}'.format(name=package_name)
    except:
        pass

    if resourceArchived:
        return {'zip_id': zip_id}

    os.remove(file_path)

    return {'zip_id': None}
