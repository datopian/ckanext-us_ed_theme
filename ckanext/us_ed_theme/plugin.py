import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.us_ed_theme import helpers
from ckan.lib.plugins import DefaultTranslation


class Us_Ed_ThemePlugin(plugins.SingletonPlugin, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.ITranslation)

    # ITemplateHelpers

    def get_helpers(self):
        return {
            'us_ed_get_groups': helpers.get_groups,
            'us_ed_get_recently_updated_datasets':
                helpers.get_recently_updated_datasets,
        }

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'us_ed_theme')
