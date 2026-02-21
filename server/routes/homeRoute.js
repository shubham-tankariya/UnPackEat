import express from "express";
import { IsLoggedIn } from "../middlewares/isLoggedIn.js";

const router = express.Router();

// Home page - renders the barcode search field
router.get("/", IsLoggedIn, (req, res) => {
    const searchProductdata = req.session.searchProductdata || null;
    res.render("home.ejs", { searchProductdata, page: 'home' });
});

export default router;
