# tests/test_rs.py
import unittest
from error_correction import ReedSolomon

class TestRS(unittest.TestCase):
    def setUp(self):
        self.rs = ReedSolomon(data_size=256, redundancy=16, primitive_polynomial="0x11D")
        self.test_data = b"UnitTest RS data"

    def test_encode_decode_no_error(self):
        encoded = self.rs.encode(self.test_data)
        corrected, stats = self.rs.decode(encoded)
        # 若无错误注入，应当返回原始数据
        self.assertIsNotNone(corrected)
        self.assertEqual(corrected, self.test_data)
        self.assertEqual(stats.get("status"), "CORRECTED")

    def test_decode_with_error(self):
        # 模拟错误注入后 RS 解码失败的情况
        encoded = self.rs.encode(self.test_data)
        # 简单地修改 encoded 数据中的部分内容
        corrupted = bytearray(encoded)
        corrupted[5] ^= 0xFF  # 反转第6个字节
        corrected, stats = self.rs.decode(bytes(corrupted))
        # 如果 RS 无法纠正错误，则返回状态 DUE
        self.assertIsNone(corrected)
        self.assertEqual(stats.get("status"), "DUE")

if __name__ == "__main__":
    unittest.main()

