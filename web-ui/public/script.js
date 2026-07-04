const fqdnInput = document.getElementById('fqdn');
const roleSelect = document.getElementById('role');
const ramInput = document.getElementById('ram');
const ncpuInput = document.getElementById('ncpu');
const nodeBtn = document.getElementById('nodeBtn');
const deleteBtn = document.getElementById('deleteBtn');
const statusDiv = document.getElementById('status');
const outputPre = document.getElementById('output');

function setStatus(message, type) {
    statusDiv.textContent = message;
    statusDiv.className = `status ${type}`;
    statusDiv.style.display = 'block';
}

function showOutput(output) {
    outputPre.textContent = output;
    outputPre.style.display = 'block';
}

function clearDisplay() {
    statusDiv.style.display = 'none';
    outputPre.style.display = 'none';
}

async function handleAction(endpoint, body) {
    const originalNodeBtnText = nodeBtn.textContent;
    const originalDeleteBtnText = deleteBtn.textContent;
    
    nodeBtn.disabled = true;
    deleteBtn.disabled = true;
    clearDisplay();
    setStatus('Processing...', 'success');

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        });

        const data = await response.json();

        if (response.ok) {
            setStatus(data.message, 'success');
            if (data.output) showOutput(data.output);
        } else {
            setStatus(data.error || 'An error occurred', 'error');
            if (data.details) showOutput(data.details);
        }
    } catch (error) {
        setStatus(`Network error: ${error.message}`, 'error');
    } finally {
        nodeBtn.disabled = false;
        deleteBtn.disabled = false;
    }
}

nodeBtn.addEventListener('click', () => {
    const fqdn = fqdnInput.value.trim();
    const role = roleSelect.value;
    const ram = ramInput.value.trim();
    const ncpu = ncpuInput.value.trim();
    
    if (!fqdn) {
        setStatus('Please enter an FQDN', 'error');
        return;
    }
    handleAction('/api/node', { fqdn, role, ram, ncpu });
});

deleteBtn.addEventListener('click', () => {
    const fqdn = fqdnInput.value.trim();
    if (!fqdn) {
        setStatus('Please enter an FQDN', 'error');
        return;
    }
    if (confirm(`Are you sure you want to delete ${fqdn}?`)) {
        handleAction('/api/delete', { fqdn });
    }
});
