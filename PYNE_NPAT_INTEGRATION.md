# PyNE 和 NPAT 集成指南

## 安装状态

✅ **PyNE**: 已安装 (pip 版本)
✅ **NPAT**: 已安装并可用
✅ **依赖**: pandas, matplotlib 已安装

## 重要：NPAT 数据库设置

NPAT 需要下载核数据数据库才能正常工作。首次使用前请运行：

```bash
cd /Users/amy/oppenheimer_env
source bin/activate
python3 setup_npat_database.py
```

或者直接在 Python 中：

```python
import npat
npat.download("all", True)
```

这将下载所需的核数据文件（可能需要一些时间）。

## 集成功能

### 1. NPAT (Nuclear Physics Analysis Tools)

NPAT 已成功集成到 `nuclear_physics.py` 中，提供以下功能：

#### `analyze_decay_chain_npat(Z, A, time_seconds, initial_activity=1.0)`
- **功能**: 使用 NPAT 分析放射性衰变链
- **参数**:
  - `Z`: 原子序数
  - `A`: 质量数
  - `time_seconds`: 衰变时间（秒）
  - `initial_activity`: 初始活度 (Bq, 可选，默认 1.0)
- **返回**: 包含衰变链信息的字典
- **格式**: NPAT 使用 "238U" 格式（质量数在前，无连字符）

**示例**:
```python
from nuclear_physics import NuclearPhysics

physics = NuclearPhysics()
result = physics.analyze_decay_chain_npat(92, 238, 3600)  # U-238, 1小时
```

#### `get_nuclide_data_npat(Z, A)`
- **功能**: 使用 NPAT 获取核素数据
- **参数**:
  - `Z`: 原子序数
  - `A`: 质量数
- **返回**: 包含核素信息的字典
- **格式**: NPAT 使用 "238U" 格式（质量数在前，无连字符）

**示例**:
```python
result = physics.get_nuclide_data_npat(92, 235)  # U-235
```

**注意**: 如果返回结果包含 `error: 'NPAT database not initialized'`，请运行数据库设置脚本。

### 2. PyNE (Nuclear Engineering Toolkit)

PyNE 已检测到，但 pip 版本可能功能有限。完整版本的 PyNE 需要从源码编译。

**当前状态**:
- ✅ PyNE 基础模块已导入
- ⚠️ 完整功能（nucname, data, material）可能需要完整安装

## 使用方法

### 在代码中检查库可用性

```python
from nuclear_physics import NuclearPhysics

physics = NuclearPhysics()

# 检查库是否可用
if physics.npat_available:
    print("NPAT 可用")
    result = physics.analyze_decay_chain_npat(92, 238, 3600)

if physics.pyne_available:
    print("PyNE 可用")
    # 使用 PyNE 功能
```

### 在 Oppenheimer GUI 中使用

可以在 `oppenheimer_gui.py` 中集成这些功能：

```python
# 在 calculate_nuclear_properties 方法中
if self.physics.npat_available:
    npat_data = self.physics.get_nuclide_data_npat(Z, A)
    if npat_data:
        # 显示 NPAT 数据
        result_text += f"\n\nNPAT 数据:\n{json.dumps(npat_data, indent=2)}"
```

## NPAT API 说明

### DecayChain
- **格式**: `DecayChain("238U", units='s', A0=1.0, time=3600)` (质量数在前)
- **用途**: 衰变链分析
- **参数**:
  - `parent`: 母核素，格式 "238U"
  - `units`: 时间单位 ('s', 'm', 'h', 'd', 'y')
  - `A0`: 初始活度 (Bq)
  - `time`: 衰变时间

### Isotope
- **格式**: `Isotope("238U")` (质量数在前，无连字符)
- **用途**: 核素数据访问
- **属性**: `half_life`, `decay_mode`, `stable` 等（需要数据库）

## 已知限制

1. **PyNE pip 版本**: 
   - pip 安装的 PyNE 可能是简化版本
   - 完整功能需要从源码编译安装

2. **NPAT API**:
   - 某些方法可能需要特定参数格式
   - 建议查阅 NPAT 文档了解详细 API

## 扩展建议

1. **添加更多 NPAT 功能**:
   - 光谱分析
   - 校准功能
   - 能量损失表征

2. **集成 PyNE 完整版本**:
   - 如果安装了完整 PyNE，可以添加更多功能
   - 核素名称转换
   - 材料管理
   - 数据查询

## 测试

运行测试：
```bash
cd /Users/amy/oppenheimer_env
source bin/activate
python3 -c "from nuclear_physics import NuclearPhysics; np = NuclearPhysics(); print('NPAT:', np.npat_available); print('PyNE:', np.pyne_available)"
```

## 总结

✅ NPAT 已成功集成并可用
✅ PyNE 已检测到（pip 版本）
✅ 所有依赖已安装
✅ 集成代码已添加到 `nuclear_physics.py`

Oppenheimer AI 现在可以使用 NPAT 进行核物理分析了！

