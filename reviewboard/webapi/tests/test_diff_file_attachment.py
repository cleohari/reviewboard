from djblets.webapi.errors import PERMISSION_DENIED

from reviewboard.webapi.resources import resources
from reviewboard.webapi.tests.base import BaseWebAPITestCase
from reviewboard.webapi.tests.mimetypes import (
    diff_file_attachment_item_mimetype,
    diff_file_attachment_list_mimetype)
from reviewboard.webapi.tests.mixins import BasicTestsMetaclass
from reviewboard.webapi.tests.urls import (get_diff_file_attachment_item_url,
                                           get_diff_file_attachment_list_url)


class ResourceListTests(BaseWebAPITestCase, metaclass=BasicTestsMetaclass):
    """Testing the DiffFileAttachmentResource list APIs."""
    fixtures = ['test_users', 'test_scmtools']
    sample_api_url = 'repositories/<id>/diff-file-attachments/'
    resource = resources.diff_file_attachment

    def compare_item(self, item_rsp, attachment):
        self.assertEqual(item_rsp['id'], attachment.pk)
        self.assertEqual(item_rsp['filename'], attachment.filename)
        self.assertEqual(item_rsp['caption'], attachment.caption)
        self.assertEqual(item_rsp['mimetype'], attachment.mimetype)

    def setup_http_not_allowed_list_test(self, user):
        repository = self.create_repository()

        return get_diff_file_attachment_list_url(repository)

    #
    # HTTP GET tests
    #

    def setup_basic_get_test(self, user, with_local_site, local_site_name,
                             populate_items):
        repository = self.create_repository(with_local_site=with_local_site)

        if populate_items:
            diffset = self.create_diffset(repository=repository)
            filediff = self.create_filediff(diffset)
            items = [self.create_diff_file_attachment(filediff)]
        else:
            items = []

        return (get_diff_file_attachment_list_url(repository, local_site_name),
                diff_file_attachment_list_mimetype,
                items)

    def test_get_with_mimetype(self):
        """Testing the GET repositories/<id>/diff-file-attachments/ API
        with ?mimetype=
        """
        repository = self.create_repository()
        diffset = self.create_diffset(repository=repository)
        filediff = self.create_filediff(diffset)
        attachment = self.create_diff_file_attachment(
            filediff,
            caption='Image',
            orig_filename='image.png',
            mimetype='image/png')
        self.create_diff_file_attachment(
            filediff,
            caption='Text',
            orig_filename='text.txt',
            mimetype='text/plain')

        rsp = self.api_get(
            get_diff_file_attachment_list_url(repository) +
            '?mimetype=image/png',
            expected_mimetype=diff_file_attachment_list_mimetype)
        self.assertEqual(rsp['stat'], 'ok')
        self.assertIn('diff_file_attachments', rsp)

        attachments_rsp = rsp['diff_file_attachments']
        self.assertEqual(len(attachments_rsp), 1)
        attachment_rsp = attachments_rsp[0]
        self.assertEqual(attachment_rsp['id'], attachment.pk)
        self.assertEqual(attachment_rsp['filename'], 'image.png')
        self.assertEqual(attachment_rsp['caption'], 'Image')
        self.assertEqual(attachment_rsp['mimetype'], 'image/png')

    def test_get_with_repository_file_path(self):
        """Testing the GET repositories/<id>/diff-file-attachments/ API
        with ?repository-file-path=
        """
        repository = self.create_repository()
        diffset = self.create_diffset(repository=repository)
        filediff1 = self.create_filediff(diffset,
                                         source_file='/test-file-1.png',
                                         dest_file='/test-file-1.png')
        filediff2 = self.create_filediff(diffset,
                                         source_file='/test-file-2.png',
                                         dest_file='/test-file-2.png')
        attachment = self.create_diff_file_attachment(
            filediff1,
            caption='File 1',
            orig_filename='/test-file-1.png')
        self.create_diff_file_attachment(
            filediff2,
            caption='File 2',
            orig_filename='/test-file-2.png')

        rsp = self.api_get(
            get_diff_file_attachment_list_url(repository) +
            '?repository-file-path=/test-file-1.png',
            expected_mimetype=diff_file_attachment_list_mimetype)
        self.assertEqual(rsp['stat'], 'ok')
        self.assertIn('diff_file_attachments', rsp)

        attachments_rsp = rsp['diff_file_attachments']
        self.assertEqual(len(attachments_rsp), 1)
        attachment_rsp = attachments_rsp[0]
        self.assertEqual(attachment_rsp['id'], attachment.pk)
        self.assertEqual(attachment_rsp['filename'], '/test-file-1.png')
        self.assertEqual(attachment_rsp['caption'], 'File 1')
        self.assertEqual(attachment_rsp['mimetype'], 'image/png')

    def test_get_with_repository_revision(self):
        """Testing the GET repositories/<id>/diff-file-attachments/ API
        with ?repository-revision=
        """
        repository = self.create_repository()
        diffset = self.create_diffset(repository=repository)
        filediff1 = self.create_filediff(diffset,
                                         source_file='/test-file-1.png',
                                         dest_file='/test-file-1.png',
                                         source_revision='4',
                                         dest_detail='5')
        filediff2 = self.create_filediff(diffset,
                                         source_file='/test-file-2.png',
                                         dest_file='/test-file-2.png',
                                         source_revision='9',
                                         dest_detail='10')
        attachment = self.create_diff_file_attachment(
            filediff1,
            caption='File 1',
            orig_filename='/test-file-1.png')
        self.create_diff_file_attachment(
            filediff2,
            caption='File 2',
            orig_filename='/test-file-2.png')

        rsp = self.api_get(
            get_diff_file_attachment_list_url(repository) +
            '?repository-revision=5',
            expected_mimetype=diff_file_attachment_list_mimetype)
        self.assertEqual(rsp['stat'], 'ok')
        self.assertIn('diff_file_attachments', rsp)

        attachments_rsp = rsp['diff_file_attachments']
        self.assertEqual(len(attachments_rsp), 1)
        attachment_rsp = attachments_rsp[0]
        self.assertEqual(attachment_rsp['id'], attachment.pk)
        self.assertEqual(attachment_rsp['filename'], '/test-file-1.png')
        self.assertEqual(attachment_rsp['caption'], 'File 1')
        self.assertEqual(attachment_rsp['mimetype'], 'image/png')


class ResourceItemTests(BaseWebAPITestCase, metaclass=BasicTestsMetaclass):
    """Testing the DiffFileAttachmentResource item APIs."""
    fixtures = ['test_users', 'test_scmtools']
    sample_api_url = 'repositories/<id>/diff-file-attachments/<id>/'
    resource = resources.diff_file_attachment

    def compare_item(self, item_rsp, attachment):
        self.assertEqual(item_rsp['id'], attachment.pk)
        self.assertEqual(item_rsp['filename'], attachment.filename)
        self.assertEqual(item_rsp['caption'], attachment.caption)
        self.assertEqual(item_rsp['mimetype'], attachment.mimetype)

    def setup_http_not_allowed_item_test(self, user):
        repository = self.create_repository()
        diffset = self.create_diffset(repository=repository)
        filediff = self.create_filediff(diffset)
        attachment = self.create_diff_file_attachment(filediff)

        return get_diff_file_attachment_item_url(repository, attachment)

    #
    # HTTP GET tests
    #

    def setup_basic_get_test(self, user, with_local_site, local_site_name):
        repository = self.create_repository(with_local_site=with_local_site)
        diffset = self.create_diffset(repository=repository)
        filediff = self.create_filediff(diffset)
        attachment = self.create_diff_file_attachment(filediff)

        return (get_diff_file_attachment_item_url(attachment, repository,
                                                  local_site_name),
                diff_file_attachment_item_mimetype,
                attachment)

    def test_get_with_invite_only_repo(self):
        """Testing the GET repositories/<id>/diff-file-attachments/<id>/ API
        with access to an invite-only repository
        """
        repository = self.create_repository(public=False)
        repository.users.add(self.user)
        diffset = self.create_diffset(repository=repository)
        filediff = self.create_filediff(diffset)
        attachment = self.create_diff_file_attachment(filediff)

        rsp = self.api_get(
            get_diff_file_attachment_item_url(attachment, repository),
            expected_mimetype=diff_file_attachment_item_mimetype)

        self.assertEqual(rsp['stat'], 'ok')
        self.assertIn('diff_file_attachment', rsp)

        attachment_rsp = rsp['diff_file_attachment']
        self.assertEqual(attachment_rsp['id'], attachment.pk)
        self.assertEqual(attachment_rsp['filename'], attachment.filename)
        self.assertEqual(attachment_rsp['caption'], attachment.caption)
        self.assertEqual(attachment_rsp['mimetype'], attachment.mimetype)

    def test_get_with_invite_only_repo_no_access(self):
        """Testing the GET repositories/<id>/diff-file-attachments/<id>/ API
        without access to an invite-only repository
        """
        repository = self.create_repository(public=False)
        diffset = self.create_diffset(repository=repository)
        filediff = self.create_filediff(diffset)
        attachment = self.create_diff_file_attachment(filediff)

        rsp = self.api_get(
            get_diff_file_attachment_item_url(attachment, repository),
            expected_status=403)

        self.assertEqual(rsp['stat'], 'fail')
        self.assertEqual(rsp['err']['code'], PERMISSION_DENIED.code)
