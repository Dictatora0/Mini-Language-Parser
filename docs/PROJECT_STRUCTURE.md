# 项目结构说明

## 📁 目录结构

```
Mini-Language-Parser/
├── README.md                 # 项目主说明文档
├── LICENSE                   # 许可证文件
├── .gitignore               # Git 忽略文件配置
├── Makefile                 # 项目管理命令
├── setup.py                 # 安装配置
├── pyproject.toml           # 项目配置
├── requirements.txt         # 依赖列表
│
├── src/                     # 核心源代码目录
│   ├── __init__.py         # 包初始化文件
│   ├── lexer.py            # 词法分析器
│   └── parser.py           # 语法分析器
│
├── tests/                   # 测试目录
│   ├── __init__.py         # 测试包初始化
│   └── test_cases.py       # 完整测试套件
│
├── docs/                    # 文档目录
│   ├── GRAMMAR.md          # 完整文法定义
│   └── PROJECT_STRUCTURE.md # 项目结构说明
│
├── data/                    # 数据文件目录
│   ├── correct_example1.txt # 正确示例1
│   ├── correct_example2.txt # 正确示例2
│   ├── correct_example3.txt # 正确示例3
│   ├── error_example1.txt   # 错误示例1
│   └── error_example2.txt   # 错误示例2
│
├── bin/                     # 可执行文件目录（预留）
└── examples/                # 更多示例（预留）
```

---

## 📋 文件说明

### 核心模块 (`src/`)

- **`lexer.py`** - 词法分析器

  - `Token` 类：表示词法单元
  - `TokenType` 枚举：Token 类型定义
  - `Lexer` 类：词法分析器实现

- **`parser.py`** - 语法分析器

  - `Parser` 类：递归下降语法分析器
  - `parse_from_source()` 函数：从源代码分析
  - `parse_from_file()` 函数：从 Token 文件分析

- **`__init__.py`** - 包初始化
  - 导出主要类和函数
  - 版本信息

### 测试模块 (`tests/`)

- **`test_cases.py`** - 完整测试套件
  - 29 个测试用例
  - 覆盖所有语法结构
  - 包含正确和错误程序

### 文档 (`docs/`)

- **`GRAMMAR.md`** - 完整的 EBNF 文法

  - 文法规则说明
  - First/Follow 集合
  - LL(1) 验证

- **`PROJECT_STRUCTURE.md`** - 项目结构说明（本文件）

### 数据文件 (`data/`)

- **`correct_example*.txt`** - 正确的示例程序
- **`error_example*.txt`** - 错误的示例程序

---

## 🚀 使用方式

### 1. 直接运行

```bash
# 主程序（交互式菜单）
python3 main.py

# 分析文件
python3 main.py data/correct_example1.txt

# 运行测试
python3 main.py --test

# 运行示例
python3 main.py --demo
```

### 2. 使用 Makefile

```bash
# 运行测试
make test

# 运行示例
make demo

# 清理临时文件
make clean

# 验证项目结构
make verify
```

### 3. 作为模块导入

```python
from src import Lexer, Parser, parse_from_source

# 词法分析
lexer = Lexer(source_code)
tokens = lexer.tokenize()

# 语法分析
result = parse_from_source(source_code)
print(result)
```

---

## 🔧 开发工作流

### 添加新功能

1. 在 `src/` 目录下添加或修改代码
2. 在 `tests/` 目录下添加对应测试
3. 更新文档（如需要）
4. 运行测试验证

### 运行测试

```bash
# 完整测试套件
make test

# 或
python3 main.py --test
```

### 代码质量

```bash
# 格式化代码（需要安装 black）
make format

# 代码检查（需要安装 flake8）
make lint
```

---

## 📦 安装和部署

### 开发安装

```bash
# 克隆项目
git clone https://github.com/Dictatora0/Mini-Language-Parser.git
cd Mini-Language-Parser

# 安装依赖
pip install -r requirements.txt

# 开发模式安装
pip install -e .
```

### 生产安装

```bash
# 从 PyPI 安装（如果已发布）
pip install mini-language-parser

# 或从源码安装
pip install .
```

---

## 🎯 设计原则

1. **模块化设计** - 清晰的功能分离
2. **标准化结构** - 遵循 Python 项目最佳实践
3. **完整测试** - 全面的测试覆盖
4. **详细文档** - 完善的使用和开发文档
5. **易于扩展** - 便于添加新功能

---

## 📝 贡献指南

1. Fork 项目
2. 创建功能分支
3. 添加测试
4. 确保所有测试通过
5. 提交 Pull Request

---

## 🐛 问题报告

使用 GitHub Issues 报告问题，请包含：

- 详细的问题描述
- 复现步骤
- 期望结果
- 实际结果
- 环境信息

---

**最后更新**: 2024 年
