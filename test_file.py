import os
import district_portal
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        # self.db_fd, district_portal.app.config['DATABASE'] = tempfile.mkstemp()
        district_portal.app.testing = True
        self.app = district_portal.app.test_client()
        with district_portal.app.app_context():
            district_portal.home_controller()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(district_portal.app.config['DATABASE'])


if __name__ == '__main__':
    unittest.main()
