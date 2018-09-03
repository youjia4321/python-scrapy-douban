# -*- coding: utf-8 -*-
import scrapy
from urllib import request
from PIL import Image

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://accounts.douban.com/login']
    login_url = 'https://accounts.douban.com/login'
    profile_url = 'https://www.douban.com/people/161614413/'
    edit_url = 'https://www.douban.com/j/people/161614413/edit_signature'
    def parse(self, response):
        formdata = {
            'source': 'index_nav',
            'redir': 'https://www.douban.com/',
            'remember': 'on',
            'login': '登录'
        }
        form_email = input('输入豆瓣账号：')
        form_password = input('输入豆瓣密码：')
        formdata['form_email'] = form_email
        formdata['form_password'] = form_password
        captcha_url = response.css('img#captcha_image::attr(src)').get()
        if captcha_url:
            captcha = self.regonize_captcha(captcha_url)
            formdata['captcha-solution'] = captcha
            captcha_id = response.xpath('//input[@name="captcha-id"]/@value').get()
            formdata['captcha-id'] = captcha_id
            # 打印出formdata中的参数是否正确
            # print('#######################')
            # print(formdata)
            # print('#######################')
        yield scrapy.FormRequest(url=self.login_url, formdata=formdata, callback=self.parse_after_login)

        
    def parse_after_login(self, response):
        if response.url == 'https://www.douban.com/':
            profile_url = 'https://www.douban.com/people/161614413/'
            yield scrapy.Request(url=profile_url, callback=self.parse_profile)
        else:
            print('登录失败!')

    def parse_profile(self, response):
        if response.url == self.profile_url:
            print('进入到个人主页，修改个性签名...')
            formdata = {}
            ck = response.xpath('//input[@name="ck"]/@value').get()
            formdata['ck'] = ck
            signature = input('输入修改个性签名的内容：')
            formdata['signature'] = signature
            yield scrapy.FormRequest(url=self.edit_url, formdata=formdata, callback=self.parse_edit_url)
        else:
            print('没有进入到个人主页！')
        
    def parse_edit_url(self, response):
        if response.url == self.edit_url:
            print('修改成功！')
        else:
            print('修改失败！')

    def regonize_captcha(self, img_url):
        request.urlretrieve(img_url, 'captcha.png')
        image = Image.open('captcha.png')
        image.show()
        captcha = input('请输入验证码：')
        return captcha




'''
登录到豆瓣网的post请求数据data
source:index_nav
redir:https://www.douban.com/
form_email:xxxxxxxxx
form_password:**********
captcha-solution:neeada
captcha-id:prEeRsBo3GH0U62DevpIGPOC:en
remember:on
login:登录
'''