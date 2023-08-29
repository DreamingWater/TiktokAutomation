# Lenovo-"Xie Yan"



def tk_require_comments():
    import requests
    import os

    from lxml import etree

    url = 'https://www.tiktok.com/@lilaslea_/video/7227469399572221190'
    proxies = {
        'http': f'socks5h://127.0.0.1:7890',
        'https': f'socks5h://127.0.0.1:7890',
    }
    # 设置环境变量
    os.environ['HTTP_PROXY'] = proxies['http']
    os.environ['HTTPS_PROXY'] = proxies['https']

    # 使用 requests 库发送请求
    response = requests.get(url=url)
    response.encoding = 'UTF-8'
    if '好像不可以' in response:
        print( 'yes')
    # 解析响应
    html = etree.HTML(response.text)
    comments = html.xpath('.//div[contains(@class,"tiktok-1qp5gj2-DivCommentListContainer ekjxngi3")]')  # video data 组件集合
    for comment in comments:
        res = comment.xpath('.//p[@data-e2e = "comment-level-1"]/span/text()')
        print(res)
    birth_month_pattern= './/div[contains(@class,"DivCommentItemContainer")]'
    birth_month_pattern= './/p[contains(@class,"PCommentText")]/span/text()'