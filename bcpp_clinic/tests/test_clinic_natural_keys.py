from django.test import TestCase, tag

from edc_sync.test_mixins import SyncTestSerializerMixin


class TestNaturalKey(SyncTestSerializerMixin, TestCase):

    @tag('natural_key')
    def test_natural_key_attrs(self):
        self.sync_test_natural_key_attr('bcpp_clinic')

    @tag('natural_key')
    def test_get_by_natural_key_attr(self):
        self.sync_test_get_by_natural_key_attr('bcpp_clinic')
