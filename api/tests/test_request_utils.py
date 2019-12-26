# -*- coding: utf-8 -*-

from django.test import TestCase
from api.models import Entry
from api.request_utils import get_first_and_last_ids, IconGetter


class TestRequestUtils(TestCase):

    def setUp(self):
        for i in range(1, 5):
            Entry.objects.create(**{'url': 'https://google.com/', 'desc': 'Test {0}'.format(i)})

    def test_id_getter(self):
        last_four = Entry.get_last_four()
        start_id, end_id = get_first_and_last_ids(last_four)
        self.assertEqual(last_four[0].id, start_id)
        self.assertEqual(last_four[-1].id, end_id)

        # empty data
        start, end = get_first_and_last_ids([])
        self.assertEqual((start, end), (None, None))

    def test_icon_getter(self):
        test_string = b'<!DOCTYPE html><html class="tw-root--hover"><head><meta charset="utf-8"><title>Twitch</title><meta property=\'og:site_name\' content=\'Twitch\'><meta property=\'fb:app_id\' content=\'161273083968709\'><meta property=\'twitter:site\' content=\'@twitch\'><meta property=\'og:title\' content=\'Twitch\'><meta property=\'og:description\' content=\'Twitch is the world&#39;s leading video platform and community for gamers.\'><meta property=\'og:image\' content=\'https://static-cdn.jtvnw.net/ttv-static-metadata/twitch_logo3.jpg\'><meta property=\'og:url\' content=\'https://www.twitch.tv/directory\'><meta property=\'og:type\' content=\'website\'><link rel=\'canonical\' href=\'https://www.twitch.tv/directory\'><link rel=\'alternate\' href=\'https://m.twitch.tv/directory\'><link rel="icon" type="image/png" sizes="32x32" href="https://static.twitchcdn.net/assets/favicon-32-d6025c14e900565d6177.png"><link rel="icon" type="image/png" sizes="16x16" href="https://static.twitchcdn.net/assets/favicon-16-2d5d1f5ddd489ee10398.png"><link rel="dns-prefetch" href="https://api.twitch.tv/"><link rel="dns-prefetch" href="https://passport.twitch.tv/"><link rel="dns-prefetch" href="https://static-cdn.jtvnw.net/"><link rel="preconnect" href="https://api.twitch.tv/"><link rel="preconnect" href="https://static-cdn.jtvnw.net/"><link rel="dns-prefetch" href="https://gql.twitch.tv/"><link rel="dns-prefetch" href="https://cvp.twitch.tv/"><link rel="dns-prefetch" href="https://irc-ws.chat.twitch.tv/"><link rel="dns-prefetch" href="https://pubsub-edge.twitch.tv/"><link rel="dns-prefetch" href="https://static.twitchcdn.net/"><link rel="preconnect" href="https://gql.twitch.tv/"><link rel="preconnect" href="https://static.twitchcdn.net/"><link rel="preconnect" href="https://cvp.twitch.tv/"><link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml"></head><body><div id="root" class="root"><style>html{font-size:62.5%}body{font-size:1.2rem;background-color:#fafafa}.root,body,html{margin:0;overflow:hidden;width:100%;height:100%;display:-webkit-box;display:-ms-flexbox;display:flex;-ms-flex-direction:column;flex-direction:column;position:relative}body.dark-theme{background-color:#000}.shell-nav{background:#fff;height:5rem;width:100%;position:absolute;display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:stretch;-ms-flex-align:stretch;align-items:stretch}body.dark-theme .shell-nav{background:#18181b}html.desktop-login .shell-nav{display:none}.shell-nav__logo{padding-top:1.3rem;padding-left:1.3rem;display:inline-block;margin:0}.shell-nav__logo svg{fill:#9147ff}body.dark-theme .shell-nav__logo svg{fill:#9147ff}.shell-nav__link{padding:2rem;display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-pack:center;-ms-flex-pack:center;justify-content:center;-webkit-box-align:center;-ms-flex-align:center;align-items:center}.shell-nav__link-list{display:flex}.shell-nav__link::after{content:\'\';height:.4rem;background:rgba(0,0,0,.2);border-radius:2px}body.dark-theme .shell-nav__link::after{background:rgba(255,255,255,.2)}.shell-nav__link--discovery::after{width:6.9rem}.shell-nav__link--browse::after{width:5.9rem}.shell-nav__link--follow::after{width:7.6rem}.shell-nav__link--follow{display:none}body.logged-in .shell-nav__link--follow{display:-webkit-box;display:-ms-flexbox;display:flex}.shell-nav__ellipsis{width:5rem;display:-webkit-box;display:-ms-flexbox;display:flex;display:none;-webkit-box-pack:center;-ms-flex-pack:center;justify-content:center;-webkit-box-align:center;-ms-flex-align:center;align-items:center}.shell__svg--navmore{fill:rgba(255,255,255,.4);height:2rem}.shell-nav__search-container{-webkit-box-flex:1;-ms-flex-positive:1;flex-grow:1;display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center}.shell-nav__search{display:none;width:100%;max-width:40rem;height:3rem;margin:0 1rem;background:rgba(255,255,255,.4);border-radius:2px}.shell-nav__user-card{width:5rem;display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;justify-content:flex-end;box-sizing:border-box}.shell-nav__user-card-avatar{margin-right:1rem;width:3rem;height:3rem;background:#f2f2f2;-ms-flex-negative:0;flex-shrink:0;border-radius:2px}body.dark-theme .shell-nav__user-card-avatar{background:#242427}.shell-nav__user-auth{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center}body.logged-in .shell-nav__user-auth{display:none}.shell-nav__user-auth-button{display:-webkit-box;display:-ms-flexbox;display:flex;-webkit-box-align:center;-ms-flex-align:center;align-items:center;-webkit-box-pack:center;-ms-flex-pack:center;justify-content:center;height:3rem;margin-right:1rem;padding:.8rem;box-sizing:border-box;border-radius:2px}.shell-nav__user-auth-button--login{width:5.2rem}.shell-nav__user-auth-button--singup{width:6.1rem}.shell-nav__user-auth-button::after{content:\'\';width:100%;height:.4rem;border-radiu'
        icon_getter = IconGetter('https://www.twitch.tv/directory/')
        r = icon_getter.parse_content(test_string)
        self.assertIsNotNone(r)

        test_string_2 = b"""<html lang="en-US">
                        <head>
                        <title>SQL CASE Statement</title>
                        <meta charset="utf-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <meta name="Keywords" content="HTML,CSS,JavaScript,SQL,PHP,jQuery,XML,DOM,Bootstrap,Python,Java,Web development,W3C,tutorials,programming,training,learning,quiz,primer,lessons,references,examples,exercises,source code,colors,demos,tips">
                        <meta name="Description" content="Well organized and easy to understand Web building tutorials with lots of examples of how to use HTML, CSS, JavaScript, SQL, PHP, Python, Bootstrap, Java and XML.">
                        <link rel="icon" href="/favicon.ico" type="image/x-icon">
                        <link rel="stylesheet" href="/w3css/4/w3.css">
                        <link href='https://fonts.googleapis.com/css?family=Source Code Pro' rel='stylesheet'>
                        """

        icon_getter = IconGetter('https://www.w3schools.com/sql/sql_case.asp')
        r = icon_getter.parse_content(test_string_2)
        self.assertIsNotNone(r)
