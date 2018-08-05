# -*- coding: utf-8 -*-
import scrapy
import json
from weibo.items import UserItem,UserRelationItem


class WeibocnSpider(scrapy.Spider):
    name = 'weibocn'
    allowed_domains = ['m.weibo.cn']
    # user_url = 'https://m.weibo.cn/p/index?containerid=230283{uid}_-_INFO&title=%25E5%259F%25BA%25E6%259C%25AC%25E8%25B5%2584%25E6%2596%2599&luicode=10000011&lfid=230283{uid}&display=0&retcode=6102'
    user_url = 'https://m.weibo.cn/api/container/getIndex?uid={uid}&type=uid&value={uid}&containerid=100505{uid}'
    follow_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{uid}&page={page}'
    fan_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{uid}&since_id={page}'
    star_uid = ['6177628278','2514127734','1366356590','6049590367','1795420390']

    def start_requests(self):
        for uid in self.star_uid:
            yield scrapy.Request(self.user_url.format(uid = uid),callback=self.parse_user)


    def parse_user(self, response):
        result = json.loads(response.text)
        if result.get('data').get('userInfo'):
            user_info = result.get('data').get('userInfo')
            user_item = UserItem()
            fild_map = {
                'id':'id',
                'name':'screen_name',
                'gender':'gender',
                'description':'description',
                'fans_count':'followers_count',
                'follows_count':'follow_count',
                'weibos_count':'statuses_count',
                'verified':'verified',
                'verified_reason':'verified_reason'
            }
            for field,attr in fild_map.items():
                user_item[field] = user_info.get(attr)
            yield user_item
            uid = user_info.get('id')
            yield scrapy.Request(self.follow_url.format(uid=uid,page=1),callback=self.parse_follows,meta={'page':1,'uid':'uid'})
            yield scrapy.Request(self.fan_url.format(uid=uid,page=1),callback=self.parse_fans,meta={'page':1,'uid':'uid'})





    def parse_follows(self, response):
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards') and len(result.get('data').get('cards')) and result.get('data').get('cards')[-1].get('card_group'):
            follows = result.get('data').get('cards')[-1].get('card_group')
            for follow in follows:
                if follow.get('user'):
                    uid = follow.get('user').get('id')
                    yield scrapy.Request(self.user_url.format(uid = uid),callback=self.parse_user)
            uid = response.meta.get('uid')
            page = response.meta.get('page') + 1
            yield scrapy.Request(self.follow_url.format(uid=uid,page=page),callback=self.parse_follows,meta={'page':page,'uid':'uid'})

    def parse_fans(self, response):
        result = json.loads(response.text)
        if result.get('ok') and result.get('data').get('cards') and len(result.get('data').get('cards')) and result.get('data').get('cards')[-1].get('card_group'):
            fans = result.get('data').get('cards')[-1].get('card_group')
            for fan in fans:
                if fan.get('user'):
                    uid = fan.get('user').get('id')
                    yield scrapy.Request(self.user_url.format(uid = uid),callback=self.parse_user)
            uid = response.meta.get('uid')
            page = response.meta.get('page') + 1
            yield scrapy.Request(self.fan_url.format(uid=uid,page=page),callback=self.parse_fans,meta={'page':page,'uid':'uid'})