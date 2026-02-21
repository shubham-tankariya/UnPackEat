import express from "express";
import { IsLoggedIn } from "../middlewares/isLoggedIn.js";

const router = express.Router();

router.get("/", IsLoggedIn, (req, res) => {
    res.render("awareness", { page: 'awareness' });
});

export default router;
