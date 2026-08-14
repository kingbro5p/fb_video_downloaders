from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

def extract_facebook_video(url):
    """ফেসবুক লিঙ্ক থেকে ভিডিওর ডাউনলোডের তথ্য বের করার কমন ফাংশন"""
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                'success': True,
                'title': info.get('title', 'Facebook Video'),
                'download_url': info.get('url'),
                'thumbnail': info.get('thumbnail', ''),
                'duration': info.get('duration_string', '')
            }, 200
    except Exception as e:
        return {
            'success': False,
            'error': 'ভিডিও লিংকটি এক্সট্র্যাক্ট করা যায়নি। ভিডিওটি প্রাইভেট হতে পারে অথবা লিংকটি সঠিক নয়।'
        }, 400


# ১. প্রধান ওয়েবসাইট রুট (Web Interface)
@app.route('/')
def home():
    return render_template('index.html')


# ২. স্ট্যান্ডার্ড API Endpoint (POST Method অথবা GET ?url=)
@app.route('/download', methods=['GET', 'POST'])
def download():
    url = None
    if request.method == 'POST':
        # JSON Body থেকে লিঙ্ক নেওয়া
        data = request.get_json(silent=True) or {}
        url = data.get('url') or request.form.get('url')
    else:
        # GET Parameter (Query String) থেকে লিঙ্ক নেওয়া (?url=...)
        url = request.args.get('url')

    if not url:
        return jsonify({'success': False, 'error': 'অনুগ্রহ করে ফেসবুক ভিডিওর লিংক প্রদান করুন'}), 400

    result, status_code = extract_facebook_video(url)
    return jsonify(result), status_code


# ৩. ডাইরেক্ট স্লেশ API Endpoint (/api/YOUR_FACEBOOK_URL)
@app.route('/api/<path:fb_url>', methods=['GET'])
def download_path(fb_url):
    if not fb_url:
        return jsonify({'success': False, 'error': 'ইউআরএল পাওয়া যায়নি'}), 400
    
    result, status_code = extract_facebook_video(fb_url)
    return jsonify(result), status_code


if __name__ == '__main__':
    app.run(debug=True)
    
