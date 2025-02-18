from flask import Flask, render_template, request, redirect, url_for
import time

app = Flask(__name__)

# In-memory database (replace with a real database for long-term storage)
users = {}
subjects = []
rewards = 0

# Reward system
def get_reward(time_spent, time_limit):
    if time_spent <= time_limit:
        return 10  # Full reward
    else:
        return 5   # Partial reward

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    if username not in users:
        users[username] = {'chapters_completed': 0, 'rewards': 0}
    return redirect(url_for('dashboard', username=username))

@app.route('/dashboard/<username>', methods=['GET', 'POST'])
def dashboard(username):
    global rewards
    if request.method == 'POST':
        subject_name = request.form['subject_name']
        chapter_name = request.form['chapter_name']
        time_limit = int(request.form['time_limit'])
        start_time = time.time()

        subjects.append({'subject_name': subject_name, 'chapter_name': chapter_name, 'time_limit': time_limit})
        
        return render_template('study.html', username=username, chapter_name=chapter_name, time_limit=time_limit)

    return render_template('dashboard.html', username=username, subjects=subjects)

@app.route('/study/<username>/<chapter_name>/<int:time_limit>', methods=['POST'])
def study(username, chapter_name, time_limit):
    global rewards
    start_time = time.time()

    # Simulating studying (you will click the button once you complete the chapter)
    time_spent = time.time() - start_time
    reward = get_reward(time_spent, time_limit)
    rewards += reward

    users[username]['rewards'] += reward
    users[username]['chapters_completed'] += 1
    
    return render_template('study_complete.html', chapter_name=chapter_name, reward=reward)

@app.route('/achievements/<username>')
def achievements(username):
    user = users.get(username, None)
    if user:
        return render_template('achievements.html', username=username, user=user)
    return redirect(url_for('index'))

if __name__ == '__main__':
  
    app.run(debug=True)
