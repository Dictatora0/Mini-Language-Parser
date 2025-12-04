# Mini 语言语法分析器 Makefile

.PHONY: help test clean install format lint demo run

# 默认目标
help:
	@echo "Mini 语言语法分析器 - 可用命令:"
	@echo "  make test     - 运行测试套件"
	@echo "  make demo     - 运行示例程序"
	@echo "  make run      - 运行主程序"
	@echo "  make install  - 安装项目"
	@echo "  make format   - 格式化代码"
	@echo "  make lint     - 代码检查"
	@echo "  make clean    - 清理临时文件"

# 运行测试
test:
	@echo "运行测试套件..."
	python3 main.py --test

# 运行示例
demo:
	@echo "运行示例程序..."
	python3 main.py --demo

# 运行主程序
run:
	@echo "启动主程序..."
	python3 main.py

# 安装项目
install:
	@echo "安装项目依赖..."
	pip3 install -r requirements.txt
	pip3 install -e .

# 代码格式化
format:
	@echo "格式化代码..."
	@if command -v black >/dev/null 2>&1; then \
		black src/ tests/ main.py; \
	else \
		echo "请安装 black: pip install black"; \
	fi

# 代码检查
lint:
	@echo "进行代码检查..."
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 src/ tests/ main.py; \
	else \
		echo "请安装 flake8: pip install flake8"; \
	fi

# 清理临时文件
clean:
	@echo "清理临时文件..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".DS_Store" -delete
	find . -type f -name "*.log" -delete
	find . -type f -name "*.tmp" -delete
	rm -rf build/ dist/ *.egg-info/

# 运行单个示例文件
run-example:
	@echo "运行示例文件..."
	python3 main.py data/correct_example1.txt

# 生成文档
docs:
	@echo "生成文档..."
	@echo "文档已存在于 docs/ 目录"

# 验证项目结构
verify:
	@echo "验证项目结构..."
	@echo "检查必需文件..."
	@test -f main.py && echo "✓ main.py 存在" || echo "✗ main.py 缺失"
	@test -f src/lexer.py && echo "✓ src/lexer.py 存在" || echo "✗ src/lexer.py 缺失"
	@test -f src/parser.py && echo "✓ src/parser.py 存在" || echo "✗ src/parser.py 缺失"
	@test -f tests/test_cases.py && echo "✓ tests/test_cases.py 存在" || echo "✗ tests/test_cases.py 缺失"
	@test -f README.md && echo "✓ README.md 存在" || echo "✗ README.md 缺失"
	@test -f docs/GRAMMAR.md && echo "✓ docs/GRAMMAR.md 存在" || echo "✗ docs/GRAMMAR.md 缺失"
	@echo "结构验证完成！"
