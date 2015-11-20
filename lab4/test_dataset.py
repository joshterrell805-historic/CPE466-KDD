import unittest
import dataset

class TestDataset(unittest.TestCase):
    dataset_str = """
Id,Political Party,Ideology,Race,Gender,Religion,Family Income,Education,Age,Region,Bush Approval,Vote
-1,3,3,3,2,3,6,3,4,4,2,2
Vote
3,Independent,Moderate,White,Male,Catholic,30000-49999,College,45-64,Northeast,Approve,McCain
4,Republican,Liberal,White,Female,Protestant,50000-74999,H.S. diploma or less,45-64,Northeast,Approve,Obama
5,Democratic,Moderate,White,Male,Catholic,Less than 30000,College,30-44,Midwest,Disapprove,McCain
"""
    def test_read_dataset(self):
        cols, data = dataset.read(self.dataset_str)
        self.assertEqual(cols, ['Political Party', 'Ideology',
        'Race', 'Gender', 'Religion', 'Family Income', 'Education',
        'Age', 'Region', 'Bush Approval'])
        self.assertEqual(data,
                [(["Independent","Moderate","White", "Male", "Catholic",
                    "30000-49999","College","45-64","Northeast",
                    "Approve"],"McCain"),
                 (["Republican","Liberal","White","Female","Protestant",
                    "50000-74999","H.S. diploma or less","45-64","Northeast",
                    "Approve"],"Obama"),
                 (["Democratic","Moderate","White","Male","Catholic",
                    "Less than 30000","College","30-44","Midwest",
                    "Disapprove"],"McCain")])

    def test_read_dataset_with_restrictions(self):
        cols, data = dataset.read(self.dataset_str,
                                  restrictions=[0,1,0,0,1,0,0,0,0,0,1])
        self.assertEqual(cols, ['Political Party', 'Gender',
                                'Bush Approval'])
        self.assertEqual(data,
                [(["Independent","Male","Approve"],"McCain"),
                 (["Republican","Female","Approve"],"Obama"),
                 (["Democratic","Male","Disapprove"],"McCain")])

        cols, data = dataset.read(self.dataset_str, has_label=False,
                                  restrictions=[0,1,0,0,1,0,0,0,0,0,1,1])
        self.assertEqual(cols, ['Political Party', 'Gender',
                                'Bush Approval', 'Vote'])
        self.assertEqual(data,
                [(["Independent","Male","Approve","McCain"], None),
                 (["Republican","Female","Approve","Obama"], None),
                 (["Democratic","Male","Disapprove","McCain"], None)])
