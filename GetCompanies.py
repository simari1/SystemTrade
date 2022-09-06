from pyquery import PyQuery
q = PyQuery('https://kabutan.jp/stock/?code=7203')
sector = q.find('#stockinfo_i2 div a')[0].text
unit = q.find('#stockinfo_i2 dl dd')[1].text
per = q.find('#stockinfo_i3 td:nth-child(1)')[0].text
pbr = q.find('#stockinfo_i3 td')[0].text
turnover = q.find('#kobetsu_left td')[12].text

q = PyQuery('https://minkabu.jp/stock/7203')
market_value = q.find('ly_vamd_inner ly_colsize_9_fix fwb tar wsnw')[0].text
number_of_shares = q.find('ly_vamd_inner ly_colsize_9_fix fwb tar wsnw')[0].text

print("test")