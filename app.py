from flask import Flask, render_template
import requests
import io
import base64
import matplotlib
matplotlib.use('Agg')  # non-GUI backend for saving plots in scripts/servers
import matplotlib.pyplot as plt


app = Flask(__name__)


# ThingSpeak channel info
THINGSPEAK_CHANNEL_ID = 3030027
THINGSPEAK_API_KEY = "GPF52ZQ1SQE08TVC"
THINGSPEAK_URL = f'https://api.thingspeak.com/channels/{THINGSPEAK_CHANNEL_ID}/feeds.json?api_key={THINGSPEAK_API_KEY}&results=1'


# --- Mock data for graph (average queue per hour, assuming operating hours are 9-6pm) ---
stall_history = [
    {"hour": "09-10", "avgQueue": 7},
    {"hour": "10-11", "avgQueue": 12},
    {"hour": "11-12", "avgQueue": 15},
    {"hour": "12-13", "avgQueue": 14},
    {"hour": "13-14", "avgQueue": 6},
    {"hour": "14-15", "avgQueue": 8},
    {"hour": "15-16", "avgQueue": 5}   # quietest hour
]


def get_best_hour(data):
    best = min(data, key=lambda d: d["avgQueue"])  # lowest average
    return best["hour"], best["avgQueue"]


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

    # Prepare graph
    hours = [d["hour"] for d in stall_history]
    averages = [d["avgQueue"] for d in stall_history]

    fig, ax = plt.subplots()
    bars = ax.bar(hours, averages)

    # highlight the quietest hour in green
    best_hour, best_avg = get_best_hour(stall_history)
    best_index = hours.index(best_hour)
    bars[best_index].set_color("green")

    ax.set_title("Last Week's Queue Data (Average Queue per Hour)")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Average Queue Length")

    # save as base64
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    graph_url = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close(fig)

    people, category, wait = get_queue_data()
    print(people, category, wait)   # for debugging
    status_class, phrase_text = map_category(category)
    people_text = f"≤ {people} people"
    print(status_class, phrase_text, people_text) # for debugging

    return render_template("index.html",
                           graph_url=graph_url,
                           best_hour=best_hour,
                           best_avg=best_avg,
                           people_text=people_text,
                           status_class=status_class,
                           phrase_text=phrase_text,
                           waiting_time=wait)

if __name__ == '__main__':
    app.run(debug=True, port=5000)