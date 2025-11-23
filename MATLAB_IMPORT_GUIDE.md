# MATLAB 代码导入指南

## 概述

系统已支持导入 MATLAB `.m` 文件到知识库！MATLAB 代码中的数学公式、注释和计算逻辑会被自动提取并添加到知识库中。

## 功能特性

✅ **自动提取**：
- MATLAB 注释（以 `%` 开头的行）
- 数学表达式和公式
- 变量赋值和函数调用
- 代码逻辑和算法

✅ **智能识别**：
- 量子物理相关代码自动分类
- 核物理计算自动识别
- 公式和概念自动提取

✅ **批量导入**：
- 支持单个文件导入
- 支持整个目录批量导入
- 递归搜索子目录

## 使用方法

### 1. 导入单个 MATLAB 文件

```bash
# 激活虚拟环境
source bin/activate

# 导入单个文件
python3 import_matlab_files.py --file path/to/your/file.m
```

**示例**：
```bash
python3 import_matlab_files.py --file example_quantum_schrodinger.m
```

### 2. 批量导入目录中的所有 MATLAB 文件

```bash
# 导入目录中的所有 .m 文件
python3 import_matlab_files.py --directory path/to/matlab/code/

# 导入当前目录
python3 import_matlab_files.py --directory .
```

### 3. 创建示例文件

```bash
# 创建一个示例 MATLAB 文件用于测试
python3 import_matlab_files.py --create-example
```

## MATLAB 文件格式要求

### 推荐的 MATLAB 文件格式

```matlab
% filename.m
% Brief description of what this code does
% 
% Mathematical equations:
%   H*psi = E*psi  (Schrödinger equation)
%   Where H = -hbar^2/(2m) * d^2/dx^2 + V(x)
%
% Parameters:
%   x: position vector
%   m: particle mass
%   V: potential energy function

function [output] = function_name(input)
    % Implementation details
    % Mathematical formulas used:
    %   E = hbar^2 * k^2 / (2*m)
    %   psi = A * exp(i*k*x)
    
    % Code here
end
```

### 最佳实践

1. **添加详细注释**：
   - 文件开头说明代码用途
   - 列出使用的数学公式
   - 说明参数和返回值

2. **使用有意义的变量名**：
   - `hbar` 而不是 `h`
   - `wave_function` 而不是 `wf`
   - `potential_energy` 而不是 `pe`

3. **包含数学公式**：
   - 在注释中写出完整的数学表达式
   - 说明公式的物理意义

## 示例：量子力学 MATLAB 代码

```matlab
% quantum_schrodinger_solver.m
% Solves the time-independent Schrödinger equation
% 
% Equation: H*psi = E*psi
% Where H = -hbar^2/(2m) * d^2/dx^2 + V(x)
%
% This implements the quantum mechanical wave function solution

function [E, psi] = quantum_schrodinger_solver(V, x, m)
    % Physical constants
    hbar = 1.0545718e-34;  % Reduced Planck constant (J·s)
    
    % Hamiltonian operator: H = -hbar^2/(2m) * d^2/dx^2 + V(x)
    % Discretize the second derivative
    dx = x(2) - x(1);
    N = length(x);
    
    % Kinetic energy operator (finite difference)
    T = -hbar^2/(2*m) * (diag(ones(N-1,1),1) - 2*eye(N) + diag(ones(N-1,1),-1)) / dx^2;
    
    % Potential energy operator (diagonal)
    V_matrix = diag(V);
    
    % Total Hamiltonian
    H = T + V_matrix;
    
    % Solve eigenvalue problem: H*psi = E*psi
    [psi, E] = eig(H);
    E = diag(E);
    
    % Normalize wave functions
    for i = 1:length(E)
        psi(:,i) = psi(:,i) / sqrt(trapz(x, abs(psi(:,i)).^2));
    end
end
```

## 导入后的数据

导入的 MATLAB 代码会包含以下信息：

- **标题**：`MATLAB Code: [filename]`
- **内容**：代码和注释的完整文本
- **公式**：自动提取的数学表达式
- **概念**：自动识别的物理概念（量子力学、核物理等）
- **关键词**：文件名、MATLAB、相关概念
- **领域**：自动分类到相应领域

## 查看导入结果

导入完成后，数据会：
1. ✅ 添加到 `knowledge_base.json`
2. ✅ 添加到向量索引（用于语义搜索）
3. ✅ 提取所有公式和概念

## 支持的 MATLAB 代码类型

✅ **量子物理计算**：
- 薛定谔方程求解器
- 量子隧穿计算
- 量子态演化
- 量子纠缠计算

✅ **核物理计算**：
- 结合能计算
- 临界质量计算
- 中子通量计算
- 反应截面计算

✅ **数学计算**：
- 数值积分
- 微分方程求解
- 矩阵运算
- 统计分析

## 故障排除

### 问题：文件未找到

```
Error: File 'path/to/file.m' not found!
```

**解决方案**：检查文件路径是否正确，使用绝对路径或确保在正确的目录下运行。

### 问题：没有数据提取

```
No data extracted from MATLAB file
```

**解决方案**：
- 确保文件包含注释（以 `%` 开头）
- 添加数学表达式和公式
- 检查文件编码是否为 UTF-8

### 问题：导入失败

```
Error importing MATLAB file: [error message]
```

**解决方案**：
- 检查文件格式是否正确
- 确保文件可读
- 查看错误信息了解具体问题

## 集成到现有工作流

### 在数据导入脚本中使用

```python
from data_importer import DataImporter
from knowledge_manager import KnowledgeManager

# 初始化
importer = DataImporter()
km = KnowledgeManager()

# 导入 MATLAB 文件
matlab_data = importer.import_from_matlab_code("path/to/file.m")

# 添加到知识库
for item in matlab_data:
    km.add_knowledge(item)
```

## 总结

✅ MATLAB 代码导入功能已完全集成
✅ 支持单个文件和批量导入
✅ 自动提取公式、概念和注释
✅ 智能分类到相应领域
✅ 已测试并验证功能正常

现在您可以轻松地将 MATLAB 代码中的数学知识导入到 Oppenheimer AI 的知识库中！

