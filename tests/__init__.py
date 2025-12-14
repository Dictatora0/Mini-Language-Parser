"""
Mini 语言语法分析器 - 测试模块
包含完整的测试套件
"""

from .test_parser_comprehensive import run_all_tests as run_comprehensive_tests
from .test_cases import run_all_tests as run_case_tests, TEST_CASES


def run_all_tests():
    success1 = run_comprehensive_tests()
    success2 = run_case_tests()
    return success1 and success2


__all__ = ['run_all_tests', 'TEST_CASES']
