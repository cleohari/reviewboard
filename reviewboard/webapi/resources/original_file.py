from django.core.exceptions import ObjectDoesNotExist
from djblets.webapi.errors import DOES_NOT_EXIST

from reviewboard.webapi.resources import resources
from reviewboard.webapi.resources.base_original_file import \
    BaseOriginalFileResource


class OriginalFileResource(BaseOriginalFileResource):
    """Provides the unpatched file corresponding to a file diff."""
    added_in = '2.0'

    name = 'original_file'

    def get_filediff(self, request, *args, **kwargs):
        """Returns the FileDiff, or an error, for the given parameters."""
        review_request_resource = resources.review_request

        try:
            review_request = review_request_resource.get_object(
                request, *args, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST

        if not review_request_resource.has_access_permissions(request,
                                                              review_request):
            return self.get_no_access_error(request)

        try:
            return resources.filediff.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            return DOES_NOT_EXIST


original_file_resource = OriginalFileResource()
