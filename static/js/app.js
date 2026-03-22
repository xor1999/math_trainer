const API = {
    async getTechniques() {
        const res = await fetch('/api/techniques');
        return res.json();
    },
    async getProblem(technique) {
        const res = await fetch('/api/problem', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ technique }),
        });
        return res.json();
    },
    async getHint(technique, problem) {
        const res = await fetch('/api/hint', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ technique, problem }),
        });
        return res.json();
    },
    async submit(data) {
        const res = await fetch('/api/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        return res.json();
    },
    async getStats() {
        const res = await fetch('/api/stats');
        return res.json();
    },
};

// State
let state = {
    techniques: {},
    currentTechnique: null,
    currentCategory: null,
    currentProblem: null,
    currentAnswer: null,
    mode: 'practice', // practice | test
    problemNum: 0,
    totalProblems: 10,
    sessionResults: [],
    timerStart: null,
    timerInterval: null,
    // Test mode: multiple techniques
    testTechniques: [],
};

// DOM
const views = {
    select: document.getElementById('select-view'),
    practice: document.getElementById('practice-view'),
    summary: document.getElementById('summary-view'),
    stats: document.getElementById('stats-view'),
};

const navBtns = {
    practice: document.getElementById('nav-practice'),
    test: document.getElementById('nav-test'),
    stats: document.getElementById('nav-stats'),
};

function showView(name) {
    Object.values(views).forEach(v => v.classList.remove('active'));
    views[name].classList.add('active');
}

function setActiveNav(name) {
    Object.values(navBtns).forEach(b => b.classList.remove('active'));
    if (navBtns[name]) navBtns[name].classList.add('active');
}

// Technique selector
async function loadTechniques() {
    state.techniques = await API.getTechniques();
    renderTechniqueList();
}

function renderTechniqueList() {
    const container = document.getElementById('technique-list');
    container.innerHTML = '';

    for (const [category, techniques] of Object.entries(state.techniques).sort()) {
        const group = document.createElement('div');
        group.className = 'category-group';
        group.innerHTML = `<h3>${category}</h3>`;

        for (const tech of techniques) {
            const card = document.createElement('div');
            card.className = 'technique-card';
            card.innerHTML = `
                <div>
                    <div class="name">${tech.name}</div>
                    <div class="desc">${tech.description}</div>
                </div>
                <div class="arrow">→</div>
            `;
            card.addEventListener('click', () => {
                if (state.mode === 'practice') {
                    startPractice(tech.name, category);
                } else {
                    startTest([tech.name], category);
                }
            });
            group.appendChild(card);
        }

        // "All" button for test mode
        if (state.mode === 'test') {
            const allCard = document.createElement('div');
            allCard.className = 'technique-card';
            allCard.innerHTML = `
                <div>
                    <div class="name">All ${category}</div>
                    <div class="desc">Mix all ${category} techniques</div>
                </div>
                <div class="arrow">→</div>
            `;
            allCard.addEventListener('click', () => {
                const names = techniques.map(t => t.name);
                startTest(names, category);
            });
            group.appendChild(allCard);
        }

        container.appendChild(group);
    }

    // "All techniques" for test mode
    if (state.mode === 'test') {
        const allGroup = document.createElement('div');
        allGroup.className = 'category-group';
        allGroup.innerHTML = `<h3>Everything</h3>`;
        const allCard = document.createElement('div');
        allCard.className = 'technique-card';
        allCard.innerHTML = `
            <div>
                <div class="name">All techniques</div>
                <div class="desc">Random mix of everything</div>
            </div>
            <div class="arrow">→</div>
        `;
        allCard.addEventListener('click', () => {
            const allNames = Object.values(state.techniques).flat().map(t => t.name);
            startTest(allNames, 'mixed');
        });
        allGroup.appendChild(allCard);
        container.appendChild(allGroup);
    }
}

// Practice
async function startPractice(name, category) {
    state.currentTechnique = name;
    state.currentCategory = category;
    state.mode = 'practice';
    state.problemNum = 0;
    state.totalProblems = parseInt(document.getElementById('num-problems').value) || 10;
    state.sessionResults = [];

    document.getElementById('practice-title').textContent = name;
    document.getElementById('practice-mode-badge').textContent = 'Practice';
    document.getElementById('hint-area').style.display = 'block';

    showView('practice');
    nextProblem();
}

// Test
async function startTest(names, category) {
    state.testTechniques = names;
    state.currentCategory = category;
    state.mode = 'test';
    state.problemNum = 0;
    state.totalProblems = parseInt(document.getElementById('num-problems').value) || 10;
    state.sessionResults = [];

    document.getElementById('practice-title').textContent =
        names.length === 1 ? names[0] : `Test: ${category}`;
    document.getElementById('practice-mode-badge').textContent = 'Test — Timed';
    document.getElementById('hint-area').style.display = 'none';

    showView('practice');
    nextProblem();
}

async function nextProblem() {
    if (state.problemNum >= state.totalProblems) {
        showSummary();
        return;
    }

    state.problemNum++;

    // Pick technique
    let techName;
    if (state.mode === 'test' && state.testTechniques.length > 0) {
        techName = state.testTechniques[Math.floor(Math.random() * state.testTechniques.length)];
        state.currentTechnique = techName;
    } else {
        techName = state.currentTechnique;
    }

    const data = await API.getProblem(techName);
    state.currentProblem = data.problem;
    state.currentAnswer = data.answer;

    // Update UI
    document.getElementById('problem-text').textContent = data.problem + ' = ?';
    document.getElementById('progress-fill').style.width =
        `${((state.problemNum - 1) / state.totalProblems) * 100}%`;
    document.getElementById('problem-counter').textContent =
        `${state.problemNum} / ${state.totalProblems}`;

    const input = document.getElementById('answer-input');
    input.value = '';
    input.className = 'answer-input';
    input.disabled = false;
    input.focus();

    document.getElementById('feedback').textContent = '';
    document.getElementById('feedback').className = 'feedback';
    document.getElementById('hint-text').style.display = 'none';

    // Start timer
    state.timerStart = Date.now();
    clearInterval(state.timerInterval);
    state.timerInterval = setInterval(updateTimer, 100);
}

function updateTimer() {
    if (!state.timerStart) return;
    const elapsed = ((Date.now() - state.timerStart) / 1000).toFixed(1);
    document.getElementById('timer').textContent = `${elapsed}s`;
}

async function submitAnswer() {
    const input = document.getElementById('answer-input');
    const raw = input.value.trim();
    if (raw === '') return;

    clearInterval(state.timerInterval);
    const elapsed = (Date.now() - state.timerStart) / 1000;

    let userAnswer = null;
    const parsed = Number(raw);
    if (!isNaN(parsed)) userAnswer = parsed;

    const isCorrect = userAnswer === state.currentAnswer;

    // Visual feedback
    input.className = `answer-input ${isCorrect ? 'correct' : 'wrong'}`;
    input.disabled = true;

    const feedback = document.getElementById('feedback');
    if (isCorrect) {
        feedback.textContent = `✓ Correct — ${elapsed.toFixed(1)}s`;
        feedback.className = 'feedback correct';
    } else {
        feedback.textContent = `✗ Answer: ${state.currentAnswer} — ${elapsed.toFixed(1)}s`;
        feedback.className = 'feedback wrong';
    }

    // Record
    const result = {
        technique: state.currentTechnique,
        category: state.currentCategory,
        problem: state.currentProblem,
        correct_answer: state.currentAnswer,
        user_answer: userAnswer,
        time_seconds: elapsed,
    };
    state.sessionResults.push({ ...result, is_correct: isCorrect });
    await API.submit(result);

    // Auto-advance after delay
    setTimeout(nextProblem, isCorrect ? 800 : 1500);
}

async function showHint() {
    const data = await API.getHint(state.currentTechnique, state.currentProblem);
    const hintEl = document.getElementById('hint-text');
    if (data.hint) {
        hintEl.textContent = data.hint;
        hintEl.style.display = 'block';
    } else {
        hintEl.textContent = 'No hint available for this technique.';
        hintEl.style.display = 'block';
    }
}

// Summary
function showSummary() {
    clearInterval(state.timerInterval);
    const correct = state.sessionResults.filter(r => r.is_correct).length;
    const total = state.sessionResults.length;
    const totalTime = state.sessionResults.reduce((s, r) => s + r.time_seconds, 0);
    const avgTime = total > 0 ? totalTime / total : 0;

    document.getElementById('summary-score').textContent =
        total > 0 ? `${Math.round((correct / total) * 100)}%` : '—';
    document.getElementById('summary-correct').textContent = `${correct}/${total}`;
    document.getElementById('summary-avg-time').textContent = `${avgTime.toFixed(1)}s`;

    showView('summary');
}

// Stats view
async function loadStats() {
    const stats = await API.getStats();
    const tbody = document.getElementById('stats-body');
    tbody.innerHTML = '';

    const entries = Object.entries(stats).sort();
    if (entries.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4" class="stats-empty">No history yet. Go practice!</td></tr>`;
        return;
    }

    for (const [name, s] of entries) {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${name}</td>
            <td class="mono">${s.total}</td>
            <td class="mono">${(s.accuracy * 100).toFixed(0)}%</td>
            <td class="mono">${s.avg_time.toFixed(1)}s</td>
        `;
        tbody.appendChild(tr);
    }
}

// Navigation
navBtns.practice.addEventListener('click', () => {
    state.mode = 'practice';
    setActiveNav('practice');
    renderTechniqueList();
    showView('select');
    clearInterval(state.timerInterval);
});

navBtns.test.addEventListener('click', () => {
    state.mode = 'test';
    setActiveNav('test');
    renderTechniqueList();
    showView('select');
    clearInterval(state.timerInterval);
});

navBtns.stats.addEventListener('click', () => {
    setActiveNav('stats');
    loadStats();
    showView('stats');
    clearInterval(state.timerInterval);
});

// Practice view controls
document.getElementById('answer-input').addEventListener('keydown', (e) => {
    if (e.key === 'Enter') submitAnswer();
});

document.getElementById('hint-btn').addEventListener('click', showHint);

document.getElementById('back-btn').addEventListener('click', () => {
    clearInterval(state.timerInterval);
    if (state.mode === 'test') {
        navBtns.test.click();
    } else {
        navBtns.practice.click();
    }
});

// Summary controls
document.getElementById('summary-again').addEventListener('click', () => {
    if (state.mode === 'test') {
        startTest(state.testTechniques, state.currentCategory);
    } else {
        startPractice(state.currentTechnique, state.currentCategory);
    }
});

document.getElementById('summary-back').addEventListener('click', () => {
    if (state.mode === 'test') {
        navBtns.test.click();
    } else {
        navBtns.practice.click();
    }
});

// Init
loadTechniques();
setActiveNav('practice');
showView('select');
