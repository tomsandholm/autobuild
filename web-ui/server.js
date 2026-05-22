const express = require('express');
const { exec } = require('child_process');
const path = require('path');
const app = express();
const port = 3000;

app.use(express.json());
app.use(express.static('public'));

app.post('/api/node', (req, res) => {
    const { fqdn, role } = req.body;
    if (!fqdn || !role) {
        return res.status(400).json({ error: 'FQDN and ROLE are required' });
    }

    const command = `make node NAME=${fqdn} ROLE=${role}`;
    console.log(`Executing: ${command}`);

    exec(command, { cwd: path.join(__dirname, '..') }, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return res.status(500).json({ error: error.message, details: stderr });
        }
        res.json({ message: 'Node created successfully', output: stdout });
    });
});

app.post('/api/delete', (req, res) => {
    const { fqdn } = req.body;
    if (!fqdn) {
        return res.status(400).json({ error: 'FQDN is required' });
    }

    const command = `make Delete NAME=${fqdn}`;
    console.log(`Executing: ${command}`);

    exec(command, { cwd: path.join(__dirname, '..') }, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return res.status(500).json({ error: error.message, details: stderr });
        }
        res.json({ message: 'Node deleted successfully', output: stdout });
    });
});

app.listen(port, () => {
    console.log(`Web UI listening at http://localhost:${port}`);
});
