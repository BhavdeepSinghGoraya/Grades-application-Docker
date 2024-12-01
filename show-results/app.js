// app.js
const express = require('express');
const { MongoClient } = require('mongodb');
const path = require('path');

const app = express();
const port = process.env.PORT || 8000;
const mongoUri = 'mongodb://mongo-db:27017'; // Docker service name for MongoDB

const client = new MongoClient(mongoUri);

app.get('/show-results', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});
app.get('/get-latest-entry', async (req, res) => {
    try {
        await client.connect();
        const database = client.db('analytics_db'); // Your MongoDB database
        const collection = database.collection('grade_statistics'); // Your MongoDB collection

        const latestEntry = await collection.find().sort({ _id: -1 }).limit(1).toArray();
        res.status(200).json(latestEntry[0]); // Send the latest entry as JSON
    } catch (error) {
        console.error('Error retrieving latest entry:', error);
        res.status(500).send('Error retrieving latest entry');
    } finally {
        await client.close();
    }
});

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}/show-results`);
});
