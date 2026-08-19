import concurrent.futures
import re
import urllib.request
import urllib.error

# Dados brutos das rádios
RAW_DATA = """
Alternative | Acdic Infektion | Foreign Mix | http://radio.acidicinfektion.ind.in:8047/stream
Alternative | DnB FM | Drum and Bass | http://go.dnbfm.ru:8000/play
Alternative | Vallenato | Salsa | http://radiolatina.info:7087/
Alternative | Radio Paradise | Random | http://stream-tx1.radioparadise.com/mp3-128
Alternative | Chillout Lounge | Mix | http://sc1c-sjc.1.fm:8010
Alternative | Fidella Mix | Random | http://streaming.radionomy.com/fidellamix
Alternative | Estereo Sula 100.1 FM | Classic | http://96.31.90.115:8230
Alternative | Radio Monza | Foreign Indie| http://uplink.intronic.nl:80/radiomonza
Alternative | Eldo Radio | Independent Indie| http://sender.eldoradio.de:8000/128
Alternative | SikhNet Radio | Foreign Indie| http://radio2.sikhnet.com:8023/autodj
Ambient | Masschinengeist | Deep Space | http://178.209.52.163:7331/maschinengeist.org.128.aacp
Ambient | Radiolla | Easy Listening | http://air.radiolla.com:80/radiolla.128k.mp3
Ambient | Piano Perfect | Instrumental | http://206.217.213.235:8050
Ambient | New Age Nuance | Instrumental | http://206.217.213.235:8040
Ambient | Guitar Genius | Instrumental | http://173.244.215.162:8020
Ambient | Vorarlberg | Lounge | http://webradio.antennevorarlberg.at:80/lounge
Ambient | Black Label FM | Lounge | http://listen.radionomy.com/blacklabelfm
Ambient | Jamendo Gabber Lounge | Classic | http://streaming.radionomy.com/Gabberfm
AMV | Radio AMV | Alternate Metaverse | http://radioamv.com
AMV | Unity Airport Radio | Alternate Metaverse | http://142.44.159.230:5196
AMV | Club Cherry | DJ Zed | http://37.59.28.208:8321
Blues | Blues Radio | Hits | http://sc2b-sjc.1.fm:8030
Blues | Blues Got|The Ass Kicking Blues Rocker | http://206.217.213.236:8500
Blues | KHNY Honey 103 | Soul R&B| http://honey.macchiatomedia.org:8080
Blues | Black Beats FM | ForeignR&B | http://stream.blackbeats.fm
Country | Radio Folk | Country Side Folk | http://mp3stream3.abradio.cz:8000/folk128.mp3
Country | Cool Radio | Foreign Rock & Pop & Folk | http://176.9.30.66:80
Country | Future Festival Radio | Folk Festival | http://uk1-pn.webcast-server.net:8000/Green-Futures-Festival-Radio
Country | The Renegade | Honky Tonk | http://37.59.37.139:7570
Country | FM Country | Classics | http://sc3c-sjc.1.fm:7806
Country | Country HIts 24 | Mix Hits | http://countrymusic24.powerstream.de:9000
Country | Rockabilly | Classic | http://209.9.238.6:6042
Electro | Ellhnikos 90.3 FM | Greek | http://live.ellinikos.gr:8010/903.mp3
Electro | Radio Koprivnica | European | http://194.152.206.205:9000/rkc192
Electro | Arges Mioveni NR1 | Romainian | http://89.39.189.53:8000
Electro | Radiolla Volta | Hype | http://air.radiolla.com:80/volta.192k.mp3
Electro | House Club Set | Hits | http://sr2.webradionetwork.eu:9000/wrn_96k.mp3
Electro | Mix 247 EDM | EDM | http://listen.radionomy.com/mix247edm
Electro | NSB Radio | Dance | http://live.nsbradio.co.uk:8904
Electro| Enation FM | House | http://useless.streams.enation.fm:8000
Electro | Noise FM | Electronic Trance | http://noisefm.ru:8000/live
Electro | Hard House UK | Hits | http://streams.netmindz.net:80/hhuk.mp3
Electro | Hardcore Radio | Hardcore | http://81.18.165.236:80
Electro | EBM Radio | Techno | http://87.106.138.241:7000
Funk | Second Radio | Random | http://secondstream.de:10001
Funk | Groove Salad | Modern | http://ice.somafm.com/groovesalad
Funk | Secret Agent | Mix | http://ice.somafm.com/secretagent
Funk | Hot 108 | Hits | http://108.61.30.179:4030
Funk | 1 Power | Hits | http://108.61.30.179:5000
Funk | Power Hits | Hits | http://108.61.30.179:7000
Funk | Vibes | Foreign | http://mp3stream3.abradio.cz:8000/hiphopvibes.mp3
Funk | Jungle Radio | Old School | http://stream.100000000000000.com:8000/HIP-HOP
Funk | Got Radio | Hits | http://206.217.213.235:8260
Funk | Radio Italia | Foreign | http://stream15.top-ix.org:80/radioitaliauno
Funk | What?! Radio | Yesterday's Hits | http://whatradio.macchiatomedia.org:9119/
Funk | Jamz | Mix | http://sc1c-sjc.1.fm:8052
Jazz | Radiolla Jiraffe | Instrumental | http://air.radiolla.com:80/jiraffe.192k.mp3
Jazz | WKAR | Instrumental | http://mozart.wkar.msu.edu:80/wkar-jazz
Jazz | Jazz-Ahh | Instrumental | http://stream.100000000000000.com:8000/JAZZ
Jazz | Smooth Radio | Mix | http://sj128.hnux.com
Jazz | Global Radio | Mix | http://sj64.hnux.com
Jazz | KKJZ 88.1 | Soul | http://1.ice1.firststreaming.com/kkjz_fm.mp3
Jazz | The Breeze 181 FM | Soul | http://181fm-edge1.cdnstream.com/181-breeze_128k.mp3
Jazz | Radio Dismuke | Classics | http://74.208.197.50:8087/
Jazz | Latiz Jazz | Foreign | http://listen.radionomy.com:80/boleros-para-enamorarse
Misc | Spectrum Radio | LIVE | http://indiespectrum.com:9000
Misc | German American Radio | German - LIVE | http://99.198.118.250:8016
Misc | Harcore Liquid Doom | Hardcore Speedcore| http://liquiddoom.net:8000/hardcore
Misc | Otaku No Radio | Anime J-Pop| http://radio.otakunopodcast.com:8000/otakunoradio
Misc | Japan-A-Radio | Hits J-Pop| http://audio.misproductions.com:80/japan128k
Misc | Bear Radio | Classic LGBTQ| http://streaming316.radionomy.com/bear-radio-oso
Misc | LGBT Nation | Pop LGBTQ | http://206.190.135.28:8051/autodj
Misc | On Gay Radio | Dance LGBTQ| http://s5.radionetz.de/0n-gay_app.mp3
Misc | XL Trax | Dance LGBTQ | http://xltrax.com:8000
Misc | Liquid Doom | Hardcore Speedcore| http://liquiddoom.net:8000/doom
Misc | DOS Radio | Game Speedcore | http://liquiddoom.net:8000/dos
Misc | Re:Noize | Power Noise Speedcore| http://stream.clubrenoize.com:9001
Misc2 | Got Mix Radio | Pop Hits | http://173.244.215.162:8250
Misc2 | Hot Pop Radio | Pop Hits | http://173.244.215.162:8260
Misc2 | Freestyle Dance Radio | International Pop | http://listen.radionomy.com/freestylefm
Misc2 | Ki$$ | Pop Hits | http://151.80.108.126:9530
Misc2 | Pondends Radio | Vibes Reggae | http://198.178.123.20:7000
Misc2 | Radio Campus | Electro Reggae| http://live.radio-campus.org:8000/lorraine
Misc2 | What?! Island | Everyday Reggae | http://whatisland.macchiatomedia.org:8118
Misc2 | 808 Reggaecast | Live Reggae | http://808.rastamusic.com/rastamusic.mp3
Misc2 | Jammin | Reggae Hits | http://64.202.98.51:808
Misc2 | WKSU | Classical | http://66.225.205.8:8030
Misc2 | Classical Minnesota | Classical | http://cms.stream.publicradio.org/cms.mp3
Misc2 | WQXR Q2 | Classical | http://q2stream.wqxr.org/q2
Rock | Super70s | Super70s | http://listen.181fm.com:8066
Rock | Top 40 | Top 40| http://uplink.duplexfx.com:8028/ Rock Top 40
Rock | WCBN | Freeform Metal | http://floyd.wcbn.org:8000/wcbn-hd.mp3
Rock | Radio FSN | Hardcore Metal | http://stream.radio-fsn.de:8000/hardcore
Rock | 100hitz | Heavy Metal | http://69.4.234.186:9100
Rock | Metal Detector | Brass Metal | http://ice.somafm.com/metal
Rock | Vibration PR | Pop-Rock | http://91.121.38.100:8030
Rock | Megarock Radio | Yesterday's | http://stream1.megarockradio.net:8240
Rock | Hard Rockin 80's | 80's | http://stream-licensing.com:8128
Rock | T1 Radio | Classic | http://t1radio.serverroom.us:8242
Rock | Rock Radio | Classic | http://uplink2.181.fm:8064
Rock | Radio Paradise | Soft Rock | http://stream-uk1.radioparadise.com:80/mp3-128
Romance | A.I.R Radio | Slow | http://listen.radionomy.com/airradiofreestyleslow
Romance | What?! Foreplay | Sexual | http://whatforeplay.macchiatomedia.org:8269
Romance | Heartbeatz | Romantic Songs | http://heartbeatz.fm:8008
Romance | Hit's 70 | Easy Listening | http://listen.radionomy.com:80/1HITS70s
Romance | Got Native Radio | Mix | http://173.244.215.162:8030
Romance | Beatles Radio | Classic | http://64.40.99.2:8088
Romance | Aural Moon | Progressive | http://64.202.98.133:2010
Romance | Ohana Angel Majestic | Everyday | http://ohana.digistream.info:10288
Romance | Star FM | Mix | http://91.250.82.237:8004
"""

def extract_url(line):
    match = re.search(r'(https?://[^\s]+)', line)
    return match.group(1) if match else None

def test_url(line):
    url = extract_url(line)
    if not url:
        return None, False

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        # Timeout de 5s para não travar em streams mortos
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status in [200, 301, 302, 307, 308]:
                return line, True
    except Exception:
        pass
    
    return line, False

def main():
    lines = [l.strip() for l in RAW_DATA.strip().split('\n') if l.strip()]
    total = len(lines)
    print(f"Iniciando teste em {total} rádios...")

    online_lines = []

    # Executa até 20 requisições simultâneas
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(test_url, line): line for line in lines}
        
        for future in concurrent.futures.as_completed(futures):
            original_line, is_working = future.result()
            if is_working:
                print(f"[ONLINE] -> {original_line}")
                online_lines.append(original_line)
            else:
                print(f"[OFFLINE] -> {original_line}")

    # Salva os resultados online em um arquivo
    output_filename = "online_stations.txt"
    with open(output_filename, "w", encoding="utf-8") as f:
        for line in online_lines:
            f.write(line + "\n")

    print("\n" + "="*50)
    print(f"Verificação concluída!")
    print(f"Total: {total} | Online: {len(online_lines)} | Offline: {total - len(online_lines)}")
    print(f"Lista de rádios funcionais salva em: {output_filename}")
    print("="*50)

if __name__ == "__main__":
    main()
