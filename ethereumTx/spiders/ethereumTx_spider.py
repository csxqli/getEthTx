import scrapy
import re
from bs4 import BeautifulSoup
from ethereumTx.items import EthereumtxItem, BlockItem
# config
startBlock = 4000000
blockNum = 10
mainUrl = 'https://etherscan.io/'
class EthereumTxSpider(scrapy.Spider):
    name = "ethereumTx"
    def start_requests(self):
        global startBlock, blockNum
        # Get Interval transactions
        basicUrl = 'https://etherscan.io/txsInternal?block='
        # basicUrl = 'https://etherscan.io/txs?block='
        urls = []
        for i in range(blockNum):
            urls.append(basicUrl+str(startBlock+i)+'&p=1')
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parseInternal)
        # For transactions
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parseInternal)
    # Get Contract Interval transactions
    def parseInternal(self, response):
        global mainUrl
        page = re.search("(=)(.*)(&)",response.url).group(2)
        soup = BeautifulSoup(response.body.decode('utf-8'),'lxml')
        if int(response.url.split("=")[-1]) == 1:
            # A total of 69 transactions found 
            txNum = soup.find(string=re.compile("Total")).split(" ")[3]
            item = BlockItem()
            item['b'] = page
            item['n'] = txNum
            item['name'] = 'block'
            yield item
        for block in soup.find_all(src=re.compile("\/green-arrow-right.png")):
            item = EthereumtxItem()
            if block is not None:
                try:
                    item['name'] = 'tx'
                    # Transfer
                    item['s'] = block.previous_sibling.previous_sibling.a["href"].split("/")[-1]
                    #.split("/")[-1]
                    txInternalType = block.find_parent("td").previous_sibling.get_text()
                    if txInternalType == "create":
                        item['t'] = 1
                    elif txInternalType == "call":
                        item['t'] = 2
                    elif txInternalType == "suicide":
                        item['t'] = 0
                    elif txInternalType == "callcode":
                        print(page)
                        print(txInternalType)
                        item['t'] = 3
                    else:
                        item['t'] = 4
                        print(page)
                        print(txInternalType)
                    if block.find_parent("td").next_sibling.a or block.find_parent("td").next_sibling.span:
                        if txInternalType == "create":
                            item['r'] = block.find_parent("td").next_sibling.a["href"].split("/")[-1]
                        else:
                            item['r'] = block.find_parent("td").next_sibling.span.a["href"].split("/")[-1]
                    else:
                        item['r'] = "fail"
                    
                    item['v'] = block.find_parent("td").next_sibling.next_sibling.get_text().split(" ")[0]
                    item['b'] = page
                    yield item
                except:
                    print('except')
                    pass
        
        if soup.find("a", "btn btn-default btn-xs logout") != None:
            nextPage = soup.find("a", "btn btn-default btn-xs logout")["href"]
            if nextPage != '#':
                nextUrl = mainUrl+nextPage
                yield scrapy.Request(url=nextUrl, callback=self.parseInternal)
        
    def parse(self, response):
        global mainUrl
        page = re.search("(=)(.*)(&)",response.url).group(2)
        soup = BeautifulSoup(response.body.decode('utf-8'),'lxml')
        if int(response.url.split("=")[-1]) == 1:
            # A total of 69 transactions found 
            txNum = soup.find(string=re.compile("total")).split(" ")[3]
            item = BlockItem()
            item['b'] = page
            item['n'] = txNum
            item['name'] = 'block'
            yield item
        for block in soup.find_all(href=re.compile("\/block\/")):
            item = EthereumtxItem()
            try:
                item['name']= 'tx'
                # Transfer
                item['t'] = 0
                item['s'] = block.find_parent("td").next_sibling.next_sibling.span.a["href"].split("/")[-1]
                if block.find_parent("td").next_sibling.next_sibling.next_sibling.next_sibling.span:
                    if block.find_parent("td").next_sibling.next_sibling.next_sibling.next_sibling.i:
                        # Contract Invoke
                        item['t'] = 2
                    item['r'] = block.find_parent("td").next_sibling.next_sibling.next_sibling.next_sibling.span.a["href"].split("/")[-1]
                else:
                    # Contract Creation
                    item['t'] = 1
                    item['r'] = block.find_parent("td").next_sibling.next_sibling.next_sibling.next_sibling.a["href"].split("/")[-1]
                item['v'] = block.find_parent("td").next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.get_text().split(" ")[0]
                item['b'] = page
                print('except')
                yield item
            except:
                pass
        if soup.find("a", "btn btn-default btn-xs logout") != None:
            nextPage = soup.find("a", "btn btn-default btn-xs logout")["href"]
            if nextPage != '#':
                nextUrl = mainUrl+nextPage
                yield scrapy.Request(url=nextUrl, callback=self.parse)

        
