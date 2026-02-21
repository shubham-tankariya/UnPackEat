import express from "express";
import { IsLoggedIn } from "../middlewares/isLoggedIn.js";
import User from "../models/userModel.js";
import { wrapAsync } from "../utils/wrapAsync.js";

const router = express.Router();

// Get user detail page
router.get("/", IsLoggedIn, wrapAsync(async (req, res) => {
    res.render("user_detail.ejs", { page: 'user_detail' });
}));

// Update user details and preferences
router.post("/update", IsLoggedIn, wrapAsync(async (req, res) => {
    const { firstName, lastName, conditions } = req.body;

    // Ensure conditions is an array
    const conditionArray = Array.isArray(conditions) ? conditions : (conditions ? [conditions] : []);

    await User.findByIdAndUpdate(req.user._id, {
        "userInfo.firstName": firstName,
        "userInfo.lastName": lastName,
        "user_health_profile.conditions": conditionArray
    });

    req.flash("success", "Profile updated successfully!");
    res.redirect("/user_detail");
}));

export default router;
