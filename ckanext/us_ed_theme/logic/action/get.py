from ckan.logic.action import get as get_core
from ckan.plugins import toolkit
import ckan.lib.helpers as h

@toolkit.side_effect_free
def package_show(context, data_dict):
    ''' This action is overriden so that the extra field "theme" is added.
    This is needed because when a dataset is exposed to DCAT it needs this
    field.

    Themes are coming from groups where a dataset is added to. The field
    "theme" exists in group's schema.'''

    groups = package.get_groups(group_type='group')
