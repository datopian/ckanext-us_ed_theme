import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckanext.us_ed_theme import helpers

class Us_Ed_ThemePlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    # ITemplateHelpers

    def get_helpers(self):
        return {
            'us_ed_get_groups': helpers.get_groups,
        }

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'us_ed_theme')
