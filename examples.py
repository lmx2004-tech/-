#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用示例 - 展示如何使用Xeno-canto爬虫的各种功能
"""

from dl_xeno import XenoCantoScraper

def example_1_basic_usage():
    """示例1: 基本使用 - 爬取少量数据进行测试"""
    print("=== 示例1: 基本使用 ===")
    
    scraper = XenoCantoScraper("example_output")
    
    # 只爬取前3页的robin数据，用于测试
    scraper.scrape_all_data(
        query="robin", 
        max_pages=3, 
        download_audio=True
    )

def example_2_metadata_only():
    """示例2: 只获取元数据，不下载音频"""
    print("=== 示例2: 仅获取元数据 ===")
    
    scraper = XenoCantoScraper("metadata_only")
    
    # 获取前10页的数据，但不下载音频文件
    scraper.scrape_all_data(
        query="bird", 
        max_pages=10, 
        download_audio=False
    )

def example_3_specific_species():
    """示例3: 搜索特定物种"""
    print("=== 示例3: 特定物种搜索 ===")
    
    scraper = XenoCantoScraper("species_data")
    
    # 搜索特定物种列表
    species_list = [
        "sparrow",      # 麻雀
        "eagle",        # 鹰
        "owl",          # 猫头鹰
        "crow",         # 乌鸦
        "peacock"       # 孔雀
    ]
    
    # 每个物种最多爬取2页数据
    for species in species_list:
        print(f"正在搜索: {species}")
        scraper.scrape_all_data(
            query=species, 
            max_pages=2, 
            download_audio=True
        )

def example_4_advanced_search():
    """示例4: 高级搜索 - 使用更复杂的查询"""
    print("=== 示例4: 高级搜索 ===")
    
    scraper = XenoCantoScraper("advanced_search")
    
    # 可以使用更复杂的查询参数
    # 注意：xeno-canto.org支持各种搜索参数
    advanced_queries = [
        "cnt:china",           # 中国的鸟类
        "type:song",           # 只要歌声类型的录音
        "q:A",                 # 只要A级质量的录音
        "lic:cc"               # 只要创作共用许可的录音
    ]
    
    for query in advanced_queries:
        print(f"搜索查询: {query}")
        scraper.scrape_all_data(
            query=query, 
            max_pages=1,  # 每个查询只要1页数据做示例
            download_audio=False  # 高级搜索示例不下载音频
        )

def example_5_custom_scraper():
    """示例5: 自定义爬虫设置"""
    print("=== 示例5: 自定义设置 ===")
    
    # 创建自定义输出目录的爬虫
    scraper = XenoCantoScraper("custom_birds_dataset")
    
    # 直接使用API搜索
    print("直接调用API...")
    data = scraper.search_recordings("nightingale", page=1)
    
    if data:
        print(f"找到 {data.get('numRecordings')} 条夜莺录音")
        recordings = data.get('recordings', [])
        
        if recordings:
            # 保存前10条记录的元数据
            csv_file = scraper.output_dir / "nightingale_sample.csv"
            scraper.save_metadata(recordings[:10], csv_file)
            print(f"样本数据已保存到: {csv_file}")
            
            # 手动下载第一个音频文件
            audio_dir = scraper.output_dir / "audio"
            audio_dir.mkdir(exist_ok=True)
            
            if scraper.download_audio(recordings[0], audio_dir):
                print("成功下载了一个样本音频文件")

def main():
    """主函数 - 运行所有示例"""
    print("Xeno-canto 爬虫使用示例")
    print("=" * 50)
    
    examples = [
        ("基本使用", example_1_basic_usage),
        ("仅获取元数据", example_2_metadata_only),
        ("特定物种搜索", example_3_specific_species),
        ("高级搜索", example_4_advanced_search),
        ("自定义设置", example_5_custom_scraper)
    ]
    
    print("可用示例:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")
    print("0. 运行所有示例")
    
    try:
        choice = input("\n请选择要运行的示例 (0-5): ").strip()
        
        if choice == "0":
            # 运行所有示例
            for name, func in examples:
                print(f"\n{'='*20} {name} {'='*20}")
                func()
                print("示例完成，等待3秒...")
                import time
                time.sleep(3)
        elif choice in ["1", "2", "3", "4", "5"]:
            idx = int(choice) - 1
            name, func = examples[idx]
            print(f"\n{'='*20} {name} {'='*20}")
            func()
        else:
            print("无效选择")
            
    except KeyboardInterrupt:
        print("\n用户中断")
    except Exception as e:
        print(f"运行示例时出错: {e}")

if __name__ == "__main__":
    main()