import mongoose from "mongoose";

const AdditiveSchema = new mongoose.Schema({
  code: {
    type: String,
    required: true,
    uppercase: true,
    trim: true,
    match: /^E\d+[A-Z]?$/ // e.g., E330, E160C
  },
  type: {
    type: String,
    required: true,
    trim: true,
    maxlength: 50
  }
}, { _id: false });


const NutritionSchema = new mongoose.Schema({
  energy_kcal: {
    type: Number,
    min: 0,
    max: 2000
  },
  fat: {
    type: Number,
    min: 0,
    max: 100
  },
  saturated_fat: {
    type: Number,
    min: 0,
    max: 100
  },
  carbohydrates: {
    type: Number,
    min: 0,
    max: 100
  },
  sugars: {
    type: Number,
    min: 0,
    max: 100
  },
  protein: {
    type: Number,
    min: 0,
    max: 100
  },
  fiber: {
    type: Number,
    min: 0,
    max: 100
  },
  salt: {
    type: Number,
    min: 0,
    max: 10
  }
}, { _id: false });


const IngredientsSchema = new mongoose.Schema({
  ingredients_text: {
    type: String,
    required: true,
    minlength: 5,
    maxlength: 3000
  },
  total_count: {
    type: Number,
    min: 0,
    max: 500
  },
  additives_count: {
    type: Number,
    min: 0,
    max: 100
  },
  contains_palm_oil: {
    type: Boolean,
    required: true
  },
  decoded_additives: {
    type: [AdditiveSchema],
    default: []
  }
}, { _id: false });


const BasicInfoSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    trim: true,
    minlength: 2,
    maxlength: 200
  },
  brand: {
    type: String,
    trim: true,
    maxlength: 100
  },
  quantity: {
    type: String,
    trim: true,
    maxlength: 50
  },
  image: {
    type: String,
    match: /^https?:\/\/.+/
  },
  category: {
    type: String,
    trim: true,
    maxlength: 200
  }
}, { _id: false });


const MetaSchema = new mongoose.Schema({
  nova_group: {
    type: Number,
    min: 1,
    max: 4
  },
  ecoscore_grade: {
    type: String,
    lowercase: true,
    enum: ["a", "b", "c", "d", "e"]
  },
  packaging_materials: {
    type: [String],
    default: []
  },
  traces: {
    type: [String],
    default: []
  },
  allergens_detected: {
    type: [String],
    default: []
  }
}, { _id: false });


const SummarySchema = new mongoose.Schema({
  health_score: {
    type: Number,
    required: true,
    min: 0,
    max: 100
  },
  verdict: {
    type: String,
    required: true,
    enum: [
      "Safe",
      "Moderate",
      "Limit consumption",
      "Avoid"
    ]
  },
  risk_flags: {
    type: [String],
    default: []
  },
  positives: {
    type: [String],
    default: []
  },
  warnings: {
    type: [String],
    default: []
  },
  nova_group: {
    type: Number,
    min: 1,
    max: 4
  },
  additives_count: {
    type: Number,
    min: 0,
    max: 100
  }
}, { _id: false });


const ProductSchema = new mongoose.Schema({
  barcode: {
    type: Number,
    required: true,
    unique: true,
    index: true,
    validate: {
      validator: v => Number.isInteger(v) && v > 0,
      message: "Barcode must be a positive number"
    }
  },

  summary: {
    type: SummarySchema,
    required: true
  },

  details: {
    basic_info: {
      type: BasicInfoSchema,
      required: true
    },
    nutrition: {
      type: NutritionSchema,
      required: true
    },
    ingredients: {
      type: IngredientsSchema,
      required: true
    },
    meta: {
      type: MetaSchema,
      required: true
    }
  },
});


export default mongoose.model("Product", ProductSchema);
