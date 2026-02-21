import mongoose from "mongoose";

const ProductSchema = new mongoose.Schema({
  barcode: {
    type: String,
    required: true,
    unique: true,
    index: true
  },

  product: {
    code: String,
    name: String,
    brand: String,
    image: String,
    quantity: String,
    categories: [String]
  },

  highlights: {
    health_score: Number,
    verdict: String,
    likes: [String],
    concerns: [String],
    nova_group: Number
  },

  nutrients: [{
    name: String,
    amount_100g: Number,
    unit: String,
    rda_percent: Number,
    rating: String
  }],

  nutrient_radar: {
    type: Map,
    of: Number
  },

  ingredients: {
    text: String,
    ingredients: [mongoose.Schema.Types.Mixed],
    additives: [mongoose.Schema.Types.Mixed],
    dominant: [mongoose.Schema.Types.Mixed],
    contains_palm_oil: Boolean,
    complexity: String
  },

  additives_full: [mongoose.Schema.Types.Mixed],

  allergens: [String],

  serving: {
    per_100g: mongoose.Schema.Types.Mixed,
    per_serving: mongoose.Schema.Types.Mixed,
    serving_size_g: Number
  },

  metadata: {
    nova_group: Number,
    nova_group_error: String,
    nutriscore_grade: String,
    nutrient_levels: mongoose.Schema.Types.Mixed,
    labels: [String],
    food_groups: [String],
    countries: [String],
    off_completeness: Number,
    data_quality_warnings: [String],
    nutrition_data_per: String
  },

  environment: {
    ecoscore: String,
    packaging: [String]
  },

  ai_insights: {
    summary: String,
    key_benefits: [String],
    key_concerns: [String],
    consumption_advice: String,
    alternative_suggestions: [String],
    detailed_analysis: String,
    who_should_avoid: String,
    ideal_consumption: String
  }

}, { timestamps: true });

export default mongoose.model("Product", ProductSchema);
