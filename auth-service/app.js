const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const authRoutes = require('./routes/auth'); // Authentication routes

const app = express();

// Middleware to parse JSON request bodies
app.use(bodyParser.json());

// Serve static files (your HTML, CSS, etc.)
app.use(express.static(path.join(__dirname, 'public')));

// Use authentication routes
app.use('/auth', authRoutes);

// Start the server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Authentication service running on port ${PORT}`);
});

const cors = require('cors');
const jwt = require('jsonwebtoken');

app.post('/auth/login', (req, res) => {
  const { username, password } = req.body;

  // Authenticate the user
  if (username === 'yourUsername' && password === 'yourPassword') {
    // Create a JWT token
    const token = jwt.sign({ username }, 'yourSecretKey', { expiresIn: '1h' });
    res.json({ message: 'Login successful', loggedIn: true, token });
  } else {
    res.json({ message: 'Invalid credentials', loggedIn: false });
  }
});

// Use CORS middleware
app.use(cors({
  origin: 'http://35.193.220.231:5001', // Allow requests from the Enter Data app
}));
