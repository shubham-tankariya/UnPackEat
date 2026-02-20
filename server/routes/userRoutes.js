import express from "express";
import passport from "passport";
import User from "../models/userModel.js";
import { wrapAsync } from "../utils/wrapAsync.js";

const router = express.Router();

// signup page get request
router.get("/signup", (req, res) => {
  res.render("signup.ejs");
});

// post request for signup
router.post(
  "/signup",
  wrapAsync(async (req, res, next) => {
    try {
      const { mobileNo, firstName, password } = req.body;

      const newUser = new User({
        mobileNo: mobileNo,
        userInfo: {
          firstName: firstName
        }
      });

      const registeredUser = await User.register(newUser, password);

      req.login(registeredUser, (err) => {
        if (err) return next(err);
        req.flash("success", "Welcome to Fooder!");
        res.redirect("/home");
      });
    } catch (e) {
      req.flash("error", e.message);
      res.redirect("/signup");
    }
  })
);

// login page get request
router.get("/login", (req, res) => {
  res.render("login.ejs");
});

// post request for login
router.post("/login",
  passport.authenticate("local", {
    failureRedirect: "/login",
    failureFlash: true
  }),
  (req, res) => {
    req.flash("success", "Welcome back to Fooder!");
    res.redirect("/home");
  });

// Logout route (optional but good for testing)
router.get("/logout", (req, res, next) => {
  req.logout((err) => {
    if (err) return next(err);
    req.flash("success", "Logged out successfully");
    res.redirect("/login");
  });
});

export default router;