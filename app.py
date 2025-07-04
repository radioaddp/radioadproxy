from flask import Flask, Response, stream_with_context
import requests
import os

app = Flask(__name__)

SOURCE_URL = "https://stmv1.srvsite.com/radioaddp/radioaddp/playlist.m3u8"

@app.route('/stream.m3u8')
def proxy_stream():
    headers = {
        "User-Agent": "VLC/3.0.11 LibVLC/3.0.11"
    }
    try:
        r = requests.get(SOURCE_URL, headers=headers, stream=True, timeout=10)
        return Response(stream_with_context(r.iter_content(chunk_size=1024)), content_type=r.headers.get('Content-Type', 'application/vnd.apple.mpegurl'))
    except requests.exceptions.RequestException:
        return "Erro ao conectar ao stream original.", 500

@app.route('/lista.m3u')
def m3u_playlist():
    m3u_content = """#EXTM3U
#EXTINF:-1 tvg-id="radioaddp" tvg-name="Rádio AD Dom Pedrito" tvg-logo="https://via.placeholder.com/100x100.png?text=Radio" group-title="Rádios",Rádio AD Dom Pedrito
https://radioadproxy.onrender.com/stream.m3u8
"""
    return Response(m3u_content, content_type='audio/x-mpegurl')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
