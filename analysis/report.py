# analysis/report.py
import matplotlib.pyplot as plt
import os

class ReportGenerator:
    def __init__(self):
        """
        初始化统计数据存储字典。
        格式示例：
            {
                "CRC": {"error_detected": 0, "total_tests": 0},
                "RS": {"DCE": 0, "DME": 0, "DUE": 0, "UUE": 0},
                "BCH": {"DCE": 0, "DME": 0, "DUE": 0, "UUE": 0},
            }
        """
        self.results = {
            "CRC": {"error_detected": 0, "total_tests": 0},
            "RS": {"DCE": 0, "DME": 0, "DUE": 0, "UUE": 0},
            "BCH": {"DCE": 0, "DME": 0, "DUE": 0, "UUE": 0},
        }

    def add_result(self, algorithm: str, result: dict):
        """
        添加某个算法的测试结果到统计数据中。
        参数:
          algorithm: 字符串，"CRC", "RS" 或 "BCH"
          result: 一个字典，包含测试结果统计信息。
                  对于 CRC 示例：{"error_detected": 1, "total_tests": 1}
                  对于 RS/BCH 示例：{"status": "DCE"} 或其它状态。
        """
        if algorithm == "CRC":
            # 对于 CRC，我们累加 error_detected 和 total_tests
            self.results["CRC"]["error_detected"] += result.get("error_detected", 0)
            self.results["CRC"]["total_tests"] += result.get("total_tests", 0)
        elif algorithm in ("RS", "BCH"):
            # 对于 RS 和 BCH，我们根据状态累加
            status = result.get("status")
            if status in self.results[algorithm]:
                self.results[algorithm][status] += 1

    def generate_charts(self, output_dir: str = "analysis", output_file: str = "report.png"):
        """
        根据统计数据生成图表，并保存到指定输出文件中。
        参数:
          output_dir: 输出文件夹，默认为 analysis 目录
          output_file: 输出图表文件名
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 生成 CRC 的图表（例如：错误检测率柱状图）
        crc_data = self.results["CRC"]
        if crc_data["total_tests"] > 0:
            detection_rate = (crc_data["total_tests"] - crc_data["error_detected"]) / crc_data["total_tests"] * 100
        else:
            detection_rate = 0

        fig, axs = plt.subplots(1, 3, figsize=(18, 5))

        # 图1：CRC 错误检测率
        axs[0].bar(["CRC"], [detection_rate], color="blue")
        axs[0].set_title("CRC Error Detection Rate")
        axs[0].set_ylim(0, 100)
      

