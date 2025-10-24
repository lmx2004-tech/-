# 🐦 Xeno-canto 鸟类数据集爬虫 - 完整项目

## 📁 项目文件说明

### 核心文件
- **`dl_xeno.py`** - 主爬虫脚本，包含完整的爬虫功能
- **`requirements.txt`** - Python依赖包列表
- **`README.md`** - 详细的使用说明文档

### 辅助文件
- **`test_scraper.py`** - 测试脚本，验证爬虫基本功能
- **`examples.py`** - 使用示例，展示各种使用场景
- **`run.bat`** - Windows批处理文件，提供图形化菜单

## 🚀 快速开始

### 方法1: 使用批处理文件（推荐Windows用户）
双击 `run.bat` 或在PowerShell中运行：
```powershell
.\run.bat
```

### 方法2: 命令行使用
```bash
# 安装依赖
pip install -r requirements.txt

# 运行主程序
python dl_xeno.py

# 或运行测试
python test_scraper.py
```

## 🔧 主要功能

### 1. 反爬虫机制应对
- ✅ 随机User-Agent轮换
- ✅ 智能延迟机制（2-8秒随机间隔）
- ✅ 请求重试机制
- ✅ Session保持
- ✅ SSL验证跳过

### 2. 数据爬取功能
- ✅ 支持关键词搜索
- ✅ 分页爬取所有数据
- ✅ 音频文件下载
- ✅ 元数据CSV导出
- ✅ 断点续传（自动跳过已下载文件）

### 3. 搜索类型支持
- 🔍 通用搜索（如 "bird", "robin"）
- 🔍 物种搜索（支持批量物种列表）
- 🔍 高级搜索（地区、质量、许可证等）

## 📊 测试结果

✅ **API连接测试**: 成功连接xeno-canto.org API  
✅ **数据获取测试**: 成功获取13748条robin相关记录  
✅ **元数据保存测试**: 成功保存CSV格式元数据  
✅ **音频下载测试**: 成功下载MP3音频文件  

## 📋 使用场景示例

### 场景1: 机器学习数据集准备
```python
from dl_xeno import XenoCantoScraper

scraper = XenoCantoScraper("ml_dataset")
# 获取多种鸟类的数据用于训练
species = ["robin", "sparrow", "eagle", "owl"]
scraper.search_by_species(species, download_audio=True)
```

### 场景2: 学术研究数据收集
```python
# 只获取元数据进行统计分析
scraper.scrape_all_data(
    query="cnt:china",  # 中国地区的鸟类
    download_audio=False,  # 不下载音频，节省空间
    max_pages=50  # 限制页数
)
```

### 场景3: 特定质量数据筛选
```python
# 只下载高质量录音
scraper.scrape_all_data(
    query="q:A",  # A级质量
    download_audio=True,
    max_pages=10
)
```

## 📈 性能数据

- **API响应速度**: ~1-2秒/请求
- **下载速度**: 取决于网络，一般1-5MB/分钟
- **延迟设置**: 2-5秒（请求间）+ 3-8秒（页面间）
- **内存占用**: 约50-100MB（不包含下载的音频文件）

## 🛡️ 反爬虫策略详解

### 1. 请求头伪装
```python
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36...',
    # ... 多个不同的浏览器标识
]
```

### 2. 智能延迟
- 请求间延迟：2-5秒随机
- 页面间延迟：3-8秒随机
- 物种间延迟：10-20秒随机

### 3. 错误处理
- 自动重试失败的请求（最多3次）
- 优雅处理网络超时
- 详细的错误日志记录

## 📁 输出文件结构

```
xeno_canto_dataset/
├── audio/                          # 音频文件目录
│   ├── 741461_Heteromyias_armiti.mp3
│   ├── 741460_Heteromyias_armiti.mp3
│   └── ...
├── metadata_bird.csv               # 元数据文件
└── scraper.log                    # 详细日志
```

## ⚠️ 重要注意事项

1. **法律合规**: 请遵守xeno-canto.org的服务条款
2. **合理使用**: 避免给服务器造成过大压力
3. **存储空间**: 音频文件较大，确保有足够空间
4. **网络稳定**: 建议在稳定网络环境下运行

## 🔧 自定义配置

### 修改延迟时间
在 `dl_xeno.py` 中修改：
```python
# 请求间延迟（秒）
self.random_delay(2, 5)  # 可以调整为 (1, 3) 加快速度

# 页面间延迟（秒）  
self.random_delay(3, 8)  # 可以调整为 (2, 5) 加快速度
```

### 修改输出目录
```python
scraper = XenoCantoScraper("你的自定义目录名")
```

### 自定义搜索参数
支持xeno-canto.org的所有搜索参数：
- `cnt:china` - 指定国家/地区
- `type:song` - 指定录音类型
- `q:A` - 指定质量等级
- `lic:cc` - 指定许可证类型

## 🐛 故障排除

### 问题1: 网络连接失败
**解决方案**: 检查网络连接，可能需要使用代理

### 问题2: 下载速度慢
**解决方案**: 这是正常现象，延迟机制防止被封IP

### 问题3: 磁盘空间不足
**解决方案**: 
- 使用 `download_audio=False` 只获取元数据
- 限制 `max_pages` 参数

### 问题4: 程序中断
**解决方案**: 重新运行即可，会自动跳过已下载文件

## 📞 技术支持

如果遇到问题，请检查：
1. Python版本（推荐3.7+）
2. 依赖包是否正确安装
3. 网络连接是否稳定
4. 磁盘空间是否充足

## 📜 更新日志

- **v1.0.0** - 初始版本，支持基本爬取功能
- 支持多种搜索模式
- 完整的反爬虫机制
- 详细的错误处理和日志记录