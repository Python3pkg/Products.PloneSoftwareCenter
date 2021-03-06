"""
$Id: PSCFileLink.py 19225 2006-02-13 05:50:18Z limi $
"""

from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.base import ATCTMixin
from Products.Archetypes.atapi import *
from Products.CMFCore import permissions
from zope.interface import  implements

from Products.PloneSoftwareCenter import PSCMessageFactory as _
from Products.PloneSoftwareCenter.config import PROJECTNAME
from Products.PloneSoftwareCenter.interfaces import IFileLinkContent

PSCFileLinkSchema = BaseSchema.copy() + Schema((

    TextField(
        name='title',
        default='',
        searchable=1,
        accessor="Title",
        widget=StringWidget(
            label=_("label_file_title", default="File Description"),
            description=_("help_file_title_filelink", default="File description. Normally something like 'Product Package', 'Product Installer', or 'Product Bundle' - if you have several packages in one archive. The uploaded filename will not be changed."),
            i18n_domain="plonesoftwarecenter",
        ),
    ),

    StringField(
        name='platform',
        required=1,
        searchable=0,
        vocabulary='getPlatformVocab',
        widget=SelectionWidget(
            label=_("label_file_platform", default="Platform"),
            description=_("help_file_platform", default="List of platforms available for selection"),
            i18n_domain="plonesoftwarecenter",
        ),
    ),

    StringField(
        name='externalURL',
        required=1,
        validators=('isURL',),
        widget=StringWidget(
            label=_("label_file_ext_url", default="URL for externally hosted file"),
            description=_("help_file_ext_url", default="Please enter the URL where the file is hosted."),
            i18n_domain="plonesoftwarecenter",
        ),
    ),

    StringField(
        name='externalFileSize',
        required=0,
        widget=StringWidget(
            label=_("label_file_ext_size", default="File size"),
            description=_("help_file_ext_size", default="Please enter the size of the externally hosted file, if known. Include the notation kB or MB."),
            i18n_domain="plonesoftwarecenter",
        ),
    ),

))

class PSCFileLink(ATCTMixin, BaseContent):
    """Contains a link to a downloadable file for a Release."""

    implements(IFileLinkContent)

    archetype_name = 'Externally Hosted File'
    immediate_view = default_view = 'psc_file_view'
    suppls_views = ()
    content_icon = 'link_icon.gif'
    schema = PSCFileLinkSchema
    _at_rename_after_creation = True
    global_allow = False

    security = ClassSecurityInfo()

    security.declareProtected(permissions.View, 'getPlatformVocab')
    def getPlatformVocab(self):
        """Get the platforms available for selection via acquisition from
        the top-level projects container.
        """
        return DisplayList([(item, item) for item in \
                            self.getAvailablePlatforms()])

registerType(PSCFileLink, PROJECTNAME)
