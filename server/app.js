import express from "express"
import mongoose from "mongoose";
import User from "./models/userModel.js";
import userRoutes from "./routes/userRoutes.js"
import homeRoute from "./routes/homeRoute.js"
import awarenessRoute from "./routes/awarnessRoute.js"
import historyRoute from "./routes/historyRoute.js"
import session from "express-session";
import flash from "connect-flash";
import passport from "passport";
import { Strategy as LocalStrategy } from "passport-local";
import path from "path"
import { fileURLToPath } from "url";

const app = express();
const port = 8080;
const MONGO_URI = "mongodb://127.0.0.1:27017/food-analyser";

app.set("view engine", "ejs");
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
app.set("views", path.join(__dirname, "../client/users/views"));
app.use(express.static(path.join(__dirname, "../client/users/public"))); // Added static files support
app.use(express.urlencoded({ extended: true }));
app.use(express.json())

main()
  .then(() => {
    console.log("Connected to DB");
  })
  .catch((err) => {
    console.error("DB Connection Error:", err);
  });

async function main() {
  if (!MONGO_URI) {
    throw new Error("Mongo url not defined");
  }
  await mongoose.connect(MONGO_URI);
}

const sessionOptions = {
  secret: "secretcodeforsession",
  resave: false,
  saveUninitialized: true, // Fixed typo savaUninitialized
  cookie: {
    expires: Date.now() + 7 * 24 * 60 * 60 * 1000,
    maxAge: 7 * 24 * 60 * 60 * 1000,
    httpOnly: true,
  }
}

app.use(session(sessionOptions));
app.use(flash());

app.use(passport.initialize());
app.use(passport.session());
passport.use(new LocalStrategy({ usernameField: 'mobileNo' }, User.authenticate()));

passport.serializeUser(User.serializeUser());
passport.deserializeUser(User.deserializeUser());

app.use((req, res, next) => {
  res.locals.success = req.flash("success");
  res.locals.error = req.flash("error"); // Fixed redundant Failure keys
  res.locals.currentUser = req.user;
  next();
});

// Root Route
app.get("/", (req, res) => {
  res.send("I am ROOT");
});

// Routes
app.use("/", userRoutes);
app.use("/home", homeRoute);
app.use("/awareness", awarenessRoute);
app.use("/history", historyRoute);

// 404 handler
app.use((req, res, next) => {
  console.warn(`404 - Not Found: ${req.method} ${req.originalUrl}`);
  const err = new Error("Page Not Found");
  err.statusCode = 404;
  next(err);
});

// Error handling middleware
app.use((err, req, res, next) => {
  let { statusCode = 500, message = "Something went wrong" } = err;
  console.error(`Error [${statusCode}] at ${req.originalUrl}:`, err.message);

  if (process.env.NODE_ENV === 'development') {
    console.error(err.stack);
  }

  res.status(statusCode).send(message);
});

app.listen(port, "0.0.0.0", () => {
  console.log(`App is listening on port ${port}`);
});
