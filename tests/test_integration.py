# tests/test_integration.py
import unittest
from main import main

class TestIntegration(unittest.TestCase):
    def test_main_execution(self):
        # 调用 main() 流程，观察是否会抛出异常
        try:
            main()
        except Exception as e:
            self.fail(f"Main execution raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()

