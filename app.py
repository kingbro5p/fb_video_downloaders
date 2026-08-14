from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'error': 'অনুগ্রহ করে ফেসবুক ভিডিওর লিংক প্রবেশ করান'}), 400

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url')
            title = info.get('title', 'Facebook Video')
            thumbnail = info.get('thumbnail', '')
            duration = info.get('duration_string', '')

            return jsonify({
                'success': True,
                'title': title,
                'download_url': video_url,
                'thumbnail': thumbnail,
                'duration': duration
            })
    except Exception as e:
        return jsonify({
            'error': 'ভিডিও লিংকটি এক্সট্র্যাক্ট করা যায়নি। ভিডিওটি প্রাইভেট হতে পারে অথবা লিংকটি সঠিক নয়।'
        }), 400

if __name__ == '__main__':
    app.run(debug=True)