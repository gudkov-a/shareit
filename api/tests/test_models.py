# -*- coding: utf-8 -*-

from django.test import TestCase

from api.models import Entry


class TestEntryMethods(TestCase):

    def setUp(self):
        for i in range(1, 11):
            Entry.objects.create(**{'url': 'https://google.com/', 'desc': 'Test {0}'.format(i)})

    def test_retrieving_entries(self):
        latest = Entry.get_last_four()
        ids = [i.pk for i in latest]
        self.assertEqual(ids, [7, 8, 9, 10])

        previous = Entry.get_previous_entries(ids[0])
        previous_ids = [i.pk for i in previous]
        self.assertEqual(previous_ids, [3, 4, 5, 6])

        next_entries = Entry.get_next_entries(previous_ids[-1])
        next_ids = [i.pk for i in next_entries]
        self.assertEqual(next_ids, [7, 8, 9, 10])

        next_entries = Entry.get_next_entries(next_ids[-1])
        next_ids = [i.pk for i in next_entries]
        self.assertEqual(next_ids, [1, 2, 3, 4])

        previous = Entry.get_previous_entries(1)
        previous_ids = [i.pk for i in previous]
        self.assertEqual(previous_ids, [7, 8, 9, 10])

        # Remove all except first and try to retrieve last four
        Entry.objects.all().exclude(pk=1).delete()
        entries = Entry.get_last_four()
        self.assertEqual(len(entries), 1)
