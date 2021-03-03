import unittest
import kiltis
import kiltalainen


class MyTestCase(unittest.TestCase):


    def test_kiltis(self):
        kiltalainen1 = kiltalainen.Kiltalainen("nimi", "tupsu")
        kiltalainen2 = kiltalainen.Kiltalainen("nimi2", "fuksi")

        kil = kiltis.Kiltis()
        kiltis.add_kiltalainen(kiltalainen1)
        kiltis.add_kiltalainen(kiltalainen2)

        self.assertEqual(kiltis.kiltalaiset == [kiltalainen1, kiltalainen2])




if __name__ == '__main__':
    unittest.main()
