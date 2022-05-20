
from tests.test_base import TestBase


class TestStructure(TestBase):

    def test_structure_data(self):
        """
        verify that the data files have been moved
        """

        ls = self.load_results()

        assert "train_1k.csv" in ls, "unable to find the train_1k.csv dataset"
        assert "train_10k.csv" in ls, "unable to find the train_10k.csv dataset"
        assert "train_100k.csv" in ls, "unable to find the train_100k.csv dataset"

        assert "val_1k.csv" in ls, "unable to find the val_1k.csv dataset"
        assert "val_10k.csv" in ls, "unable to find the val_10k.csv dataset"
        assert "val_100k.csv" in ls, "unable to find the val_100k.csv dataset"
