# error_correction/bch.py
import bchlib

class BCH:
    def __init__(self, symbol_size, redundancy, primitive_polynomial, generator_polynomial):
        """
        参数:
          symbol_size: 每个 symbol 的大小（单位：bit），例如 4 表示 GF(2^4)
          redundancy: 冗余字节数或冗余 symbol 数（取决于 bchlib 的定义）
          primitive_polynomial: 本原多项式（字符串形式，如 "0x1D"）
          generator_polynomial: 生成多项式（bchlib 内部使用，此参数将传入 bchlib.BCH 构造函数）
        """
        self.symbol_size = symbol_size
        self.redundancy = redundancy
        # bchlib 接受的多项式通常为整数形式
        self.primitive_polynomial = int(primitive_polynomial, 0)
        self.generator_polynomial = generator_polynomial  # 根据 bchlib 的要求使用

        # 初始化 bchlib.BCH 实例，通常构造函数为 BCH(多项式, t)
        # 这里 t 对应纠正能力，你可以把 redundancy 视为 t
        self.bch = bchlib.BCH(self.primitive_polynomial, self.redundancy)

    def encode(self, data: bytes) -> bytes:
        """
        对输入数据进行 BCH 编码，返回编码后的数据（原始数据 + 冗余校验部分）。
        """
        ecc = self.bch.encode(data)
        encoded = data + ecc
        return encoded

    def decode(self, received_data: bytes):
        """
        对 BCH 编码后的数据进行解码和纠错。
        返回:
          corrected: 纠正后的数据（如果纠正成功则返回 bytes，否则为 None）
          stats: 字典，包含初步状态：
                 - 如果 bchlib 无法纠正错误，则状态为 "DUE"
                 - 如果纠正成功，则状态为 "CORRECTED"
        """
        # 设定 ecc_size
        ecc_bytes = self.bch.ecc_bytes
        # 分离数据和 ecc 部分
        data_part = received_data[:-ecc_bytes]
        ecc_part = received_data[-ecc_bytes:]
        # 尝试纠正数据
        bitflips = self.bch.decode(data_part, ecc_part)
        stats = {}
        if bitflips is None:
            # 无法纠正错误
            corrected = None
            stats["status"] = "DUE"
        else:
            corrected = data_part  # bchlib 在 decode 后返回修正后的数据部分
            stats["status"] = "CORRECTED"
        return corrected, stats

# 测试代码（可选）
if __name__ == "__main__":
    # 这里假设 symbol_size 为 4, redundancy 为 5, primitive_polynomial "0x1D" 为示例值
    bch_instance = BCH(symbol_size=4, redundancy=5, primitive_polynomial="0x1D", generator_polynomial="GEN_POLY")
    message = b"Hello, BCH!"
    encoded = bch_instance.encode(message)
    print("Encoded BCH Data:", encoded)
    corrected, stats = bch_instance.decode(encoded)
    print("Decoded BCH Data:", corrected, "Stats:", stats)

