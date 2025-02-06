# error_correction/rs.py
import reedsolo

class ReedSolomon:
    def __init__(self, data_size, redundancy, primitive_polynomial, generator_polynomial=None):
        """
        参数:
          data_size: 数据大小（字节数）
          redundancy: 冗余字节数
          primitive_polynomial: 本原多项式（字符串形式，如 "0x11D"）
          generator_polynomial: 可选，自定义生成多项式（本例中暂不深入）
        """
        self.data_size = data_size
        self.redundancy = redundancy
        self.primitive_polynomial = int(primitive_polynomial, 0)
        self.generator_polynomial = generator_polynomial  # 可扩展

        # 初始化 reedsolo 库（设置 GF 表，基于本原多项式）
        reedsolo.init_tables(primitive=self.primitive_polynomial)
        self.rs = reedsolo.RSCodec(redundancy)

    def encode(self, data: bytes) -> bytes:
        """
        对输入数据进行 Reed-Solomon 编码，返回包含冗余信息的编码数据。
        """
        encoded = self.rs.encode(data)
        return encoded

    def decode(self, received_data: bytes):
        """
        对 Reed-Solomon 编码后的数据进行解码。
        返回:
          corrected: 纠正后的数据（如果解码成功则返回 bytes，否则为 None）
          stats: 字典，包含初步状态:
                 - 如果 reedsolo 抛出异常，则状态为 "DUE"（纠错失败）
                 - 如果解码过程中未检测到错误，则状态为 "UUE"
                 - 如果纠正成功，则状态为 "CORRECTED"
        """
        stats = {}
        try:
            corrected = self.rs.decode(received_data)
            # reedsolo 库不会抛出异常如果未检测到错误，
            # 这里需要外部传入原始数据后做比对决定 DCE 或 DME
            stats["status"] = "CORRECTED"
        except reedsolo.ReedSolomonError as e:
            corrected = None
            stats["status"] = "DUE"  # 无法纠正错误
        return corrected, stats

# 测试代码（可选）
if __name__ == "__main__":
    rs_instance = ReedSolomon(data_size=256, redundancy=16, primitive_polynomial="0x11D")
    message = b"Hello, RS Error Correction!"
    encoded = rs_instance.encode(message)
    print("Encoded RS Data:", encoded)
    # 模拟无错误情况进行解码
    corrected, stats = rs_instance.decode(encoded)
    print("Decoded RS Data:", corrected, "Stats:", stats)

