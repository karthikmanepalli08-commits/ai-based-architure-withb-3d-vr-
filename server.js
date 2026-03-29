const express = require("express");
const cors = require("cors");

const app = express();

/* Middleware */
app.use(cors());
app.use(express.json());

/* Import Routes */
const predictRoute = require("./routes/predict");

/* Use Routes */
app.use("/api", predictRoute);

/* Test Route (optional but useful) */
app.get("/", (req, res) => {
    res.send("Backend server is running 🚀");
});

/* Start Server */
const PORT = 5000;

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});