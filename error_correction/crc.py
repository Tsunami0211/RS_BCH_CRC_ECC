# error_correction/crc.py
import crcmod

class CRC:
    def __init__(self, polynomial, initial_value, final_xor, data_size):
        """
        参数:
          polynomial: 字符串形式的多项式 (例如 "0x1021")
          initial_value: 初始值 (例如 "0xFFFF")
          final_xor: 最终异或值 (例如 "0x0000")
          data_size: 数据大小（bit 数，若有需要进行 bit 操作时使用）
        """
        self.polynomial = int(polynomial, 0)
        self.initial_value = int(initial_value, 0)
        self.final_xor = int(final_xor, 0)
        self.data_size = data_size

        # 使用 crcmod 创建 CRC 函数
        self.crc_func = crcmod.mkCrcFun(self.polynomial, initCrc=self.initial_value, xorOut=self.final_xor)

    def encode(self, data: bytes):
        """
        对输入数据进行 CRC 编码，返回原始数据和 CRC 校验码。
        参数:
          data: bytes 类型数据
        返回:
          tuple: (data, crc_code)
        """
        crc_code = self.crc_func(data)
        return data, crc_code

    def decode(self, received_data: bytes, received_crc: int = None):
        """
        对接收到的数据进行 CRC 校验检测。
        参数:
          received_data: 接收到的 bytes 数据
          received_crc: 如果校验码单独传输，则可传入校验码；否则为 None，直接重新计算。
        返回:
          detected: 布尔值，True 表示校验通过（无错误），False 表示检测到错误
          stats: 字典，包含错误检测的统计信息
        """
        # 计算 CRC 校验码
        computed_crc = self.crc_func(received_data)
        if received_crc is None:
            detected = (computed_crc == 0)
        else:
            detected = (computed_crc == received_crc)
        stats = {"error_detected": not detected}
        return detected, stats

# 测试代码（可选）
if __name__ == "__main__":
    crc_instance = CRC(polynomial="0x1021", initial_value="0xFFFF", final_xor="0x0000", data_size=1024)
    message = b"Hello, CRC!"
    data, crc_code = crc_instance.encode(message)
    print(f"CRC Code: {crc_code}")
    result, stats = crc_instance.decode(data, crc_code)
    print(f"CRC Check Passed? {result}, Stats: {stats}")

