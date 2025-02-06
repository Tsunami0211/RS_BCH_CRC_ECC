# error_injection/injector.py

import random

def inject_single_bit_error(data: bytes, num_errors: int = 1) -> bytes:
    """
    对数据随机选择 num_errors 个 bit 进行反转
    参数:
      data: 输入数据，bytes 类型
      num_errors: 要反转的 bit 数量，默认 1
    返回:
      注入错误后的 bytes 数据
    """
    # 将数据转换为可变的 bytearray
    data_array = bytearray(data)
    total_bits = len(data_array) * 8  # 数据总 bit 数

    for _ in range(num_errors):
        # 随机选择一个 bit 的索引
        bit_index = random.randint(0, total_bits - 1)
        # 定位到具体的 byte 和 bit 位
        byte_index = bit_index // 8
        bit_in_byte = bit_index % 8
        # 反转对应 bit，注意：1<<bit_in_byte 产生掩码
        data_array[byte_index] ^= (1 << bit_in_byte)

    return bytes(data_array)

def inject_double_bit_error(data: bytes, num_errors: int = 1) -> bytes:
    """
    对数据随机选择 num_errors 对 bit 进行双比特反转
    此处定义为反转两个不同位置的 bit（也可以定义为在同一个 byte 内连续的两个 bit）
    参数:
      data: 输入数据，bytes 类型
      num_errors: 要注入的双比特错误对数，默认 1
    返回:
      注入错误后的 bytes 数据
    """
    data_array = bytearray(data)
    total_bits = len(data_array) * 8

    for _ in range(num_errors):
        # 随机选择两个不同的 bit 索引
        bit_index1 = random.randint(0, total_bits - 1)
        bit_index2 = random.randint(0, total_bits - 1)
        # 确保两个索引不同
        while bit_index2 == bit_index1:
            bit_index2 = random.randint(0, total_bits - 1)

        # 定位两个 bit 分别在哪个 byte 以及位位置
        for bit_index in (bit_index1, bit_index2):
            byte_index = bit_index // 8
            bit_in_byte = bit_index % 8
            data_array[byte_index] ^= (1 << bit_in_byte)

    return bytes(data_array)

# 如果需要支持其它错误注入方法，可以继续添加函数

# 示例测试代码（可选）
if __name__ == "__main__":
    original_data = b"Hello, Error Injection!"
    print("Original Data:", original_data)
    
    # 测试单比特反转
    corrupted_single = inject_single_bit_error(original_data, num_errors=3)
    print("Data after single bit errors:", corrupted_single)
    
    # 测试双比特反转
    corrupted_double = inject_double_bit_error(original_data, num_errors=2)
    print("Data after double bit errors:", corrupted_double)

