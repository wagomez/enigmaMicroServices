import os
from microsvc import msAPIGetDevices
import unittest

class msAPIGetDevicesTestCase(unittest.TestCase):

    def setUp(self):
        print("SetUP")
        #self.db_fd, newApp.app.config['DATABASE'] = tempfile.mkstemp()
        #newApp.app.config['TESTING'] = True
        self.app = msAPIGetDevices.app.test_client()
        #with newApp.app.app_context():
        #newApp.init_db()


    def tearDown(self):
        print("tear Down")

    def test_GetDevicesCMTS(self):
        #self.setUp()
        rv = self.app.get('/getDevicesGroup/CMTS')
        print("Respuesta")
        print (rv.data)
        assert b'["cbr8' in rv.data

    def test_GetDevicesPE(self):
        #self.setUp()
        rv = self.app.get('/getDevicesGroup/PE')
        print("Respuesta")
        print (rv.data)
        assert b'["PE' in rv.data



if __name__ == '__main__':
    unittest.main()
