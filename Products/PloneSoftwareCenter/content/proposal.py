"""
$Id: PSCImprovementProposal.py 24697 2006-06-10 22:01:35Z optilude $
"""

from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content.base import ATCTMixin
from Products.Archetypes.atapi import *
from Products.CMFCore import permissions
from zope.interface import implements
import transaction

from Products.PloneSoftwareCenter import PSCMessageFactory as _
from Products.PloneSoftwareCenter.config import PROJECTNAME
from Products.PloneSoftwareCenter.interfaces import IImprovementProposalContent

TEXT_TYPES = (
    'text/structured',
    'text/x-rst',
    'text/html',
    'text/plain',
)


PSCImprovementProposalSchema = OrderedBaseFolderSchema.copy() + Schema((

    StringField(
        name='id',
        required=0,
        searchable=1,
        mode='r', # Leave the custom auto-generated ID
        widget=StringWidget(
            label=_("label_proposal_number", default="Proposal number"),
            description=_("help_proposal_number", default="The number of the Improvement Proposal."),
            i18n_domain="plonesoftwarecenter",
        ),
    ),

    StringField(
        name='proposer',
        required=1,
        searchable=1,
        index=":schema",
        widget=StringWidget(
            label=_("label_proposal_proposer", default="Proposer"),
            description=_("help_proposal_proposer", default="The person proposing this improvement."),
            i18n_domain="plonesoftwarecenter",
        ),
    ),

    StringField(
        name='seconder',
        required=0,
        searchable=1,
        index=":schema",
        widget=StringWidget(
            label=_("label_proposal_seconder", default="Seconder"),
            description=_("help_proposal_seconder", default="The person seconding this improvement."),
            i18n_domain="plonesoftwarecenter",
        ),
    ),

    StringField(
        name='description',
        required=1,
        searchable=1,
        accessor="Description",
        storage=MetadataStorage(),
        widget=TextAreaWidget(
            label=_("label_proposal_summary", default="Proposal Summary"),
            description=_("help_proposal_summary", default="A short summary of the proposal."),
            i18n_domain="plonesoftwarecenter",
            rows=5,
        ),
    ),

    LinesField(
        name='proposalTypes',
        multiValued=1,
        required=1,
        vocabulary='getProposalTypesVocab',
        enforceVocabulary=1,
        index='KeywordIndex:schema',
        widget=MultiSelectionWidget(
            label=_("label_proposal_types", default="Proposal types"),
            description=_("help_proposal_types", default="The type of proposal this is."),
            i18n_domain = "plonesoftwarecenter",
        ),
    ),

    TextField(
        name='motivation',
        required=1,
        searchable=1,
        default_content_type='text/plain',
        default_output_type='text/html',
        allowable_content_types=TEXT_TYPES,
        widget=RichWidget(
            label=_("label_proposal_motivation", default="Motivation"),
            description=_("help_proposal_motivation", default="Why does this proposal exist and what problem does it solve?"),
            i18n_domain="plonesoftwarecenter",
            rows=20,
        ),
    ),

    TextField(
        name='proposal',
        required=1,
        searchable=1,
        default_content_type='text/plain',
        default_output_type='text/html',
        allowable_content_types=TEXT_TYPES,
        widget=RichWidget(
            label=_("label_proposal", default="Proposal"),
            description=_("help_proposal", default="What needs to be done?"),
            i18n_domain="plonesoftwarecenter",
            rows=20,
        ),
    ),

    TextField(
        name='definitions',
        required=0,
        searchable=1,
        default_content_type='text/plain',
        default_output_type='text/html',
        allowable_content_types=TEXT_TYPES,
        widget=RichWidget(
            label=_("label_proposal_definitions", default="Definitions"),
            description=_("help_proposal_definitions", default="If you have any definitions for your proposal, please include them here."),
            i18n_domain="plonesoftwarecenter",
            rows=5,
        ),
    ),

    TextField(
        name='assumptions',
        searchable=1,
        default_content_type='text/plain',
        default_output_type='text/html',
        allowable_content_types=TEXT_TYPES,
        widget=RichWidget(
            label=_("label_proposal_assumptions", default="Assumptions"),
            description=_("help_proposal_assumptions", default="Key assumptions made. What is being covered by and what is intentionally left out of the scope of the proposal."),
            i18n_domain="plonesoftwarecenter",
            rows=20,
        ),
    ),

    TextField(
        name='implementation',
        required=0,
        searchable=1,
        default_content_type='text/plain',
        default_output_type='text/html',
        allowable_content_types=TEXT_TYPES,
        widget=RichWidget(
            label=_("label_proposal_implementation", default="Implementation"),
            description=_("help_proposal_implementation", default="How should it be done?"),
            i18n_domain="plonesoftwarecenter",
            rows=20,
        ),
    ),

    TextField(
        name='deliverables',
        required=0,
        searchable=1,
        default_content_type='text/plain',
        default_output_type='text/html',
        allowable_content_types=TEXT_TYPES,
        widget=RichWidget(
            label=_("label_proposal_deliverables", default="Deliverables"),
            description=_("help_proposal_deliverables", default="What code and documentation needs to be produced? Standard items: Unit tests, localization, and documentation"),
            rows=10,
            i18n_domain="plonesoftwarecenter",
        ),
    ),

    TextField(
        name='risks',
        required=0,
        searchable=1,
        default_content_type='text/plain',
        default_output_type='text/html',
        allowable_content_types=TEXT_TYPES,
        widget=RichWidget(
            label=_("label_proposal_risks", default="Risks"),
            description=_("help_proposal_risks", default="What are the risks of implementing this proposal? What incompatibilities can it cause?"),
            i18n_domain="plonesoftwarecenter",
            rows=10,
        ),
    ),

    TextField(
        name='timeline',
        required=0,
        searchable=1,
        default_content_type='text/plain',
        default_output_type='text/html',
        allowable_content_types=TEXT_TYPES,
        widget=RichWidget(
            label=_("label_proposal_progress_log", default="Progress log"),
            description=_("help_proposal_progress_log", default="Enter progress updates here as work is done."),
            i18n_domain="plonesoftwarecenter",
            rows=10,
        ),
    ),

    TextField(
        name='participants',
        searchable=1,
        #validators=('isTidyHtml',),
        default_content_type='text/plain',
        default_output_type='text/html',
        allowable_content_types=TEXT_TYPES,
        widget=RichWidget(
            label=_("label_proposal_participants", default="Participants"),
            description=_("help_proposal_participants", default="The people already identified for the implementation, if applicable."),
            i18n_domain="plonesoftwarecenter",
            rows=5,
        ),
    ),

    StringField(
        name='branch',
        validators=('isURL',),
        mutator='setBranch',
        widget=StringWidget(
            label=_("label_proposal_branch_name_url", default="Branch name/URL"),
            description=_("help_proposal_branch_name_url", default="The URL for the branch development is done on, if applicable."),
            i18n_domain="plonesoftwarecenter",
        ),
    ),

    ComputedField(
        name='relatedReleases',
        expression="sorted([o.getId() for o in context.getBackReferences('RelatedFeatures') ])",
        index=':schema',
        widget=StringWidget(
            label=_("label_proposal_related_releases", default="Related Releases"),
#            description=_(u"help_proposal_related_releases", default=u""),
            modes=('view',),
        ),
    ),

))


class PSCImprovementProposal(ATCTMixin, OrderedBaseFolder):
    """What used to be a PLIP."""

    implements(IImprovementProposalContent)

    archetype_name = 'Improvement Proposal'
    immediate_view = default_view = 'psc_improvements_view'
    suppl_views = ()
    content_icon = 'improvementproposal_icon.gif'
    schema = PSCImprovementProposalSchema
    global_allow = False
    filter_content_types = True
    allowed_content_types = ('Image', 'File')
    _at_rename_after_creation = True

    security = ClassSecurityInfo()

    typeDescMsgId = 'description_edit_improvementproposal'
    typeDescription = ('An Improvement Proposal contains plans for '
                       'feature additions or improvements. Improvement '
                       'proposals may be associated with a planned or '
                       'implemented release, to generate a roadmap. '
                       'Only Motivation and Proposal are required fields, '
                       'but you are encouraged to fill in the other fields '
                       'that are relevant. You can also add files and images '
                       'inside an improvement proposal, if needed.')

    security.declareProtected(permissions.ModifyPortalContent,
                                'setBranch')
    def setBranch(self, value):
        """Set the repository branch, stripping off whitespace and any trailing
        slashes
        """
        value = value.strip()
        while value.endswith('/'):
            value = value[:-1]
        self.getField('branch').set(self, value)

    def getProposalTypesVocab(self):
        """Get the allowed proposal types."""
        list = DisplayList()
        # Acquire the types
        types = self.aq_inner.aq_parent.getProposalTypes()
        for type in types:
            list.add(type, type)
        return list

    def _renameAfterCreation(self, check_auto_id=False):
        """Get sequentially numbered ids"""
        parent = self.aq_inner.aq_parent
        maxId = 0
        for id in parent.objectIds():
            try:
                intId = int(id)
                maxId = max(maxId, intId)
            except (TypeError, ValueError):
                pass
        newId = str(maxId + 1)
        # Can't rename without a subtransaction commit when using
        # portal_factory!
        transaction.savepoint(optimistic=True)
        self.setId(newId)

registerType(PSCImprovementProposal, PROJECTNAME)
