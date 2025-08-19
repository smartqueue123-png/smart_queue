# from flask import Flask, render_template_string
# import requests

# app = Flask(__name__)

# # ThingSpeak channel info
# THINGSPEAK_CHANNEL_ID = 3030027
# THINGSPEAK_API_KEY = GPF52ZQ1SQE08TVC
# THINGSPEAK_URL = f'https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID}/fields/1.json?api_key={THINGSPEAK_API_KEY}&results=1'

# # HTML template
# HTML_TEMPLATE = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
# <meta charset="UTF-8">
# <meta name="viewport" content="width=device-width, initial-scale=1.0">
# <title>Queue Monitor</title>
# {{ css|safe }}
# </head>
# <body>
# <div class="card">
#     <div class="stall-name">Nasi Lemak Delight</div>
#     <div class="queue-info">
#         <div class="people">{{ people_text }}</div>
#         <div class="status-bar {{ status_class }}"></div>
#         <div class="phrase">{{ phrase_text }}</div>
#         <div class="phrase">(est. waiting time: <span style="font-size: 28px; font-weight: bold;">{{ waiting_time }}</span>min)</div>
#     </div>
# </div>
# </body>
# </html>
# """

# # CSS from your snippet
# CSS = """
# <style>
# body { margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #fff5f5; color: #3d0000; }
# .card { background: white; margin: 10px 0; padding: 20px; border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; }
# .card .stall-name { font-size: 20px; font-weight: bold; color: #b30000; flex: 1 1 100%; }
# .queue-info { text-align: right; flex: 1 1 100%; margin-top: 10px; display: flex; flex-direction: column; align-items: flex-end; }
# .queue-info .people { font-size: 16px; }
# .status-bar { width: 100%; max-width: 100px; height: 10px; border-radius: 5px; margin: 5px 0; }
# .queue-info .phrase { font-weight: bold; }
# .short { background-color: #4CAF50; }
# .medium { background-color: #FFEB3B; }
# .long { background-color: #F44336; }
# </style>
# """

# def get_queue_data():
#     """Fetch latest ThingSpeak data"""
#     try:
#         r = requests.get(THINGSPEAK_URL)
#         r.raise_for_status()
#         feeds = r.json().get('feeds', [])
#         if not feeds:
#             return 0, 0, 0
#         latest = feeds[-1]
#         # ThingSpeak fields: field1=estimated_people, field2=category, field3=waiting_time
#         estimated_people = int(latest.get('field1', 0))
#         category = int(latest.get('field2', 0))
#         waiting_time = int(latest.get('field3', 0))
#         return estimated_people, category, waiting_time
#     except Exception as e:
#         print("Error fetching ThingSpeak:", e)
#         return 0, 0, 0

# def map_category(category):
#     """Map numeric category to class and phrase"""
#     if category in [0,1]:
#         return 'short', 'No wait'
#     elif category == 2:
#         return 'medium', 'Wait a little'
#     elif category == 3:
#         return 'long', 'Long wait'
#     else:
#         return '', ''

# @app.route('/')
# def index():
#     people, category, wait = get_queue_data()
#     status_class, phrase_text = map_category(category)
#     people_text = f"≤ {people} people"
#     return render_template_string(HTML_TEMPLATE, people_text=people_text, status_class=status_class, phrase_text=phrase_text, waiting_time=wait, css=CSS)

# if __name__ == '__main__':
#     app.run(debug=True, port=3000)



from flask import Flask, render_template
import requests

app = Flask(__name__)

# ThingSpeak channel info
THINGSPEAK_CHANNEL_ID = 3030027
THINGSPEAK_API_KEY = "GPF52ZQ1SQE08TVC"
THINGSPEAK_URL = f'https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID}/feeds.json?api_key={THINGSPEAK_API_KEY}&results=1'

def get_queue_data():
    """Fetch latest ThingSpeak data"""
    try:
        r = requests.get(THINGSPEAK_URL)
        r.raise_for_status()
        feeds = r.json().get('feeds', [])
        if not feeds:
            return 0, 0, 0
        latest = feeds[-1]
        estimated_people = int(latest.get('field1', 0))
        waiting_time = int(latest.get('field2', 0))
        category = int(latest.get('field3', 0))
        return estimated_people, category, waiting_time
    except Exception as e:
        print("Error fetching ThingSpeak:", e)
        return 0, 0, 0

def map_category(category):
    """Map numeric category to class and phrase"""
    if category in [0,1]:
        return 'short', 'Good to go!'
    elif category == 2:
        return 'medium', 'Wait a little'
    elif category == 3:
        return 'long', 'Long wait'
    else:
        return '', ''

@app.route('/')
def index():
    people, category, wait = get_queue_data()
    print(people, category, wait)   # <-- check the console
    status_class, phrase_text = map_category(category)
    people_text = f"≤ {people} people"
    print(status_class, phrase_text, people_text)
    return render_template('index.html',
                           people_text=people_text,
                           status_class=status_class,
                           phrase_text=phrase_text,
                           waiting_time=wait)

if __name__ == '__main__':
    app.run(debug=True, port=5000)



# Hello World