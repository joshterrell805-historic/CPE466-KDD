import unittest
import dataset

class TestDataset(unittest.TestCase):
    def test_read_dataset(self):
        dataset_str = """
Id,Political Party,Ideology,Race,Gender,Religion,Family Income,Education,Age,Region,Bush Approval,Vote
-1,3,3,3,2,3,6,3,4,4,2,2
Vote
3,Independent,Moderate,White,Male,Catholic,30000-49999,College,45-64,Northeast,Approve,McCain
4,Republican,Liberal,White,Female,Protestant,50000-74999,H.S. diploma or less,45-64,Northeast,Approve,Obama
5,Democratic,Moderate,White,Male,Catholic,Less than 30000,College,30-44,Midwest,Disapprove,McCain
"""
        col_sets, data = dataset.read(dataset_str)
        self.assertEqual(col_sets[1:], [set(["Independent", "Republican",
                "Democratic"]),set(["Moderate", "Liberal"]),set(["White"]),
                set(["Male","Female"]),set(["Catholic","Protestant"]),set([
                "30000-49999","50000-74999","Less than 30000"]),set(["College",
                "H.S. diploma or less"]),set(["45-64","30-44"]),
                set(["Northeast","Midwest"]),set(["Approve","Disapprove"]),
                set(["McCain","Obama"])])
        self.assertEqual(data,
                [(["3","Independent","Moderate","White", "Male", "Catholic",
                    "30000-49999","College","45-64","Northeast",
                    "Approve"],"McCain"),
                 (["4","Republican","Liberal","White","Female","Protestant",
                    "50000-74999","H.S. diploma or less","45-64","Northeast",
                    "Approve"],"Obama"),
                 (["5","Democratic","Moderate","White","Male","Catholic",
                    "Less than 30000","College","30-44","Midwest",
                    "Disapprove"],"McCain")])
