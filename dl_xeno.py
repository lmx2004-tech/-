#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xeno-canto 鸟类数据集爬虫
爬取 https://xeno-canto.org 上的鸟类录音数据
"""

import requests
import time
import random
import csv
from pathlib import Path
import logging
from typing import Dict, List, Optional
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import concurrent.futures

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class XenoCantoScraper:
    def __init__(self, output_dir: str = "xeno_canto_data"):
        """
        初始化爬虫
        
        Args:
            output_dir: 输出目录
        """
        self.base_url = "https://xeno-canto.org"
        self.api_url = "https://xeno-canto.org/api/2/recordings"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # 设置日志
        self.setup_logging()
        
        # 创建session
        self.session = self.create_session()
        
        # 反爬虫策略
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
        
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        # 统计信息
        self.total_downloaded = 0
        self.failed_downloads = 0
        
    def setup_logging(self):
        """设置日志"""
        log_file = self.output_dir / "scraper.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def create_session(self):
        """创建带重试机制的session"""
        session = requests.Session()
        
        # 设置重试策略
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
        
    def get_random_headers(self):
        """获取随机请求头"""
        headers = self.headers.copy()
        headers['User-Agent'] = random.choice(self.user_agents)
        return headers
        
    def random_delay(self, min_delay: float = 0.5, max_delay: float = 2.0):
        """减少延迟时间"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        
    def search_recordings(self, query: str = "bird", page: int = 1) -> Optional[Dict]:
        """
        搜索录音数据
        
        Args:
            query: 搜索关键词
            page: 页码
            
        Returns:
            API响应数据
        """
        params = {
            'query': query,
            'page': page
        }
        
        try:
            response = self.session.get(
                self.api_url,
                params=params,
                headers=self.get_random_headers(),
                timeout=30,
                verify=False
            )
            
            if response.status_code == 200:
                data = response.json()
                self.logger.info(f"成功获取第 {page} 页数据，共 {data.get('numRecordings', 0)} 条记录")
                return data
            else:
                self.logger.error(f"请求失败，状态码: {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"搜索录音时出错: {str(e)}")
            return None
            
    def download_audio(self, recording: Dict, audio_dir: Path) -> bool:
        """
        下载音频文件
        
        Args:
            recording: 录音信息
            audio_dir: 音频保存目录
            
        Returns:
            是否下载成功
        """
        try:
            file_url = recording.get('file')
            if not file_url:
                self.logger.warning(f"录音 {recording.get('id')} 没有音频文件URL")
                return False
                
            # 创建文件名
            filename = f"{recording.get('id')}_{recording.get('gen')}_{recording.get('sp')}.mp3"
            filename = "".join(c for c in filename if c.isalnum() or c in "._-")
            filepath = audio_dir / filename
            
            # 检查文件是否已存在
            if filepath.exists():
                self.logger.info(f"文件已存在，跳过: {filename}")
                return True
                
            # 下载文件
            response = self.session.get(
                file_url,
                headers=self.get_random_headers(),
                timeout=60,
                stream=True,
                verify=False
            )
            
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                            
                self.logger.info(f"成功下载: {filename}")
                self.total_downloaded += 1
                return True
            else:
                self.logger.error(f"下载失败，状态码 {response.status_code}: {file_url}")
                return False
                
        except Exception as e:
            self.logger.error(f"下载音频时出错: {str(e)}")
            self.failed_downloads += 1
            return False
            
    def download_audio_multithreaded(self, recordings: List[Dict], audio_dir: Path):
        """
        使用多线程下载音频文件

        Args:
            recordings: 录音信息列表
            audio_dir: 音频保存目录
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_recording = {
                executor.submit(self.download_audio, recording, audio_dir): recording for recording in recordings
            }
            for future in concurrent.futures.as_completed(future_to_recording):
                recording = future_to_recording[future]
                try:
                    future.result()
                except Exception as e:
                    self.logger.error(f"音频下载失败: {recording.get('id')} - {str(e)}")

    def save_metadata(self, recordings: List[Dict], csv_file: Path):
        """
        保存元数据到CSV文件
        
        Args:
            recordings: 录音数据列表
            csv_file: CSV文件路径
        """
        try:
            # 如果文件不存在，创建并写入表头
            file_exists = csv_file.exists()
            
            with open(csv_file, 'a', newline='', encoding='utf-8') as f:
                if recordings:
                    fieldnames = recordings[0].keys()
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    
                    if not file_exists:
                        writer.writeheader()
                        
                    for recording in recordings:
                        writer.writerow(recording)
                        
            self.logger.info(f"元数据已保存到: {csv_file}")
            
        except Exception as e:
            self.logger.error(f"保存元数据时出错: {str(e)}")
            
    def scrape_all_data(self, query: str = "bird", max_pages: int = None, download_audio: bool = True):
        """
        爬取所有数据
        
        Args:
            query: 搜索关键词
            max_pages: 最大页数限制
            download_audio: 是否下载音频文件
        """
        self.logger.info(f"开始爬取数据，查询: '{query}'")
        
        # 创建子目录
        audio_dir = self.output_dir / "audio"
        if download_audio:
            audio_dir.mkdir(exist_ok=True)
            
        csv_file = self.output_dir / f"metadata_{query}.csv"
        
        page = 1
        total_recordings = 0
        
        while True:
            self.logger.info(f"正在处理第 {page} 页...")
            
            # 获取当前页数据
            data = self.search_recordings(query, page)
            if not data:
                self.logger.error(f"获取第 {page} 页数据失败")
                break
                
            recordings = data.get('recordings', [])
            if not recordings:
                self.logger.info("没有更多数据，爬取完成")
                break
                
            # 保存元数据
            self.save_metadata(recordings, csv_file)
            total_recordings += len(recordings)
            
            # 下载音频文件
            if download_audio:
                self.logger.info("开始多线程下载音频文件...")
                self.download_audio_multithreaded(recordings, audio_dir)
                
            # 检查是否达到最大页数
            if max_pages and page >= max_pages:
                self.logger.info(f"达到最大页数限制: {max_pages}")
                break
                
            # 检查是否还有更多页面
            num_pages = data.get('numPages', 0)
            if page >= num_pages:
                self.logger.info("已爬取所有页面")
                break
                
            page += 1
            
            # 页面间延迟
            self.random_delay(3, 8)
            
        # 输出统计信息
        self.logger.info("爬取完成！")
        self.logger.info(f"总记录数: {total_recordings}")
        self.logger.info(f"成功下载音频: {self.total_downloaded}")
        self.logger.info(f"下载失败: {self.failed_downloads}")
        self.logger.info(f"数据保存在: {self.output_dir}")
        
    def search_by_species(self, species_list: List[str], download_audio: bool = True):
        """
        按物种搜索
        
        Args:
            species_list: 物种名称列表
            download_audio: 是否下载音频
        """
        for species in species_list:
            self.logger.info(f"正在搜索物种: {species}")
            self.scrape_all_data(query=species, download_audio=download_audio)
            
            # 物种间延迟
            self.random_delay(10, 20)


def main():
    """主函数"""
    print("Xeno-canto 鸟类数据集爬虫")
    print("=" * 50)
    
    # 创建爬虫实例
    scraper = XenoCantoScraper("xeno_canto_dataset")
    
    try:
        # 选择爬取模式
        print("请选择爬取模式:")
        print("1. 爬取所有鸟类数据")
        print("2. 按特定物种搜索")
        print("3. 仅获取元数据（不下载音频）")
        
        choice = input("请输入选择 (1-3): ").strip()
        
        if choice == "1":
            # 爬取所有鸟类数据
            max_pages = input("输入最大页数限制（回车表示无限制）: ").strip()
            max_pages = int(max_pages) if max_pages else None
            scraper.scrape_all_data(query="bird", max_pages=max_pages)
            
        elif choice == "2":
            # 按物种搜索
            species_input = input("请输入物种名称（多个用逗号分隔）: ").strip()
            species_list = [s.strip() for s in species_input.split(',')]
            scraper.search_by_species(species_list)
            
        elif choice == "3":
            # 仅获取元数据
            max_pages = input("输入最大页数限制（回车表示无限制）: ").strip()
            max_pages = int(max_pages) if max_pages else None
            scraper.scrape_all_data(query="bird", max_pages=max_pages, download_audio=False)
            
        else:
            print("无效选择")
            
    except KeyboardInterrupt:
        print("\n用户中断，正在退出...")
    except Exception as e:
        print(f"发生错误: {str(e)}")
        

if __name__ == "__main__":
    main()