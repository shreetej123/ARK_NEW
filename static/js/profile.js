async function loadProfile() {
    const user = await checkAuth();

    if (!user) {
        window.location.href = '/';
        return;
    }

    try {
        const response = await fetch('/api/progress');
        const data = await response.json();

        document.getElementById('completedLessons').textContent = data.completed_lessons;
        document.getElementById('currentStreak').textContent = data.current_streak;
        document.getElementById('totalPoints').textContent = data.points;
        document.getElementById('userLevel').textContent = data.level;

        const percentage = Math.round((data.completed_lessons / data.total_lessons) * 100);
        document.getElementById('progressBar').style.width = percentage + '%';
        document.getElementById('progressPercentage').textContent = percentage;

        displayAchievements(data.achievements);
        displayActivity(data.recent_activities);
    } catch (error) {
        console.error('Error loading profile:', error);
    }
}

function displayAchievements(achievements) {
    const container = document.getElementById('achievementsList');

    if (achievements.length === 0) {
        container.innerHTML = '<div class="loading">No achievements yet. Keep learning!</div>';
        return;
    }

    container.innerHTML = achievements.map(achievement => `
        <div class="achievement-badge">
            <span>🏆</span>
            <strong>${achievement}</strong>
        </div>
    `).join('');
}

function displayActivity(activities) {
    const container = document.getElementById('activityList');

    if (activities.length === 0) {
        container.innerHTML = '<div class="loading">No recent activity</div>';
        return;
    }

    container.innerHTML = activities.map(activity => `
        <div class="activity-item">
            <div>
                <strong>${activity.title}</strong>
                <br>
                <small>${activity.type}</small>
            </div>
            <div>
                ${activity.date}
            </div>
        </div>
    `).join('');
}

document.addEventListener('DOMContentLoaded', () => {
    loadProfile();
});
