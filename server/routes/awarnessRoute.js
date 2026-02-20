import express from "express";
import { IsLoggedIn } from "../middlewares/isLoggedIn.js";

const router = express.Router();

router.get("/", IsLoggedIn, (req, res) => {
    res.send("I am awareness route");
});

export default router;
