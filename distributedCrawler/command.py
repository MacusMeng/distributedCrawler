from scrapy import cmdline

# cmdline.execute("scrapy crawl douban".split())

# 红娘网站爬取
# redis:lpush hongniang:start_urls http://www.hongniang.com/index/search?sort=0&wh=0&sex=2&starage=0&province=0&city=0&marriage=0&edu=0&income=0&height=0&pro=0&house=0&child=0&xz=0&sx=0&mz=0&hometownprovince=0
#cmdline.execute("scrapy crawl hongniangSpider".split())

#lpush anju:start_urls https://wh.zu.anjuke.com/fangyuan/hongshana/
#mdline.execute("scrapy crawl anjuke".split())

#妹子图住抓取
#http://www.meizitu.com/
cmdline.execute("scrapy crawl Meizitu3W".split())

