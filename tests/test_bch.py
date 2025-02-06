# tests/test_bch.py
import unittest
from error_correction import BCH

class TestBCH(unittest.TestCase):
    def setUp(self):
        # 这里需要根据 bchlib 的要求进行设置，示例参数仅供参考
        self.bch = BCH(symbol_size=4, redundancy=5, primitive_polynomial="0x1D", generator_polynomial="GEN_POLY")
        self.test_data = b"UnitTest BCH data"

    def test_encode_decode_no_error(self):
        encoded = self.bch.encode(self.test_data)
        corrected, stats = self.bch.decode(encoded)
        self.assertIsNotNone(corrected)
        self.assertEqual(corrected, self.test_data)
        self.assertEqual(stats.get("status"), "CORRECTED")

    def test_decode_with_error(self):
        encoded = self.bch.encode(self.test_data)
        corrupted = bytearray(encoded)
        # 反转 ECC 部分中的一部分数据，模拟错误
        if len(corrupted) > self.bch.bch.ecc_bytes:
            # 修改 ECC 的第一个字节
            corrupted[-self.bch.bch.ecc_bytes] ^= 0xFF
        corrected, stats = self.bch.decode(bytes(corrupted))
        # 如果纠正失败，状态应为 DUE
        if corrected is None:
            self.assertEqual(stats.get("status"), "DUE")
        else:
            # 如果纠正成功，必须与原始数据一致
            self.assertEqual(corrected, self.test_data)

if __name__ == "__main__":
    unittest.main()
W
