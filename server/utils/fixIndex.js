import mongoose from 'mongoose';

const MONGO_URI = "mongodb://127.0.0.1:27017/food-analyser";

async function fixIndex() {
    try {
        await mongoose.connect(MONGO_URI);
        console.log("Connected to DB");

        const collection = mongoose.connection.db.collection('users');

        // List indexes
        const indexes = await collection.indexes();
        console.log("Current indexes:", indexes.map(i => i.name));

        if (indexes.find(i => i.name === 'username_1')) {
            await collection.dropIndex('username_1');
            console.log("Successfully dropped 'username_1' index");
        } else {
            console.log("'username_1' index not found");
        }

        await mongoose.disconnect();
        process.exit(0);
    } catch (err) {
        console.error("Error fixing index:", err);
        process.exit(1);
    }
}

fixIndex();
