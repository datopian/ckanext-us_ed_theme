import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.us_ed_theme import helpers
from ckanext.us_ed_theme import actions
from ckan.lib.plugins import DefaultTranslation


class Us_Ed_ThemePlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IRoutes, inherit=True)

    # ITemplateHelpers

    def get_helpers(self):
        return {
            'us_ed_get_groups': helpers.get_groups,
            'us_ed_get_recently_updated_datasets':
                helpers.get_recently_updated_datasets,
            'us_ed_get_most_popular_datasets':
                helpers.get_most_popular_datasets
        }

    # IActions

    def get_actions(self):
        return {
            'us_ed_theme_prepare_zip_resources': actions.prepare_zip_resources,
        }

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'us_ed_theme')

    # IRoutes

    def before_map(self, map):
        map.connect(
            'download_zip',
            '/download/zip/{zip_id}',
            controller='ckanext.us_ed_theme.controller:DownloadController',
            action='download_zip'
        )

        return map
