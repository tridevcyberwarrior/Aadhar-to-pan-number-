from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/pan-info', methods=['GET'])
def get_pan_info():
    aadhar_no = request.args.get('aadhar_no')
    
    if not aadhar_no:
        return jsonify({"error": "aadhar_no parameter required"}), 400
    
    # Validate Aadhaar format (12 digits)
    if not aadhar_no.isdigit() or len(aadhar_no) != 12:
        return jsonify({"error": "Invalid Aadhaar number. Must be 12 digits."}), 400
    
    url = f"https://apnapanindia.co.in/pan-aadhar-search/ajax-check-pan-status.php?aadhar_no={aadhar_no}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Mobile Safari/537.36',
        'Accept': '*/*',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://apnapanindia.co.in/pan-aadhar-search/pan-find-application-type1.php',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9,hi;q=0.8',
        'sec-ch-ua': '"Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Connection': 'keep-alive',
        'Host': 'apnapanindia.co.in'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            try:
                data = response.json()
                return jsonify(data)
            except:
                return jsonify({
                    "status": "error",
                    "message": "Invalid JSON response",
                    "raw_response": response.text
                }), 500
        else:
            return jsonify({
                "status": "error",
                "message": f"HTTP {response.status_code}",
                "response": response.text
            }), response.status_code
            
    except requests.exceptions.Timeout:
        return jsonify({"status": "error", "message": "Request timeout"}), 504
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "PAN Info API",
        "usage": "/pan-info?aadhar_no=725635600653",
        "note": "Enter 12-digit Aadhaar number"
    })

if __name__ == '__main__':
    app.run(debug=True)
