import express from "express";
import { IsLoggedIn } from "../middlewares/isLoggedIn.js";

const router = express.Router();

// Home page - renders the barcode search field
router.get("/", IsLoggedIn, (req, res) => {
    const searchProductdata = req.session.searchProductdata || null;
    // Clear the session data after fetching if you only want it to show once, 
    // or keep it if you want it to persist until next search.
    // req.session.searchProductdata = null; 
    res.render("home.ejs", { searchProductdata });
});

// Search route - handles barcode submission and calls Python API
router.post("/search", IsLoggedIn, async (req, res) => {
    const { barcode } = req.body;

    if (!barcode) {
        req.flash("error", "Please enter a barcode");
        return res.redirect("/home");
    }

    try {
        // Calling the Python FastAPI backend
        // Defaulting to http://127.0.0.1:8000 based on common FastAPI/Uvicorn defaults
        const response = await fetch(`http://127.0.0.1:8000/product/${barcode}`);

        if (!response.ok) {
            throw new Error(`Python API responded with status: ${response.status}`);
        }

        const data = await response.json();

        // Storing data in session as requested
        console.log(data);
        req.session.searchProductdata = data;

        req.flash("success", "Product analysis completed!");
        res.redirect("/home");

    } catch (error) {
        console.error("Search Error:", error);
        req.flash("error", "Failed to fetch product data. Ensure the analysis engine is running.");
        res.redirect("/home");
    }
});

export default router;
