"""
$Id: PSCReleaseFolder.py 24400 2006-06-04 22:38:43Z optilude $
"""

from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.base import ATCTMixin
from Products.Archetypes.atapi import *
from Products.CMFCore import permissions
from zope.interface import implements
import transaction

from Products.PloneSoftwareCenter import PSCMessageFactory as _
from Products.PloneSoftwareCenter import config
from Products.PloneSoftwareCenter.interfaces import IReleaseFolderContent

PSCReleaseFolderSchema = OrderedBaseFolderSchema.copy() + Schema((

    StringField(
        name='id',
        required=0,
        searchable=1,
        mode='r', # Leave the custom auto-generated ID
        widget=StringWidget (
            label=_("label_releasefolder_short_name", default="Short name"),
            description=_("help_releasefolder_short_name", default="Short name of the container - this should be 'release' to comply with the standards."),
            i18n_domain="plonesoftwarecenter",
        ),
    ),

    StringField(
        name='title',
        default='Releases',
        searchable=1,
        accessor="Title",
        widget=StringWidget(
            label=_("label_releasefolder_title", default="Title"),
            description=_("help_releasefolder_title", default="Enter a title for the container"),
            i18n_domain="plonesoftwarecenter",
        ),
    ),

    StringField(
        name='description',
        default='Existing and upcoming releases for this project.',
        searchable=1,
        accessor="Description",
        widget=TextAreaWidget(
            label=_("label_release_description", default="Description"),
            description=_("help_release_description", default="Enter a description of the container"),
            i18n_domain="plonesoftwarecenter",
        ),
    ),

))

class PSCReleaseFolder(ATCTMixin, OrderedBaseFolder):
    """Folder type for holding releases."""

    implements(IReleaseFolderContent)

    archetype_name = 'Releases Section'
    immediate_view = default_view = 'psc_releasefolder_view'
    content_icon = 'download_icon.gif'
    schema = PSCReleaseFolderSchema

    security = ClassSecurityInfo()

    global_allow = 0
    filter_content_types = 1
    allowed_content_types = ('PSCRelease',)
    _at_rename_after_creation = True

    typeDescMsgId = 'description_edit_releasefolder'
    typeDescription = ('A Releases Section is used to hold software '
                       'releases. It is given a default short name and '
                       'title to ensure that projects are consistent. '
                       'Please do not rename it.')

    def _renameAfterCreation(self, check_auto_id=False):
        parent = self.aq_inner.aq_parent
        if config.RELEASES_ID not in parent.objectIds():
            # Can't rename without a subtransaction commit when using
            # portal_factory!
            transaction.savepoint(optimistic=True)
            self.setId(config.RELEASES_ID)

    security.declareProtected(permissions.View, 'generateUniqueId')
    def generateUniqueId(self, type_name):
        """Override for the .py script in portal_scripts with the same name.

        Gives some default names for contained content types.
        """

        if type_name != 'PSCRelease':
            return self.aq_parent.generateUniqueId(type_name)

        # Generate a fake version number, to signify that the user needs to
        # correct it

        # find the highest-used major version
        ids = self.objectIds()

        def getMajor(i):
            try:
                return int(float(i))
            except ValueError:
                return 0

        def getMinor(i):
            if '.' in i:
                try:
                    return int(float(i[i.find('.')+1:]))
                except ValueError:
                    return 0

        majors, minors = ([getMajor(id) for id in ids],
                          [getMinor(id) for id in ids])

        if majors:
            major = max(majors) or 1
        else:
            major = 1

        if minors:
            minor = max(minors)
        else:
            minor = 0

        while '%s.%s' % (major, minor,) in self.objectIds():
            minor += 1
        return '%s.%s' % (major, minor)

registerType(PSCReleaseFolder, config.PROJECTNAME)
