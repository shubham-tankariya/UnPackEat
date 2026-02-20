import mongoose from "mongoose";
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const passportLocalMongoose = require("passport-local-mongoose");
const Schema = mongoose.Schema;

const userSchema = new Schema({
  mobileNo: {
    type: String,
    required: true,
    unique: true,
    match: /^[0-9]{10}$/
  },
  userInfo: {
    firstName: {
      type: String,
      required: true,
    },
    lastName: {
      type: String,
    },
    dateOfBirth: {
      type: Date,
    }

  },
  user_health_profile: {
    conditions: [
      {
        type: String,
      },
    ],
  },
  scanning_History: [
    {
      type: Schema.Types.ObjectId,
      ref: "Product"
    },
  ],
});
const plmPlugin = (passportLocalMongoose && passportLocalMongoose.default) ? passportLocalMongoose.default : passportLocalMongoose;
userSchema.plugin(plmPlugin, {
  usernameField: "mobileNo"
});
const User = mongoose.model("User", userSchema);
export default User;
