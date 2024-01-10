const express = require('express');
const multer = require('multer');
const bodyParser = require('body-parser');
const { execFile } = require('child_process');
const path = require('path');
const fs = require('fs');

const app = express();
const port = 3001;


const storage = multer.memoryStorage();
const upload = multer({ storage: storage }).single('file'); // Update 'file' to match the name attribute in your HTML form


app.use(express.static('Public'));


app.use(bodyParser.json());


app.post('/upload', (req, res) => {
    upload(req, res, (err) => {
        if (err) {
            return res.status(400).json({ error: 'Error uploading file' });
        }

        if (!req.file) {
            return res.status(400).json({ error: 'No file uploaded' });
        }

        
        const tempImagePath = path.join(__dirname, 'uploads', 'tempImage.jpg');
        fs.writeFileSync(tempImagePath, req.file.buffer);


        const pythonScriptPath = '';// path of script
        const modelPath = '';//path of ML model
        const command = 'python3';
        const args = [pythonScriptPath, tempImagePath, modelPath];

        execFile(command, args, (error, stdout, stderr) => {
            fs.unlinkSync(tempImagePath); 

            if (error) {
                console.error(`Error executing Python script: ${error}`);
                return res.status(500).json({ error: 'Internal server error' });
            }

            const prediction = stdout.trim();
            res.json({ prediction });
        });
    });
});


app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'Public', 'disease-prediction.html'));
});


app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
