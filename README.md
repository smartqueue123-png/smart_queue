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

QN: What happpens if the queue length is more than 15, what willl your app shows

ANS: the barrier can hold up to 15 people only


\n



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






