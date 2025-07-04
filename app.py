from flask import Flask, Response, stream_with_context
import requests

app = Flask(__name__)

SOURCE_URL = "https://stmv1.srvsite.com/radioaddp/radioaddp/playlist.m3u8"

@app.route('/stream.m3u8')
def proxy_stream():
    headers = {
        "User-Agent": "VLC/3.0.11 LibVLC/3.0.11"
    }
    r = requests.get(SOURCE_URL, headers=headers, stream=True)
    return Response(stream_with_context(r.iter_content(chunk_size=1024)), content_type=r.headers['Content-Type'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
