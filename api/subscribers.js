import { MongoClient } from 'mongodb';

const uri = process.env.MONGODB_URI;
const options = {
  useUnifiedTopology: true,
  useNewUrlParser: true,
};

export default async function handler(req, res) {
  if (req.method === 'POST') {
    const { email } = req.body;

    if (!email || !email.includes('@')) {
      return res.status(400).json({ message: 'Valid email is required' });
    }

    try {
      const client = await MongoClient.connect(uri, options);
      const db = client.db('netreach');
      const collection = db.collection('subscribers');

      // Check for existing email
      const existing = await collection.findOne({ email });
      if (existing) {
        await client.close();
        return res.status(400).json({ message: 'This email is already registered' });
      }

      // Insert new subscriber
      await collection.insertOne({
        email,
        createdAt: new Date(),
        referralSource: req.headers.referer || 'direct'
      });

      await client.close();
      return res.status(201).json({ 
        success: true, 
        message: 'Thank you for your interest! We\'ll notify you when we launch.' 
      });

    } catch (error) {
      console.error('Subscription error:', error);
      return res.status(500).json({ message: 'Server error, please try again later' });
    }
  } 
  
  // Handle GET request for testing
  else if (req.method === 'GET') {
    try {
      const client = await MongoClient.connect(uri, options);
      const db = client.db('netreach');
      const collection = db.collection('subscribers');
      
      const subscribers = await collection.find()
        .sort({ createdAt: -1 })
        .limit(5)
        .toArray();
      
      await client.close();
      return res.status(200).json(subscribers);
    } catch (error) {
      console.error('Fetch error:', error);
      return res.status(500).json({ message: 'Server error' });
    }
  }

  return res.status(405).json({ message: 'Method not allowed' });
} 