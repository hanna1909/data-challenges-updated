
from tests.test_base import TestBase


class TestShifts(TestBase):

    def test_shifts_parameters(self):
        """
        verify that the shifts parameters are correctly set
        """

        db_user = self.load_results("test_shifts_db_user")
        db_password = self.load_results("test_shifts_db_password")
        db_hostname = self.load_results("test_shifts_db_hostname")
        db_port = self.load_results("test_shifts_db_port")
        db_name = self.load_results("test_shifts_db_name")
        tracking_db = self.load_results("test_shifts_tracking_db")

        assert db_user == "taxifare_readonly"
        assert db_password == "m4e7dbNPDPg8tNR2Br36NgUGd3"
        assert db_hostname == "wagon-mlflo-1768.postgresql.a.osc-fr1.scalingo-dbs.com"
        assert db_port == "37750"
        assert db_name == "wagon_mlflo_1768"
        assert tracking_db == "postgresql://taxifare_readonly:m4e7dbNPDPg8tNR2Br36NgUGd3@wagon-mlflo-1768.postgresql.a.osc-fr1.scalingo-dbs.com:37750/wagon_mlflo_1768"

    def test_shifts_get_latest_trained_row(self):
        """
        verify the retrieval of the latest trained row
        """

        # TODO
        assert True

    def test_shifts_complete(self):
        """
        verify that the complete workflow runs on all new data chunks
        """

        # TODO
        assert True
