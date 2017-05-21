from Products.CMFCore.utils import getToolByName
from io import StringIO
from Products.contentmigration.walker import CustomQueryWalker
from Products.contentmigration.migrator import BaseInlineMigrator
from zope.annotation.interfaces import IAnnotations
import transaction


class RatingsMigrator(BaseInlineMigrator):
    """
    Migrate PSC Projects from the content ratings product to the twothumbs product
    """

    src_portal_type = src_meta_type = 'PSCProject'

    def migrate_ratings(self):

        """
        contentratings and twothumbs both use annotations. Just want to move
        one to another. Here we say anything >= 3 rating is a thumbs up
        """

        from cioppino.twothumbs import rate as thumbrate

        transaction.begin()
        item = self.obj
        annotations = IAnnotations(item)
        if annotations:
            if 'contentratings.userrating.psc_stars' in annotations:
                ratings = annotations['contentratings.userrating.psc_stars'].all_user_ratings()
                annotations = thumbrate.setupAnnotations(item)
                for rating in ratings:

                    if rating >= 3.0:
                        thumbrate.loveIt(item, rating.userid)
                    else:
                        thumbrate.hateIt(item, rating.userid)

        # we need to reindex th object anyways
        item.reindexObject()
        transaction.commit()


def migrate(self):
    out = StringIO()
    print("Starting ratings migration", file=out)

    portal_url = getToolByName(self, 'portal_url')
    portal = portal_url.getPortalObject()

    # Migrate release count variable
    walker = CustomQueryWalker(portal, RatingsMigrator,
                               query = {'portal_type': 'PSCProject'})
    transaction.savepoint(optimistic=True)
    print("Switching from contentratings to twothumbs..", file=out)
    walker.go(out=out)
    print(walker.getOutput(), file=out)

    print("Migration finished", file=out)
