"""template.html + data.json -> ../index.html"""
import os
H = os.path.dirname(os.path.abspath(__file__))
t = open(os.path.join(H, 'template.html'), encoding='utf-8').read()
d = open(os.path.join(H, 'data.json'), encoding='utf-8').read()
head = '''<!doctype html>
<html lang="ko"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#eef0ec" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#101413" media="(prefers-color-scheme: dark)">
<meta name="description" content="몬스터 헌터 와일즈 몬스터·무기·방어구·스킬·장식주·호석·아이템 한국어 도감">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="와일즈 도감">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="icon-192.png">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}img{max-width:100%}</style>
'''
body = t.replace('__DATA__', d)
title_end = body.index('</title>') + len('</title>')
out = head + body[:title_end] + '\n' + body[title_end:].replace('<header', '</head><body>\n<header', 1) + '\n</body></html>\n'
open(os.path.join(H, '..', 'index.html'), 'w', encoding='utf-8').write(out)
print('index.html', len(out.encode()))
