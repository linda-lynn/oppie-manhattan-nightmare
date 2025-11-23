# MATLAB 核物理数据分析集成指南

## 概述

已创建完整的 MATLAB 核物理分析系统，允许 Oppenheimer AI 使用 MATLAB 进行高精度核物理计算。

## 系统架构

### 1. MATLAB 函数库 (`matlab_nuclear_analysis/`)

包含以下 MATLAB 函数：

- **`binding_energy.m`** - 结合能计算（半经验质量公式）
- **`critical_mass.m`** - 临界质量计算（四因子公式）
- **`neutron_flux.m`** - 中子通量计算
- **`decay_chain.m`** - 放射性衰变链计算
- **`quantum_tunneling.m`** - 量子隧穿概率计算

### 2. Python 接口 (`matlab_nuclear_interface.py`)

提供 Python 到 MATLAB 的桥接，包括：
- MATLAB Engine 启动和管理
- 函数调用封装
- 数据类型转换（Python ↔ MATLAB）
- 错误处理和回退机制

## 安装步骤

### 方法 1: 使用 MATLAB Engine for Python（推荐）

1. **安装 MATLAB**
   - 确保已安装 MATLAB（R2014b 或更高版本）

2. **安装 MATLAB Engine for Python**
   ```bash
   # 找到 MATLAB 安装目录
   # macOS/Linux: 通常在 /Applications/MATLAB_R20XX.app/ 或 /usr/local/MATLAB/R20XX/
   # Windows: 通常在 C:\Program Files\MATLAB\R20XX\
   
   # 进入 MATLAB Engine Python 目录
   cd matlabroot/extern/engines/python
   
   # 安装（使用您的 Python 解释器）
   python setup.py install
   # 或
   python3 setup.py install
   ```

3. **验证安装**
   ```python
   import matlab.engine
   eng = matlab.engine.start_matlab()
   print("MATLAB version:", eng.version())
   eng.quit()
   ```

### 方法 2: 使用 pip（如果可用）

```bash
pip install matlabengine
```

**注意**: 此方法可能不适用于所有 MATLAB 版本。

## 使用方法

### 基本使用

```python
from matlab_nuclear_interface import MATLABNuclearAnalysis

# 初始化 MATLAB 接口
matlab_analysis = MATLABNuclearAnalysis()

# 计算结合能
result = matlab_analysis.calculate_binding_energy(Z=92, A=235)
print(f"Binding energy: {result['binding_energy_MeV']:.2f} MeV")
print(f"Per nucleon: {result['binding_energy_per_nucleon_MeV']:.2f} MeV/nucleon")

# 计算临界质量
result = matlab_analysis.calculate_critical_mass(
    Z=92, A=235, 
    density=18700,  # kg/m³
    geometry='sphere'
)
print(f"Critical mass: {result['critical_mass_kg']:.2f} kg")
print(f"Critical radius: {result['critical_radius_m']*100:.2f} cm")

# 关闭 MATLAB 引擎
matlab_analysis.close()
```

### 在 Oppenheimer GUI 中集成

修改 `oppenheimer_gui.py` 以使用 MATLAB：

```python
from matlab_nuclear_interface import MATLABNuclearAnalysis

class OppenheimerGUI:
    def __init__(self):
        # ... 现有初始化代码 ...
        
        # 初始化 MATLAB 分析接口
        self.matlab_analysis = MATLABNuclearAnalysis()
    
    def calculate_nuclear_properties(self):
        Z = int(self.z_entry.get())
        A = int(self.a_entry.get())
        
        # 使用 MATLAB 计算结合能
        if self.matlab_analysis.matlab_available:
            result = self.matlab_analysis.calculate_binding_energy(Z, A)
            # 显示 MATLAB 计算结果
        else:
            # 使用 Python 回退计算
            result = self.physics.calculate_binding_energy(Z, A)
```

## MATLAB 函数详细说明

### 1. binding_energy.m

**功能**: 计算核结合能

**输入**:
- `Z`: 原子序数
- `A`: 质量数

**输出**:
- `B`: 总结合能 (MeV)
- `B_per_nucleon`: 每核子结合能 (MeV)
- `terms`: 各项贡献（体积项、表面项、库仑项、不对称项、配对项）

**公式**: `B = a_v*A - a_s*A^(2/3) - a_c*Z²/A^(1/3) - a_a*(A-2Z)²/A + δ`

### 2. critical_mass.m

**功能**: 计算临界质量

**输入**:
- `Z`: 原子序数
- `A`: 质量数
- `density`: 材料密度 (kg/m³)
- `geometry`: 几何形状 ('sphere', 'cylinder', 'slab')

**输出**:
- `M_critical`: 临界质量 (kg)
- `R_critical`: 临界半径/尺寸 (m)
- `k_eff`: 有效倍增因子
- `factors`: 四因子公式各项

**公式**: `k_eff = η × ε × p × f`

### 3. neutron_flux.m

**功能**: 计算中子通量和反应率

**输入**:
- `n`: 中子密度 (neutrons/m³)
- `v`: 中子速度 (m/s)
- `Sigma`: 宏观截面 (m⁻¹)
- `geometry`: 几何类型
- `dimensions`: 几何尺寸 (m)

**输出**:
- `phi`: 中子通量 (neutrons/m²/s)
- `reaction_rate`: 反应率 (reactions/m³/s)
- `flux_profile`: 空间通量分布

**公式**: `φ = nv`, `R = φΣ`

### 4. decay_chain.m

**功能**: 计算放射性衰变链

**输入**:
- `N0`: 初始原子数（向量）
- `lambda`: 衰变常数 (s⁻¹, 向量)
- `t`: 时间 (s)

**输出**:
- `N`: 时间 t 时的原子数
- `activity`: 活度 A(t) = λN(t) (Bq)
- `half_lives`: 半衰期 T_1/2 = ln(2)/λ (s)

**公式**: `N(t) = N₀e^(-λt)` (单核素)
         Bateman 方程（衰变链）

### 5. quantum_tunneling.m

**功能**: 计算量子隧穿概率

**输入**:
- `m`: 粒子质量 (kg)
- `V0`: 势垒高度 (J)
- `E`: 粒子能量 (J)
- `width`: 势垒宽度 (m)

**输出**:
- `T`: 透射系数
- `probability`: 隧穿概率
- `kappa`: 衰减常数 κ = √(2m(V-E))/ℏ

**公式**: `T = exp(-2κa)` (矩形势垒)

## 测试

运行测试脚本：

```bash
python3 matlab_nuclear_analysis/matlab_nuclear_interface.py
```

这将：
1. 尝试启动 MATLAB 引擎
2. 测试所有计算函数
3. 显示结果和使用的计算方法（MATLAB 或 Python 回退）

## 回退机制

如果 MATLAB 不可用，系统会自动使用 Python 回退实现：
- 所有函数都有 Python 版本
- 计算结果可能略有不同，但功能完整
- 结果中会标注 `method: 'Python_fallback'`

## 性能优势

使用 MATLAB 的优势：
- ✅ 高精度数值计算
- ✅ 优化的矩阵运算
- ✅ 丰富的科学计算工具箱
- ✅ 专业的核物理计算函数
- ✅ 更好的数值稳定性

## 故障排除

### 问题：无法启动 MATLAB 引擎

**错误**: `matlab.engine.MatlabExecutionError`

**解决方案**:
1. 检查 MATLAB 是否正确安装
2. 确认 MATLAB Engine for Python 已安装
3. 检查 MATLAB 路径是否正确

### 问题：找不到 MATLAB 函数

**错误**: `Undefined function`

**解决方案**:
1. 确认 `matlab_nuclear_analysis/` 目录存在
2. 检查 MATLAB 路径是否已添加
3. 验证函数文件名和函数名匹配

### 问题：数据类型转换错误

**错误**: `TypeError` 或 `ValueError`

**解决方案**:
- MATLAB 函数期望 `double` 类型
- Python `int` 会自动转换
- 确保数组维度正确

## 扩展功能

### 添加新的 MATLAB 函数

1. 在 `matlab_nuclear_analysis/` 中创建新的 `.m` 文件
2. 在 `matlab_nuclear_interface.py` 中添加 Python 包装方法
3. 添加回退 Python 实现
4. 更新文档

### 示例：添加新的计算函数

```matlab
% matlab_nuclear_analysis/new_calculation.m
function result = new_calculation(input1, input2)
    % Your MATLAB code here
    result = input1 + input2;
end
```

```python
# 在 matlab_nuclear_interface.py 中添加
def calculate_new_thing(self, input1: float, input2: float) -> Dict:
    if not self.matlab_available:
        return self._fallback_new_thing(input1, input2)
    
    result = self.engine.new_calculation(float(input1), float(input2))
    return {'result': float(result), 'method': 'MATLAB'}
```

## 总结

✅ **已完成**:
- MATLAB 核物理分析函数库（5个核心函数）
- Python-MATLAB 接口
- 回退机制
- 测试脚本
- 完整文档

✅ **功能**:
- 结合能计算
- 临界质量计算
- 中子通量计算
- 衰变链计算
- 量子隧穿计算

现在 Oppenheimer AI 可以使用 MATLAB 进行高精度的核物理数据分析！

