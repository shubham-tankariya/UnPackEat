import express from "express";
import { IsLoggedIn } from "../middlewares/isLoggedIn.js";
import fs from "fs/promises";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const router = express.Router();

import Product from "../models/productModel.js";

// Analysis page - renders the detailed food analytics or performs a new search
router.get("/", IsLoggedIn, async (req, res) => {
    const { barcode } = req.query;

    if (barcode) {
        let cleanBarcode = barcode.trim();
        try {
            // 1. Try Database First
            let data = await Product.findOne({ barcode: cleanBarcode });

            if (data) {
                console.log(`Found product ${cleanBarcode} in Database.`);
                req.session.searchProductdata = data;
                return res.render("analysis.ejs", { productData: data, source: 'database', page: 'analysis' });
            }

            // 2. Fallback to Python API
            console.log(`Product ${cleanBarcode} not in DB, calling Python API...`);
            try {
                const response = await fetch(`http://localhost:8000/product/${cleanBarcode}`);

                if (!response.ok) {
                    throw new Error(`Python API responded with status: ${response.status}`);
                }

                const apiData = await response.json();

                if (apiData) {
                    // Upsert into Database for future high-speed access
                    await Product.findOneAndUpdate(
                        { barcode: cleanBarcode },
                        apiData,
                        { upsert: true, new: true }
                    );
                    console.log(`Successfully fetched and saved product ${cleanBarcode} from Python API.`);

                    req.session.searchProductdata = apiData;
                    return res.render("analysis.ejs", { productData: apiData, source: 'live', page: 'analysis' });
                }
            } catch (apiError) {
                console.error("Python API Error:", apiError.message);
                // Fallback to filesystem check if API fails (legacy support)
                console.log(`Checking legacy filesystem for ${cleanBarcode}...`);

                let dataPath = path.join(__dirname, "../py-backend/app/data", `${cleanBarcode}.json`);
                try {
                    const rawData = await fs.readFile(dataPath, "utf-8");
                    const fsData = JSON.parse(rawData);
                    req.session.searchProductdata = fsData;
                    return res.render("analysis.ejs", { productData: fsData, source: 'filesystem', page: 'analysis' });
                } catch (fsError) {
                    throw new Error(`Product not found in DB, API, or Filesystem.`);
                }
            }

        } catch (error) {
            console.error("Search Error for barcode:", cleanBarcode, error.message);
            req.flash("error", `Product (${cleanBarcode}) not found. Please ensure the Python backend is running or try another barcode.`);
            return res.redirect("/home");
        }
    }

    const productData = req.session.searchProductdata;

    if (!productData) {
        req.flash("error", "No product data found to analyze. Please search for a product first.");
        return res.redirect("/home");
    }

    res.render("analysis.ejs", { productData, source: 'session', page: 'analysis' });
});

export default router;
