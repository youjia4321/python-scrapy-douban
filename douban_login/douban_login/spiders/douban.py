# -*- coding: utf-8 -*-
import scrapy
from urllib import request
from PIL import Image

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['http://accounts.douban.com/login']
    login_url = 'http://accounts.douban.com/login'
    profile_url = 'https://www.douban.com/people/161614413/' # 这里是个人主页的url ，写你登录账户的url地址（需要修改）
    edit_url = 'https://www.douban.com/j/people/161614413/edit_signature' # 同上

    def parse(self, response):  # response已获取的网页源码
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
        # print(captcha_url)
        if captcha_url:
            captcha = self.regonize_captcha(captcha_url)
            formdata['captcha-solution'] = captcha
            captcha_id = response.xpath('//input[@name="captcha-id"]/@value').get()
            formdata['captcha-id'] = captcha_id
            # 发送一个请求, post请求是FormRequest
        yield scrapy.FormRequest(url=self.login_url, formdata=formdata,callback=self.parse_after_login)

    def parse_after_login(self, response):
        if response.url == 'https://www.douban.com/':
            print('登录成功!')
            # get方法请求使用Request
            yield scrapy.Request(url=self.profile_url, callback=self.parse_profile)
        else:
            print('登录失败!')


    def parse_profile(self, response):
        print(response.url)
        if response.url == self.profile_url:
            print('进入到个人主页，修改个性签名...')
            formdata = {}
            ck = response.xpath('//input[@name="ck"]/@value').get()
            signature = input('输入修改个性签名的内容：')
            formdata['signature'] = signature
            formdata['ck'] = ck
            yield scrapy.FormRequest(url=self.edit_url, formdata=formdata, callback=self.parse_edit)
        else:
            print('没有进入到个人主页！')


    def parse_edit(self, response):
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
