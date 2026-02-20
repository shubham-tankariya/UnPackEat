import mongoose from 'mongoose';

const MONGO_URI = "mongodb://127.0.0.1:27017/food-analyser";

async function cleanDatabase() {
    try {
        await mongoose.connect(MONGO_URI);
        console.log("Connected to DB");

        const db = mongoose.connection.db;
        const collections = await db.listCollections({ name: 'users' }).toArray();

        if (collections.length > 0) {
            await db.collection('users').drop();
            console.log("Successfully dropped 'users' collection to clear all old indexes.");
        } else {
            console.log("'users' collection does not exist.");
        }

        await mongoose.disconnect();
        process.exit(0);
    } catch (err) {
        console.error("Error cleaning database:", err);
        process.exit(1);
    }
}

cleanDatabase();
