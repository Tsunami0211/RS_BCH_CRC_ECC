# main.py

from config.config_loader import load_config  # 配置加载器
from error_correction import CRC, ReedSolomon, BCH
from error_injection import inject_single_bit_error, inject_double_bit_error
from analysis import ReportGenerator

def main():
    # 1. 加载配置
    config = load_config("config/parameters.yaml")
    
    # 2. 初始化各个模块
    # 初始化 CRC 模块（如果启用）
    crc_instance = None
    if config.get("crc", {}).get("enabled", False):
        crc_instance = CRC(
            polynomial=config["crc"]["polynomial"],
            initial_value=config["crc"]["initial_value"],
            final_xor=config["crc"]["final_xor"],
            data_size=config["crc"]["data_size"]
        )
    
    # 初始化 RS 模块（如果启用）
    rs_instance = None
    if config.get("rs", {}).get("enabled", False):
        rs_instance = ReedSolomon(
            data_size=config["rs"]["data_size"],
            redundancy=config["rs"]["redundancy"],
            primitive_polynomial=config["rs"]["primitive_polynomial"],
            generator_polynomial=config["rs"]["generator_polynomial"]
        )
    
    # 初始化 BCH 模块（如果启用）
    bch_instance = None
    if config.get("bch", {}).get("enabled", False):
        bch_instance = BCH(
            symbol_size=config["bch"]["symbol_size"],
            redundancy=config["bch"]["redundancy"],
            primitive_polynomial=config["bch"]["primitive_polynomial"],
            generator_polynomial=config["bch"]["generator_polynomial"]
        )
    
    # 3. 准备原始测试数据
    original_data = b"Test message for error correction"
    
    # 4. 创建 ReportGenerator 实例，用于统计测试结果
    report_generator = ReportGenerator()
    
    # 5. 进行测试：这里以 CRC、RS、BCH 分别进行一次测试，并使用错误注入模拟数据错误
    # 测试 CRC
    if crc_instance:
        # 对原始数据进行 CRC 编码，返回原始数据和校验码
        data, crc_code = crc_instance.encode(original_data)
        # 使用错误注入（例如：单比特错误）模拟数据错误
        corrupted_data = inject_single_bit_error(data, num_errors=1)
        # 校验纠错：传入原始数据和校验码进行检测
        detected, crc_stats = crc_instance.decode(corrupted_data, crc_code)
        # 构造 CRC 的测试结果（这里：如果检测通过则 error_detected 为 0，否则为 1）
        crc_test_result = {
            "error_detected": 0 if detected else 1,
            "total_tests": 1
        }
        report_generator.add_result("CRC", crc_test_result)
    
    # 测试 RS
    if rs_instance:
        # 对原始数据进行 RS 编码
        rs_encoded = rs_instance.encode(original_data)
        # 模拟错误注入（比如单比特错误）
        rs_corrupted = inject_single_bit_error(rs_encoded, num_errors=2)
        # 尝试 RS 解码
        rs_corrected, rs_stats = rs_instance.decode(rs_corrupted)
        # 外部比对：如果 rs_corrected 为 None 则说明无法纠错（DUE）
        # 如果不为 None，再与原始数据比较：相同则 DCE，不同则 DME
        if rs_corrected is None:
            rs_final_status = "DUE"
        else:
            rs_final_status = "DCE" if rs_corrected == original_data else "DME"
        # 注意：如果没有注入错误，可能会出现 UUE 的情况，但这里模拟的是错误场景
        report_generator.add_result("RS", {"status": rs_final_status})
    
    # 测试 BCH
    if bch_instance:
        # 对原始数据进行 BCH 编码
        bch_encoded = bch_instance.encode(original_data)
        # 模拟错误注入（例如：双比特错误）
        bch_corrupted = inject_double_bit_error(bch_encoded, num_errors=1)
        # 尝试 BCH 解码
        bch_corrected, bch_stats = bch_instance.decode(bch_corrupted)
        # 外部比对：如果解码返回 None 则为 DUE，否则比较原始数据确定 DCE 或 DME
        if bch_corrected is None:
            bch_final_status = "DUE"
        else:
            bch_final_status = "DCE" if bch_corrected == original_data else "DME"
        report_generator.add_result("BCH", {"status": bch_final_status})
    
    # 6. 生成最终报告
    report_generator.generate_text_report()
    # 使用配置文件中 report 部分设置的文件名生成图表
    output_file = config.get("report", {}).get("output_file", "report.png")
    report_generator.generate_charts(output_file=output_file)
    
if __name__ == "__main__":
    main()

