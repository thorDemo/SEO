# -*- coding: utf-8 -*-

# Scrapy settings for junshi_news project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
DOWNLOAD_DELAY = 0.25   # 250MS 延迟抓取，防止banc
CONCURRENT_REQUESTS = 32   # 开启线程数量，默认16
AUTOTHROTTLE_START_DELAY = 3  #开始下载时限速并延迟时间
AUTOTHROTTLE_MAX_DELAY = 60   #高并发请求时最大延迟时间

BOT_NAME = 'junshi_news'

SPIDER_MODULES = ['junshi_news.spiders']
NEWSPIDER_MODULE = 'junshi_news.spiders'

DOWNLOADER_MIDDLEWARES = {
   # 'myproxies.middlewares.MyCustomDownloaderMiddleware': 543,
   # 'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware':543,
   # 'novel.middlewares.NovelDownloaderMiddleware':125,
   'junshi_news.middlewares.RandomUserAgentMiddleware': 410,
   'scrapy.downloadmiddlewares.useragent.UserAgentMiddleware': None,
}

ITEM_PIPELINES = {
   'junshi_news.pipelines.JunshiNewsPipeline': 300,
}

MYSQL_HOST = '103.56.136.105'
MYSQL_DBNAME = 'news'
MYSQL_USER = 'root'
MYSQL_PASSWD = 'password'
MYSQL_PORT = 3306

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'junshi_news (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'junshi_news.middlewares.JunshiNewsSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'junshi_news.middlewares.JunshiNewsDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'junshi_news.pipelines.JunshiNewsPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
