"""
MATLAB Installation Checker
检查 MATLAB 和 MATLAB Engine for Python 的安装状态
"""

import sys
import os
import subprocess

def check_matlab_installation():
    """检查 MATLAB 是否已安装"""
    print("=" * 60)
    print("MATLAB 安装检查")
    print("=" * 60)
    
    # 检查 MATLAB Engine for Python
    print("\n1. 检查 MATLAB Engine for Python...")
    try:
        import matlab.engine  # type: ignore
        print("   ✓ MATLAB Engine for Python 已安装")
        
        # 尝试启动 MATLAB
        print("\n2. 尝试启动 MATLAB 引擎...")
        try:
            eng = matlab.engine.start_matlab()
            version = eng.version()
            print(f"   ✓ MATLAB 引擎启动成功")
            print(f"   ✓ MATLAB 版本: {version}")
            eng.quit()
            return True
        except Exception as e:
            print(f"   ✗ MATLAB 引擎启动失败: {e}")
            return False
            
    except ImportError:
        print("   ✗ MATLAB Engine for Python 未安装")
        return False

def find_matlab_installation():
    """查找 MATLAB 安装位置"""
    print("\n3. 查找 MATLAB 安装位置...")
    
    # 常见的 MATLAB 安装路径
    common_paths = [
        "/Applications/MATLAB_R2024a.app",
        "/Applications/MATLAB_R2023b.app",
        "/Applications/MATLAB_R2023a.app",
        "/usr/local/MATLAB/R2024a",
        "/usr/local/MATLAB/R2023b",
        "/opt/MATLAB/R2024a",
        "/opt/MATLAB/R2023b",
    ]
    
    found_paths = []
    for path in common_paths:
        if os.path.exists(path):
            found_paths.append(path)
            print(f"   ✓ 找到: {path}")
    
    if not found_paths:
        print("   ✗ 未找到 MATLAB 安装")
        print("\n   请手动查找 MATLAB 安装位置:")
        print("   macOS: /Applications/MATLAB_R20XX.app")
        print("   Linux: /usr/local/MATLAB/R20XX 或 /opt/MATLAB/R20XX")
        print("   Windows: C:\\Program Files\\MATLAB\\R20XX")
        return None
    
    return found_paths[0]

def install_matlab_engine(matlab_path=None):
    """安装 MATLAB Engine for Python"""
    print("\n4. 安装 MATLAB Engine for Python...")
    
    if not matlab_path:
        matlab_path = find_matlab_installation()
    
    if not matlab_path:
        print("   ✗ 无法找到 MATLAB 安装，无法安装 Engine")
        return False
    
    # 查找 Python Engine 目录
    engine_path = os.path.join(matlab_path, "extern", "engines", "python")
    
    if not os.path.exists(engine_path):
        print(f"   ✗ 未找到 Engine 目录: {engine_path}")
        return False
    
    print(f"   ✓ 找到 Engine 目录: {engine_path}")
    print(f"\n   请手动运行以下命令安装:")
    print(f"   cd {engine_path}")
    print(f"   python3 setup.py install")
    print(f"   或")
    print(f"   python3 setup.py install --user")
    
    return False

def check_python_fallback():
    """检查 Python 回退实现"""
    print("\n5. 检查 Python 回退实现...")
    
    try:
        from matlab_nuclear_analysis.matlab_nuclear_interface import MATLABNuclearAnalysis
        
        # 测试回退功能
        analysis = MATLABNuclearAnalysis()
        
        if not analysis.matlab_available:
            print("   ✓ Python 回退实现可用")
            print("   ✓ 系统可以在没有 MATLAB 的情况下工作")
            
            # 测试一个计算
            result = analysis.calculate_binding_energy(92, 235)
            print(f"   ✓ 测试计算成功: U-235 结合能 = {result['binding_energy_MeV']:.2f} MeV")
            print(f"   ✓ 使用方法: {result['method']}")
            
            analysis.close()
            return True
        else:
            print("   ✓ MATLAB 可用，将使用 MATLAB 进行计算")
            analysis.close()
            return True
            
    except Exception as e:
        print(f"   ✗ Python 回退实现检查失败: {e}")
        return False

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("Oppenheimer AI - MATLAB 集成检查")
    print("=" * 60)
    
    # 检查 MATLAB Engine
    matlab_available = check_matlab_installation()
    
    # 检查 Python 回退
    python_fallback_ok = check_python_fallback()
    
    # 总结
    print("\n" + "=" * 60)
    print("检查结果总结")
    print("=" * 60)
    
    if matlab_available:
        print("\n✓ MATLAB 已安装并可用")
        print("  Oppenheimer AI 将使用 MATLAB 进行高精度计算")
    else:
        print("\n⚠ MATLAB 未安装或不可用")
        
        if python_fallback_ok:
            print("✓ Python 回退实现可用")
            print("  Oppenheimer AI 将使用 Python 进行计算")
            print("  功能完整，但精度可能略低于 MATLAB")
        else:
            print("✗ Python 回退实现不可用")
            print("  请检查 matlab_nuclear_interface.py 文件")
        
        # 提供安装指南
        print("\n" + "-" * 60)
        print("安装 MATLAB Engine for Python:")
        print("-" * 60)
        matlab_path = find_matlab_installation()
        if matlab_path:
            install_matlab_engine(matlab_path)
        else:
            print("\n1. 安装 MATLAB (如果尚未安装)")
            print("2. 找到 MATLAB 安装目录")
            print("3. 运行:")
            print("   cd matlabroot/extern/engines/python")
            print("   python3 setup.py install")
    
    print("\n" + "=" * 60)
    print("注意: matlabengine 不能通过 pip 安装")
    print("必须从 MATLAB 安装目录安装")
    print("=" * 60)

if __name__ == "__main__":
    main()

