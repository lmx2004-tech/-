# Xeno-canto 鸟类数据集爬虫

这个脚本可以自动爬取 [xeno-canto.org](https://xeno-canto.org) 网站上的鸟类录音数据集。

## 功能特点

- 支持按关键词搜索鸟类录音
- 自动下载音频文件和元数据
- 内置反爬虫机制应对网站限制
- 支持断点续传，避免重复下载
- 详细的日志记录和错误处理
- 支持按物种批量搜索

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本使用

直接运行脚本：

```bash
python dl_xeno.py
```

脚本会提供交互式菜单，让你选择：

1. **爬取所有鸟类数据** - 搜索关键词"bird"，获取所有相关录音
2. **按特定物种搜索** - 输入具体的鸟类物种名称进行搜索
3. **仅获取元数据** - 只下载CSV格式的元数据，不下载音频文件

### 编程使用

```python
from dl_xeno import XenoCantoScraper

# 创建爬虫实例
scraper = XenoCantoScraper("output_directory")

# 爬取特定查询的数据
scraper.scrape_all_data(query="robin", max_pages=10, download_audio=True)

# 按物种列表搜索
species_list = ["robin", "sparrow", "eagle"]
scraper.search_by_species(species_list, download_audio=False)
```

## 反爬虫策略

脚本内置了多种反爬虫策略：

- **随机User-Agent**: 模拟不同浏览器访问
- **随机延迟**: 请求间随机等待，避免频率过高
- **重试机制**: 自动重试失败的请求
- **Session保持**: 维持会话状态
- **SSL验证跳过**: 避免证书问题

## 输出结构

```
xeno_canto_dataset/
├── audio/                 # 音频文件目录
│   ├── 12345_Turdus_migratorius.mp3
│   └── ...
├── metadata_bird.csv      # 元数据文件
└── scraper.log           # 日志文件
```

## 注意事项

1. **尊重网站服务条款**: 请合理使用，避免对服务器造成过大压力
2. **存储空间**: 音频文件较大，确保有足够的磁盘空间
3. **网络稳定**: 建议在稳定的网络环境下运行
4. **中断恢复**: 脚本支持中断后重新运行，会自动跳过已下载的文件

## 常见问题

### Q: 为什么下载速度很慢？
A: 脚本内置了延迟机制防止被封IP，这是正常现象。

### Q: 如何只下载特定鸟类的数据？
A: 选择模式2，输入具体的物种名称，如"robin"、"sparrow"等。

### Q: 如何查看下载进度？
A: 脚本会在控制台显示实时进度，详细信息记录在log文件中。

### Q: 遇到网络错误怎么办？
A: 脚本有自动重试机制，如果持续失败，检查网络连接或稍后重试。

## 技术参数

- 默认延迟：2-5秒（请求间）、3-8秒（页面间）
- 重试次数：3次
- 超时时间：30秒（API请求）、60秒（文件下载）
- 支持的文件格式：主要是MP3格式的音频文件