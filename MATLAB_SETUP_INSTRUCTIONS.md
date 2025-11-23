# MATLAB 设置说明

## 重要提示

**`matlabengine` 不能通过 `pip install` 安装！**

这是正常的，因为 MATLAB Engine for Python 是 MATLAB 的一部分，必须从 MATLAB 安装目录安装。

## 当前状态

✅ **系统已配置完成**
- MATLAB 函数库已创建（5个核心函数）
- Python 接口已创建
- Python 回退实现已实现并测试通过

✅ **系统可以正常工作**
- 即使没有 MATLAB，系统也会使用 Python 回退实现
- 所有功能都可用，只是使用 Python 而不是 MATLAB 进行计算

## 如果您有 MATLAB

### 安装 MATLAB Engine for Python

1. **找到 MATLAB 安装目录**
   ```bash
   # macOS
   ls /Applications/MATLAB*
   
   # Linux
   ls /usr/local/MATLAB/
   ls /opt/MATLAB/
   ```

2. **进入 Python Engine 目录**
   ```bash
   cd /Applications/MATLAB_R2024a.app/extern/engines/python
   # 或您的 MATLAB 版本路径
   ```

3. **安装 Engine**
   ```bash
   # 使用系统 Python
   python3 setup.py install
   
   # 或使用虚拟环境的 Python
   /Users/amy/oppenheimer_env/bin/python3 setup.py install
   ```

4. **验证安装**
   ```bash
   cd /Users/amy/oppenheimer_env
   source bin/activate
   python3 check_matlab_installation.py
   ```

## 如果您没有 MATLAB

**完全没问题！** 系统已经配置了 Python 回退实现：

- ✅ 所有计算功能都可用
- ✅ 使用 NumPy 和 SciPy 进行计算
- ✅ 结果准确，功能完整
- ✅ 无需任何额外安装

### 测试 Python 回退实现

```bash
cd /Users/amy/oppenheimer_env
source bin/activate
python3 check_matlab_installation.py
```

您应该看到：
```
✓ Python 回退实现可用
✓ 系统可以在没有 MATLAB 的情况下工作
✓ 测试计算成功
```

## 功能对比

| 功能 | MATLAB 版本 | Python 回退版本 |
|------|------------|----------------|
| 结合能计算 | ✅ 高精度 | ✅ 完整实现 |
| 临界质量计算 | ✅ 高精度 | ✅ 完整实现 |
| 中子通量计算 | ✅ 高精度 | ✅ 完整实现 |
| 衰变链计算 | ✅ 高精度 | ✅ 完整实现 |
| 量子隧穿计算 | ✅ 高精度 | ✅ 完整实现 |

**区别**：
- MATLAB 版本：使用 MATLAB 的优化数值库，可能在某些复杂计算中更精确
- Python 版本：使用 NumPy/SciPy，功能完整，精度足够用于大多数应用

## 在代码中使用

无论是否有 MATLAB，代码使用方式完全相同：

```python
from matlab_nuclear_analysis.matlab_nuclear_interface import MATLABNuclearAnalysis

# 初始化（自动检测 MATLAB 是否可用）
analysis = MATLABNuclearAnalysis()

# 计算结合能
result = analysis.calculate_binding_energy(92, 235)
print(f"结合能: {result['binding_energy_MeV']:.2f} MeV")
print(f"使用方法: {result['method']}")  # 显示 'MATLAB' 或 'Python_fallback'

# 关闭
analysis.close()
```

## 总结

✅ **当前状态**：系统已完全配置，可以立即使用
✅ **Python 回退**：已实现并测试通过
✅ **MATLAB 集成**：已准备好，安装 MATLAB Engine 后自动启用
✅ **无需操作**：如果不需要 MATLAB，可以直接使用

**建议**：
- 如果您有 MATLAB：按照上述步骤安装 Engine 以获得最佳性能
- 如果您没有 MATLAB：直接使用，Python 回退实现完全够用

