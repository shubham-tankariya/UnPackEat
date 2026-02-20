export const IsLoggedIn = (req, res, next) => {

    if (!req.isAuthenticated()) {
        console.log(req.originalUrl);
        req.session.redirectUrl = req.originalUrl;
        req.flash("error", "Login is Required")
        return res.redirect("/login");
    }
    next();
};
