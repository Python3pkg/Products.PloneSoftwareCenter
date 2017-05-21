"""
$Id: PSCImprovementProposalFolder.py 24400 2006-06-04 22:38:43Z optilude $
"""

from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.base import ATCTMixin
from Products.Archetypes.atapi import *
from zope.interface import implements
import transaction

from Products.PloneSoftwareCenter import PSCMessageFactory as _
from Products.PloneSoftwareCenter.config import PROJECTNAME, IMPROVEMENTS_ID
from Products.PloneSoftwareCenter.interfaces import IImprovementProposalFolderContent

PSCImprovementProposalFolderSchema = OrderedBaseFolderSchema.copy() + Schema((

    StringField(
        name='id',
        required=0,
        searchable=1,
        mode='r', # Leave the custom auto-generated ID
        widget=StringWidget (
            label=_("label_proposalfolder_short_name", default="Short name"),
            description=_("help_proposalfolder_short_name", default="Short name of the container - this should be 'roadmap' to comply with the standards."),
            i18n_domain="plonesoftwarecenter",
        ),
    ),

    StringField(
        name='title',
        default='Roadmap',
        searchable=1,
        accessor="Title",
        widget=StringWidget(
            label=_("label_proposalfolder_title", default="Title"),
            description=_("help_proposalfolder_title", default="Enter a title for the container"),
            i18n_domain="plonesoftwarecenter",
        ),
    ),

    StringField(
        name='description',
        default='Improvement proposals which will be considered for this project',
        searchable=1,
        accessor="Description",
        widget=TextAreaWidget(
            label=_("label_proposalfolder_description", default="Description"),
            description=_("help_proposalfolder_description", default="Enter a description of the container"),
            i18n_domain="plonesoftwarecenter",
        ),
    ),

    LinesField(
        name='proposalTypes',
        multiValued=1,
        required=1,
        default=['User interface', 'Architecture'],
        widget=LinesWidget(
            label=_("label_roadmap_types", default="Roadmap proposal types"),
            description=_("help_roadmap_types", default="You will have a roadmap available in your project, and you can add categories of enhancement specifications below."),
            i18n_domain="plonesoftwarecenter",
        ),
    ),

))

class PSCImprovementProposalFolder(ATCTMixin, BaseBTreeFolder):
    """A proposal container has proposals, and a view for the listing."""

    implements(IImprovementProposalFolderContent)

    content_icon = 'improvementproposal_icon.gif'
    archetype_name = 'Roadmap Section'
    immediate_view = default_view = 'psc_roadmap'
    suppl_views = ()
    schema = PSCImprovementProposalFolderSchema

    global_allow = False
    filter_content_types = True
    allowed_content_types = ('PSCImprovementProposal',)
    _at_rename_after_creation = True

    security = ClassSecurityInfo()

    typeDescMsgId = 'description_edit_improvementproposalcontainer'
    typeDescription = ('A roadmap section contains improvement '
                       'proposals for the project.')

    def _renameAfterCreation(self, check_auto_id=False):
        parent = self.aq_inner.aq_parent
        if IMPROVEMENTS_ID not in parent.objectIds():
            # Can't rename without a subtransaction commit when using
            # portal_factory!
            transaction.savepoint(optimistic=True)
            self.setId(IMPROVEMENTS_ID)

registerType(PSCImprovementProposalFolder, PROJECTNAME)
