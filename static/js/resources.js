let allResources = [];

async function loadResources() {
    try {
        const response = await fetch('/api/resources');
        allResources = await response.json();
        displayResources(allResources);
    } catch (error) {
        console.error('Error loading resources:', error);
        document.getElementById('resourcesList').innerHTML = '<div class="loading">Error loading resources</div>';
    }
}

function displayResources(resources) {
    const container = document.getElementById('resourcesList');

    if (resources.length === 0) {
        container.innerHTML = '<div class="loading">No resources found</div>';
        return;
    }

    container.innerHTML = resources.map(resource => `
        <div class="resource-card">
            <span class="resource-badge badge-${resource.difficulty}">${resource.difficulty}</span>
            <h3>${resource.title}</h3>
            <p>${resource.description}</p>
            <div style="margin-top: 1rem;">
                <strong>Category:</strong> ${resource.category}<br>
                <strong>Type:</strong> ${resource.type}
            </div>
            <button class="btn btn-primary" style="margin-top: 1rem; width: 100%;" onclick="startResource(${resource.id})">
                Start Learning
            </button>
        </div>
    `).join('');
}

function filterResources() {
    const category = document.getElementById('categoryFilter').value;
    const difficulty = document.getElementById('difficultyFilter').value;

    let filtered = allResources;

    if (category) {
        filtered = filtered.filter(r => r.category === category);
    }

    if (difficulty) {
        filtered = filtered.filter(r => r.difficulty === difficulty);
    }

    displayResources(filtered);
}

function startResource(resourceId) {
    alert(`Starting resource ${resourceId}. This will track your progress.`);
}

document.addEventListener('DOMContentLoaded', () => {
    loadResources();

    document.getElementById('categoryFilter').addEventListener('change', filterResources);
    document.getElementById('difficultyFilter').addEventListener('change', filterResources);
});
