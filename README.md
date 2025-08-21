Pain points: 

- Finds the current crowd % vague (doesn’t show stall-specific data)

- Gets annoyed when she has to manually check multiple stalls

- Often arrives at food courts just after they get crowded

- Wishes the app could notify her when her favourite stall is less busy



How our project works:

- NOTE: This project is only done for 1 stall ONLY 

- Assuming each store has barriers and each of those barriers have 3 sensors installed (IR, Ultrasonic and LDR sensors). 

- The sensor works by detecting if there is someone standing at there (Sensor A [ultrasonic], B [IR] and C [LDR]) sensor A is nearest to the stall while sensor C is furthest from the stall. To confirm the presence is in the queue and not just someone passing by the sensors will detect presence and wait 5 seconds, if presence is still detected, sensors will confirm the presence is part of the queue

- To determine the length of the queue, if sensor A detect a person the app will show ≤ 5 people (Good to go!), else if both sensor A and B detected it will show ≤ 10 people (Wait a little), else if all sensors (sensor A, B and C) are detected it will show ≤ 15 people (Queue too long), else ≤ 0 people (Good to go!)




Possible Q&A segment:
==============================

QN: How can our code work to support more than 1 stall, or all stalls 
ANS: refer to the commented codes in app.py, vnc.py and index.html with the comment (for multiple stalls)


QN: What happpens if the queue length is more than 15, what will your app shows
ANS: the barrier can hold up to 15 people only


QN: What’s your plan if someone blocks a sensor on purpose?
ANS: 
- Senario 1: If the queue length is up to sensor A only and someone block sensor B for less than 5 seconds, our code will be able to detect that is a fault and therefore it will appear as ≤ 5 people (Good to go!)
- Senario 2: If there is no queue and someone block sensor B for less than 5 seconds, our code will be able to detect that is a fault and therefore it will appear as ≤ 0 people (Good to go!)
- Senario 3: If there is no queue and someone block sensor C for less than 5 seconds, our code will be able to detect that is a fault and therefore it will appear as ≤ 0 people (Good to go!)
- Senario 4: If there is no queue and someone block both sensor B and C for less than 5 seconds, our code will be able to detect that is a fault and therefore it will appear as ≤ 0 people (Good to go!)
- Senario 5: Else these applies to all other unexpected senarios

To determine the length of the queue, if sensor A detect a person the app will show ≤ 5 people (Good to go!), else if both sensor A and B detected it will show ≤ 10 people (Wait a little), else if all sensors (sensor A, B and C) are detected it will show ≤ 15 people (Queue too long), else ≤ 0 people (Good to go!)


QN: How did you pick the thresholds for “≤5 / ≤10 / ≤15 people” from sensor states?
ANS: We used the training kit and take not of the reading with and without hand, our thresholds derive from 2 factors:
- Factor 1: we used the readings with hands
- Factor 2: we used the readings without hands 
Then we determine the middle point of the 2 readings and set it as our threshold


QN: Why ThingSpeak instead of storing directly in your own DB?
ANS: 
- Quick setup – no need to design and maintain your own database or backend.
- Built-in visualization – automatic graphs and dashboards without extra coding.
- Cloud-hosted – data accessible anywhere, anytime.
- IoT-friendly features – supports real-time data streaming and analytics.
- Lower maintenance – avoids server, storage, and security management.


QN: Your app currently uses a page reload—why not fetch JSON and update in place?
ANS: 
- Simplicity – A full page reload is easier to implement in Python (e.g., Flask/Django) without needing additional JavaScript for dynamic updates.
- Lower development overhead – No need to write separate APIs and AJAX/Fetch logic, reducing complexity.
- Consistency – Ensures the entire page (UI + data) is refreshed, avoiding partial update bugs.
- Reliability – A reload guarantees all resources (data, styles, scripts) are reloaded in sync, reducing chance of stale data (outdated/obsolete data).
- Good for prototypes / small-scale apps – Faster to build and easier to debug compared to setting up full JSON-based asynchronous updates.


QN: What’s your fallback output if one stall errors but others succeed?
ANS: 
We added this error message to inform user: "Sorry recommended time is temporarily unavailable for this store" that the graph is temporarily unavailable 


QN: How will you save each stall’s sensor settings – in a file, in environment variables, or in a database?
ANS: 
- Start simple with a file – Save each stall’s settings (like light threshold or distance limit) in a JSON/CSV file. Easy to test and change while developing.
- Move to a database later – As the project grows, use a database to store and update calibration for many stalls more easily.





How to run this project:

1. To run the website: python app.py

2. To play with data and thingspeak: python vnc.py 

3. Use triple dots to commit and push + pull

4. To access Thingspeak channel: https://thingspeak.mathworks.com/channels/3030027 

5. To fix (this fix is for pull): git remote add origin git@github.com:smartqueue123-png/smart_queue.git

    git remote -v           # confirm the URL

    ssh -T git@github.com   # should greet you as smartqueue123-png

    https://chatgpt.com/share/68a33c78-bc08-8011-9cfa-a0a00daa791b 

6. Generate a new SSH key: ssh-keygen -t ed25519 -C "smartqueue123@gmail.com"

7. Show your public key: type $env:USERPROFILE\.ssh\id_ed25519.pub