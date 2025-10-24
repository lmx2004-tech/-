#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 验证Xeno-canto爬虫基本功能
"""

from dl_xeno import XenoCantoScraper

def test_basic_functionality():
    """测试基本功能"""
    print("开始测试 Xeno-canto 爬虫基本功能...")
    
    # 创建爬虫实例
    scraper = XenoCantoScraper("test_output")
    
    print("1. 测试API连接...")
    # 测试获取第一页数据
    data = scraper.search_recordings(query="robin", page=1)
    
    if data:
        print(f"✓ API连接成功！找到 {data.get('numRecordings', 0)} 条robin相关记录")
        print(f"✓ 总页数: {data.get('numPages', 0)}")
        
        recordings = data.get('recordings', [])
        if recordings:
            print("✓ 第一条记录示例:")
            first_record = recordings[0]
            print(f"  - ID: {first_record.get('id')}")
            print(f"  - 物种: {first_record.get('gen')} {first_record.get('sp')}")
            print(f"  - 录音地点: {first_record.get('loc')}")
            print(f"  - 文件URL: {first_record.get('file')}")
            
        print("\n2. 测试元数据保存...")
        # 测试保存少量元数据
        csv_file = scraper.output_dir / "test_metadata.csv"
        scraper.save_metadata(recordings[:5], csv_file)  # 只保存前5条
        print(f"✓ 元数据已保存到: {csv_file}")
        
        print("\n3. 测试音频下载 (仅下载1个文件)...")
        # 测试下载一个音频文件
        audio_dir = scraper.output_dir / "test_audio"
        audio_dir.mkdir(exist_ok=True)
        
        success = scraper.download_audio(recordings[0], audio_dir)
        if success:
            print("✓ 音频文件下载测试成功")
        else:
            print("⚠ 音频文件下载测试失败，但这可能是网络问题")
            
    else:
        print("✗ API连接失败，请检查网络连接")
        return False
        
    print("\n" + "="*50)
    print("基本功能测试完成！")
    print("如果所有测试通过，说明脚本可以正常工作。")
    print("现在你可以运行主脚本: python dl_xeno.py")
    print("="*50)
    
    return True

if __name__ == "__main__":
    test_basic_functionality()