# tests/test_crc.py
import unittest
from error_correction import CRC

class TestCRC(unittest.TestCase):
    def setUp(self):
        # 初始化一个 CRC 实例
        self.crc = CRC(polynomial="0x1021", initial_value="0xFFFF", final_xor="0x0000", data_size=1024)
        self.test_data = b"UnitTest CRC data"
        self.data, self.crc_code = self.crc.encode(self.test_data)

    def test_encode(self):
        # 检查返回类型是否正确
        self.assertIsInstance(self.data, bytes)
        self.assertIsInstance(self.crc_code, int)

    def test_decode_no_error(self):
        # 在无错误情况下，decode 应该返回检测通过
        detected, stats = self.crc.decode(self.data, self.crc_code)
        self.assertTrue(detected)
        self.assertEqual(stats.get("error_detected"), False)

    def test_decode_with_error(self):
        # 制造一个错误，确保 CRC 能够检测到错误
        # 这里可以调用错误注入模块或直接修改数据
        corrupted = bytearray(self.data)
        # 改变第一个 byte 的第一个 bit
        corrupted[0] ^= 0x01
        detected, stats = self.crc.decode(bytes(corrupted), self.crc_code)
        self.assertFalse(detected)
        self.assertEqual(stats.get("error_detected"), True)

if __name__ == "__main__":
    unittest.main()

