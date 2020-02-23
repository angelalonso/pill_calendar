import collections
import pytest
import pill_calendar as pc

class TestPillCalendar:
    @classmethod
    def setup_class(cls):
        pass


    def test_loadCalendar(self):
        ''' Test that we properly load data from CSV
        '''
        cal_file = './test_files/Calendar.csv'
        data = pc.loadCalendar(cal_file)
        expected_data = [{'event_id': 'aaaaaaaaaaaaaaaaaaaaaaaaaa',
                'description': 'Sintrom Amount: 2',
                'end_datetime': '2013-07-07T20:15:00Z',
                'start_datetime': '2013-07-07T18:45:00Z',
                'summary': 'Sintrom Amount: 2'},
            {'event_id': 'bbbbbbbbbbbbbbbbbbbbbbbbbb',
                'description': 'Sintrom Amount: 1',
                'end_datetime': '2013-07-06T20:15:00Z',
                'start_datetime': '2013-07-06T18:45:00Z',
                'summary': 'Sintrom Amount: 1'},
            {'event_id': 'cccccccccccccccccccccccccc',
                'description': 'Blood Level: 2.2',
                'end_datetime': '2013-07-07T10:00:00Z',
                'start_datetime': '2013-07-07T09:15:00Z',
                'summary': 'Blood Level: 2.2'},
            {'event_id': 'dddddddddddddddddddddddddd',
                'description': 'Test Blood',
                'end_datetime': '2013-07-14T10:00:00Z',
                'start_datetime': '2013-07-14T09:15:00Z',
                'summary': 'Test Blood'}]

        assert data == expected_data


    def test_getEntries(self):
        ''' Test that we properly load data from CSV
        '''
        cal_file = './test_files/Calendar.csv'
        data = pc.getEntries(pc.loadCalendar(cal_file), 'Pills')
        expected_data = [{'event_id': 'aaaaaaaaaaaaaaaaaaaaaaaaaa',
                'description': 'Sintrom Amount: 2',
                'end_datetime': '2013-07-07T20:15:00Z',
                'start_datetime': '2013-07-07T18:45:00Z',
                'summary': 'Sintrom Amount: 2'},
            {'event_id': 'bbbbbbbbbbbbbbbbbbbbbbbbbb',
                'description': 'Sintrom Amount: 1',
                'end_datetime': '2013-07-06T20:15:00Z',
                'start_datetime': '2013-07-06T18:45:00Z',
                'summary': 'Sintrom Amount: 1'}]

        assert data == expected_data

        data = pc.getEntries(pc.loadCalendar(cal_file), 'Blood Level')
        expected_data = [{'event_id': 'cccccccccccccccccccccccccc',
                'description': 'Blood Level: 2.2',
                'end_datetime': '2013-07-07T10:00:00Z',
                'start_datetime': '2013-07-07T09:15:00Z',
                'summary': 'Blood Level: 2.2'},
            {'event_id': 'dddddddddddddddddddddddddd',
                'description': 'Test Blood',
                'end_datetime': '2013-07-14T10:00:00Z',
                'start_datetime': '2013-07-14T09:15:00Z',
                'summary': 'Test Blood'}]

        assert data == expected_data


    def test_mergeEntries(self):
        ''' Test that we properly merge newly generated data into
              existing data
        '''
        # Merging exact same 2 dates
        cal_file = './test_files/Calendar.csv'
        data_set = pc.getEntries(pc.loadCalendar(cal_file), 'Pills')
        new_entries = pc.createEntries('06/07/2013', 2, [1,1])
        merged = pc.mergeEntries(data_set, new_entries)
        expected_data = [{'event_id': 'aaaaaaaaaaaaaaaaaaaaaaaaaa',
                'description': 'Sintrom Amount: 1',
                'end_datetime': '2013-07-07T20:15:00Z',
                'start_datetime': '2013-07-07T18:45:00Z',
                'summary': 'Sintrom Amount: 1'},
            {'event_id': 'bbbbbbbbbbbbbbbbbbbbbbbbbb',
                'description': 'Sintrom Amount: 1',
                'end_datetime': '2013-07-06T20:15:00Z',
                'start_datetime': '2013-07-06T18:45:00Z',
                'summary': 'Sintrom Amount: 1'}]
        assert merged == expected_data
        # Merging bc into ab
        cal_file = './test_files/Calendar.csv'
        data_set = pc.getEntries(pc.loadCalendar(cal_file), 'Pills')
        new_entries = pc.createEntries('07/07/2013', 2, [1,1])
        merged = pc.mergeEntries(data_set, new_entries)
        expected_data = [{'event_id': 'bbbbbbbbbbbbbbbbbbbbbbbbbb',
                'description': 'Sintrom Amount: 1',
                'end_datetime': '2013-07-06T20:15:00Z',
                'start_datetime': '2013-07-06T18:45:00Z',
                'summary': 'Sintrom Amount: 1'},
            {'event_id': 'aaaaaaaaaaaaaaaaaaaaaaaaaa',
                'description': 'Sintrom Amount: 1',
                'end_datetime': '2013-07-07T20:15:00Z',
                'start_datetime': '2013-07-07T18:45:00Z',
                'summary': 'Sintrom Amount: 1'},
            {'event_id': '',
                'description': 'Sintrom Amount: 1',
                'end_datetime': '2013-07-08T20:15:00Z',
                'start_datetime': '2013-07-08T18:45:00Z',
                'summary': 'Sintrom Amount: 1'}]
        assert merged == expected_data
        # Merging ab into bc
        cal_file = './test_files/Calendar.csv'
        data_set = pc.getEntries(pc.loadCalendar(cal_file), 'Pills')
        new_entries = pc.createEntries('05/07/2013', 2, [1,1])
        merged = pc.mergeEntries(data_set, new_entries)
        expected_data = [{'event_id': 'aaaaaaaaaaaaaaaaaaaaaaaaaa',
                'description': 'Sintrom Amount: 2',
                'end_datetime': '2013-07-07T20:15:00Z',
                'start_datetime': '2013-07-07T18:45:00Z',
                'summary': 'Sintrom Amount: 2'},
            {'event_id': 'bbbbbbbbbbbbbbbbbbbbbbbbbb',
                'description': 'Sintrom Amount: 1',
                'end_datetime': '2013-07-06T20:15:00Z',
                'start_datetime': '2013-07-06T18:45:00Z',
                'summary': 'Sintrom Amount: 1'},
            {'event_id': '',
                'description': 'Sintrom Amount: 1',
                'end_datetime': '2013-07-05T20:15:00Z',
                'start_datetime': '2013-07-05T18:45:00Z',
                'summary': 'Sintrom Amount: 1'}]
        assert merged == expected_data
        # Merging ef into ab
        cal_file = './test_files/Calendar.csv'
        data_set = pc.getEntries(pc.loadCalendar(cal_file), 'Pills')
        new_entries = pc.createEntries('15/07/2013', 2, [1,1])
        merged = pc.mergeEntries(data_set, new_entries)
        expected_data = [{'event_id': 'aaaaaaaaaaaaaaaaaaaaaaaaaa',
                'description': 'Sintrom Amount: 2',
                'end_datetime': '2013-07-07T20:15:00Z',
                'start_datetime': '2013-07-07T18:45:00Z',
                'summary': 'Sintrom Amount: 2'},
            {'event_id': 'bbbbbbbbbbbbbbbbbbbbbbbbbb',
                'description': 'Sintrom Amount: 1',
                'end_datetime': '2013-07-06T20:15:00Z',
                'start_datetime': '2013-07-06T18:45:00Z',
                'summary': 'Sintrom Amount: 1'},
            {'event_id': '',
                'description': 'Sintrom Amount: 1',
                'end_datetime': '2013-07-15T20:15:00Z',
                'start_datetime': '2013-07-15T18:45:00Z',
                'summary': 'Sintrom Amount: 1'},
            {'event_id': '',
                'description': 'Sintrom Amount: 1',
                'end_datetime': '2013-07-16T20:15:00Z',
                'start_datetime': '2013-07-16T18:45:00Z',
                'summary': 'Sintrom Amount: 1'}]
        assert merged == expected_data
        # Merging ab into ef
        cal_file = './test_files/Calendar.csv'
        data_set = pc.getEntries(pc.loadCalendar(cal_file), 'Pills')
        new_entries = pc.createEntries('01/07/2013', 2, [1,1])
        merged = pc.mergeEntries(data_set, new_entries)
        expected_data = [{'event_id': 'aaaaaaaaaaaaaaaaaaaaaaaaaa',
                'description': 'Sintrom Amount: 2',
                'end_datetime': '2013-07-07T20:15:00Z',
                'start_datetime': '2013-07-07T18:45:00Z',
                'summary': 'Sintrom Amount: 2'},
            {'event_id': 'bbbbbbbbbbbbbbbbbbbbbbbbbb',
                'description': 'Sintrom Amount: 1',
                'end_datetime': '2013-07-06T20:15:00Z',
                'start_datetime': '2013-07-06T18:45:00Z',
                'summary': 'Sintrom Amount: 1'},
            {'event_id': '',
                'description': 'Sintrom Amount: 1',
                'end_datetime': '2013-07-01T20:15:00Z',
                'start_datetime': '2013-07-01T18:45:00Z',
                'summary': 'Sintrom Amount: 1'},
            {'event_id': '',
                'description': 'Sintrom Amount: 1',
                'end_datetime': '2013-07-02T20:15:00Z',
                'start_datetime': '2013-07-02T18:45:00Z',
                'summary': 'Sintrom Amount: 1'}]
        assert merged == expected_data
