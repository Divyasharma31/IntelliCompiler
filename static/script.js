document.addEventListener('DOMContentLoaded', () => {
    // Initialize CodeMirror
    const editor = CodeMirror.fromTextArea(document.getElementById('code-editor'), {
        lineNumbers: true,
        mode: 'text/x-c++src',
        theme: 'dracula',
        indentUnit: 4,
        matchBrackets: true,
        autoCloseBrackets: true,
        lineWrapping: true
    });

    // State
    let currentErrors = {
        lexical: [],
        syntax: [],
        semantic: []
    };
    let lastCorrectedCode = '';

    // Elements
    const btnLexical = document.getElementById('btn-lexical');
    const btnSyntax = document.getElementById('btn-syntax');
    const btnSemantic = document.getElementById('btn-semantic');
    const btnAI = document.getElementById('btn-ai');
    const btnApplyFix = document.getElementById('btn-apply-fix');
    const btnDownload = document.getElementById('btn-download');
    
    const loadingOverlay = document.getElementById('loading-overlay');
    
    const step1 = document.getElementById('step-1');
    const step2 = document.getElementById('step-2');
    const step3 = document.getElementById('step-3');
    const step4 = document.getElementById('step-4');

    const results = {
        lexical: document.getElementById('lexical-results'),
        syntax: document.getElementById('syntax-results'),
        semantic: document.getElementById('semantic-results'),
        ai: document.getElementById('ai-results')
    };

    // Load example code
    fetch('/example')
        .then(res => res.json())
        .then(data => {
            editor.setValue(data.code);
        });

    // Helper: Show/Hide sections
    function showSection(name) {
        Object.keys(results).forEach(key => {
            if (key === name) {
                results[key].classList.remove('hidden');
                results[key].scrollIntoView({ behavior: 'smooth' });
            } else {
                results[key].classList.add('hidden');
            }
        });
    }

    function updateStep(stepNum) {
        [step1, step2, step3, step4].forEach((s, i) => {
            if (i < stepNum - 1) {
                s.classList.add('completed');
                s.classList.remove('active');
            } else if (i === stepNum - 1) {
                s.classList.add('active');
                s.classList.remove('completed');
            } else {
                s.classList.remove('active', 'completed');
            }
        });
    }

    // Lexical Analysis
    btnLexical.addEventListener('click', async () => {
        const code = editor.getValue();
        const res = await fetch('/run_phase', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code, phase: 'lexical' })
        });
        const data = await res.json();
        
        currentErrors.lexical = data.errors;
        
        // Update UI
        const errList = document.getElementById('lex-errors');
        errList.innerHTML = '';
        data.errors.forEach(err => {
            const div = document.createElement('div');
            div.className = 'error-item';
            div.textContent = err;
            errList.appendChild(div);
        });

        const tableBody = document.querySelector('#tokens-table tbody');
        tableBody.innerHTML = '';
        data.tokens.forEach(t => {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>${t.type}</td><td><code>${t.value}</code></td><td>${t.line}</td>`;
            tableBody.appendChild(tr);
        });

        showSection('lexical');
        updateStep(1);
        btnSyntax.disabled = false;
        btnSyntax.classList.add('primary');
        btnSyntax.classList.remove('secondary');
    });

    // Syntax Analysis
    btnSyntax.addEventListener('click', async () => {
        const code = editor.getValue();
        const res = await fetch('/run_phase', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code, phase: 'syntax' })
        });
        const data = await res.json();
        
        currentErrors.syntax = data.errors;

        const errList = document.getElementById('syn-errors');
        errList.innerHTML = '';
        data.errors.forEach(err => {
            const div = document.createElement('div');
            div.className = 'error-item';
            div.textContent = err;
            errList.appendChild(div);
        });

        const treeView = document.getElementById('parse-tree');
        treeView.textContent = data.tree.join('\n');

        showSection('syntax');
        updateStep(2);
        btnSemantic.disabled = false;
        btnSemantic.classList.add('primary');
        btnSemantic.classList.remove('secondary');
    });

    // Semantic Analysis
    btnSemantic.addEventListener('click', async () => {
        const code = editor.getValue();
        const res = await fetch('/run_phase', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code, phase: 'semantic' })
        });
        const data = await res.json();
        
        currentErrors.semantic = data.errors;

        const errList = document.getElementById('sem-errors');
        errList.innerHTML = '';
        data.errors.forEach(err => {
            const div = document.createElement('div');
            div.className = 'error-item';
            div.textContent = err;
            errList.appendChild(div);
        });

        const warnList = document.getElementById('sem-warnings');
        warnList.innerHTML = '';
        data.warnings.forEach(warn => {
            const div = document.createElement('div');
            div.className = 'warning-item';
            div.textContent = warn;
            warnList.appendChild(div);
        });

        const tableBody = document.querySelector('#symbols-table tbody');
        tableBody.innerHTML = '';
        data.symbol_table.forEach(s => {
            const tr = document.createElement('tr');
            tr.innerHTML = `<td>${s.name}</td><td>${s.type}</td>`;
            tableBody.appendChild(tr);
        });

        showSection('semantic');
        updateStep(3);
        btnAI.disabled = false;
    });

    // AI Correction
    btnAI.addEventListener('click', async () => {
        loadingOverlay.classList.remove('hidden');
        
        const code = editor.getValue();
        // Collect all errors
        const allErrors = [
            ...currentErrors.lexical,
            ...currentErrors.syntax,
            ...currentErrors.semantic
        ];

        try {
            const res = await fetch('/ai_correct', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    code, 
                    errors: allErrors,
                    phase: 'all' // We send all errors to AI
                })
            });
            const data = await res.json();
            
            if (data.error) {
                alert(data.error);
                return;
            }

            document.getElementById('ai-explanation').textContent = data.explanation;
            document.getElementById('ai-code-preview').textContent = data.corrected_code;
            document.getElementById('ai-tip').textContent = `💡 Pro Tip: ${data.tip}`;
            
            lastCorrectedCode = data.corrected_code;
            
            showSection('ai');
            updateStep(4);
        } catch (e) {
            console.error(e);
            alert("AI service unavailable. Please check if your API keys are set.");
        } finally {
            loadingOverlay.classList.add('hidden');
        }
    });

    // Apply Fix
    btnApplyFix.addEventListener('click', () => {
        editor.setValue(lastCorrectedCode);
        btnDownload.classList.remove('hidden');
        alert("Corrected code applied to editor! You can now re-run the analysis.");
    });

    // Download
    btnDownload.addEventListener('click', () => {
        const blob = new Blob([editor.getValue()], { type: 'text/x-c++src' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'corrected_code.cpp';
        a.click();
        URL.revokeObjectURL(url);
    });
});
