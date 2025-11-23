"""
Setup NPAT Database
下载 NPAT 所需的核数据数据库文件
"""

def setup_npat_database():
    """下载 NPAT 核数据数据库"""
    try:
        import npat
        
        print("=" * 60)
        print("NPAT 数据库设置")
        print("=" * 60)
        print("\n正在下载 NPAT 核数据数据库...")
        print("这可能需要一些时间，请耐心等待...\n")
        
        # 下载所有数据库
        npat.download("all", True)
        
        print("\n" + "=" * 60)
        print("✓ NPAT 数据库下载完成！")
        print("=" * 60)
        print("\n现在可以使用 NPAT 进行核物理分析了。")
        
    except ImportError:
        print("错误: NPAT 未安装")
        print("请运行: pip install npat")
    except Exception as e:
        print(f"错误: {e}")
        print("\n如果下载失败，可以手动下载数据库文件。")
        print("请参考 NPAT 文档了解详细信息。")


if __name__ == "__main__":
    setup_npat_database()

