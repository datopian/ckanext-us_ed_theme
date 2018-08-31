import ckan.logic as logic
from ckan import model
from ckan.plugins import toolkit
from ckan.common import config

from datetime import datetime

def _get_action(action, context_dict, data_dict):
    return toolkit.get_action(action)(context_dict, data_dict)


def get_groups():
    # Helper used on the homepage for showing groups

    data_dict = {
        'all_fields': True
    }
    groups = _get_action('group_list', {}, data_dict)

    return groups


def get_recently_updated_datasets(limit=5):
    '''
     Returns recent created or updated datasets.
    :param limit: Limit of the datasets to be returned. Default is 5.
    :type limit: integer
    :returns: a list of recently created or updated datasets
    :rtype: list
    '''
    try:
        pkg_search_results = toolkit.get_action('package_search')(data_dict={
            'sort': 'metadata_modified desc',
            'rows': limit,
        })['results']

    except toolkit.ValidationError, search.SearchError:
        return []
    else:
        pkgs = []
        for pkg in pkg_search_results:
            package = toolkit.get_action('package_show')(
                data_dict={'id': pkg['id']})
            modified = datetime.strptime(
                package['metadata_modified'].split('T')[0], '%Y-%m-%d')
            package['days_ago_modified'] = ((datetime.now() - modified).days)
            pkgs.append(package)
        return pkgs


def get_most_popular_datasets(limit=5):
    '''
     Returns most popular datasets based on total views.
    :param limit: Limit of the datasets to be returned. Default is 5.
    :type limit: integer
    :returns: a list of most popular datasets
    :rtype: list
    '''
    data = pkg_search_results = toolkit.get_action('package_search')(data_dict={
            'sort': 'views_total desc',
            'rows': limit,
        })['results']

    return data
