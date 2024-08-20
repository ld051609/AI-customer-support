// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyBogr5S5RwE9zcbfa7lDaDuX92sWGzYITc",
  authDomain: "ai-rag-chatbot-4b469.firebaseapp.com",
  projectId: "ai-rag-chatbot-4b469",
  storageBucket: "ai-rag-chatbot-4b469.appspot.com",
  messagingSenderId: "26479359878",
  appId: "1:26479359878:web:5328281b525ea3aa2bde07",
  measurementId: "G-3MZDZ45WRN"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
export { auth };