import time
from SetUp import SetUp


class TestConnectProf(SetUp):

    def test_connect(self):
        self.connect_prof()
        time.sleep(3)
        self.disconnect()
