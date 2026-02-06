async function explainConcept() {
    const concept = document.getElementById('conceptInput').value;
    const resultContainer = document.getElementById('conceptResult');

    if (!concept) {
        alert('Please enter a concept');
        return;
    }

    resultContainer.innerHTML = '<div class="loading">Generating explanation...</div>';
    resultContainer.classList.add('active');

    try {
        const response = await fetch('/api/concepts/explain', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ concept: concept }),
        });

        const data = await response.json();

        resultContainer.innerHTML = `
            <h3>${data.title}</h3>
            <p style="margin: 1rem 0;">${data.explanation}</p>
            <h4>Key Points:</h4>
            <ul style="margin-left: 2rem;">
                ${data.key_points.map(point => `<li>${point}</li>`).join('')}
            </ul>
            <h4 style="margin-top: 1rem;">Example:</h4>
            <p style="background: #f0f0f0; padding: 1rem; border-radius: 5px;">${data.example}</p>
        `;
    } catch (error) {
        console.error('Error:', error);
        resultContainer.innerHTML = '<div class="loading">Error generating explanation</div>';
    }
}

async function generateCode() {
    const task = document.getElementById('codeTask').value;
    const language = document.getElementById('codeLanguage').value;
    const resultContainer = document.getElementById('codeResult');

    if (!task) {
        alert('Please enter a task');
        return;
    }

    resultContainer.innerHTML = '<div class="loading">Generating code...</div>';
    resultContainer.classList.add('active');

    try {
        const response = await fetch('/api/code/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ task: task, language: language }),
        });

        const data = await response.json();

        resultContainer.innerHTML = `
            <h3>${data.task} - ${data.language}</h3>
            <pre><code>${escapeHtml(data.code)}</code></pre>
            <button class="btn btn-secondary" onclick="copyCode()" style="margin-top: 1rem;">Copy Code</button>
        `;
    } catch (error) {
        console.error('Error:', error);
        resultContainer.innerHTML = '<div class="loading">Error generating code</div>';
    }
}

async function showVisualization(type) {
    const resultContainer = document.getElementById('visualizationResult');

    resultContainer.innerHTML = '<div class="loading">Loading visualization...</div>';
    resultContainer.classList.add('active');

    try {
        const response = await fetch(`/api/visualizations/${type}`);
        const data = await response.json();

        resultContainer.innerHTML = `
            <h3>${data.title}</h3>
            <p>${data.description}</p>
            <div style="background: white; padding: 2rem; border-radius: 8px; margin-top: 1rem;">
                ${data.svg}
            </div>
        `;
    } catch (error) {
        console.error('Error:', error);
        resultContainer.innerHTML = '<div class="loading">Error loading visualization</div>';
    }
}

async function generateAudio() {
    const text = document.getElementById('audioText').value;
    const resultContainer = document.getElementById('audioResult');

    if (!text) {
        alert('Please enter text');
        return;
    }

    resultContainer.innerHTML = '<div class="loading">Generating audio...</div>';
    resultContainer.classList.add('active');

    try {
        const response = await fetch('/api/audio/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text }),
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);

            resultContainer.innerHTML = `
                <h4>Audio Generated Successfully!</h4>
                <audio controls style="width: 100%; margin-top: 1rem;">
                    <source src="${url}" type="audio/mp3">
                    Your browser does not support the audio element.
                </audio>
                <a href="${url}" download="lesson.mp3" class="btn btn-primary" style="margin-top: 1rem; display: inline-block;">
                    Download Audio
                </a>
            `;
        } else {
            resultContainer.innerHTML = '<div class="loading">Error generating audio</div>';
        }
    } catch (error) {
        console.error('Error:', error);
        resultContainer.innerHTML = '<div class="loading">Error generating audio</div>';
    }
}

function copyCode() {
    const code = document.querySelector('#codeResult pre code').textContent;
    navigator.clipboard.writeText(code).then(() => {
        alert('Code copied to clipboard!');
    });
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
