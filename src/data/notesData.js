export const NOTES_DATA = [
  {
    id: "html-css-mastery",
    title: "HTML5 & Modern CSS3 Visual Cheatsheet",
    category: "Frontend",
    tag: "Essential",
    badgeColor: "#f97316",
    price: 50,
    originalPrice: 199,
    rating: 4.9,
    reviewsCount: 420,
    downloads: "2.8k+",
    pages: 38,
    format: "Color PDF (High Res)",
    description: "Master Flexbox, CSS Grid, Responsive Design, Semantic HTML, CSS Variables, and 50+ interview-ready CSS tricks with visual flowcharts.",
    topics: [
      "Semantic HTML5 & Accessibility (ARIA)",
      "Flexbox & CSS Grid complete layout visual guide",
      "CSS Positioning, Z-Index stacking context & BFC",
      "Modern CSS Variables, Media Queries & Clamp()",
      "Top 30 Frontend Interview CSS Questions"
    ],
    samplePages: [
      {
        pageNumber: 1,
        title: "Flexbox vs Grid Architecture Matrix",
        content: `/* Flexbox: 1-Dimensional (Row OR Column) */
.container {
  display: flex;
  justify-content: space-between; /* Main Axis */
  align-items: center;            /* Cross Axis */
  gap: 1.5rem;
}

/* CSS Grid: 2-Dimensional (Rows AND Columns) */
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}

💡 Pro Tip: Use Flexbox for UI components (navbars, cards), and Grid for overall page layouts!`
      },
      {
        pageNumber: 2,
        title: "Responsive Typography & clamp() Magic",
        content: `/* Fluid typography without 20 media queries */
h1 {
  /* clamp(MIN, VAL, MAX) */
  font-size: clamp(2rem, 5vw + 1rem, 4.5rem);
}

/* Perfect centering in 2 lines */
.center-box {
  display: grid;
  place-items: center;
}

📌 Common Gotcha: Always specify fallback fonts and use rem units for accessibility.`
      }
    ]
  },
  {
    id: "javascript-es6-deepdive",
    title: "Modern JavaScript (ES6+ & Async) Revision Notes",
    category: "Frontend",
    tag: "Bestseller",
    badgeColor: "#eab308",
    price: 50,
    originalPrice: 249,
    rating: 5.0,
    reviewsCount: 890,
    downloads: "5.4k+",
    pages: 56,
    format: "Color PDF (High Res)",
    description: "Closures, Prototypes, Event Loop, Promises, Async/Await, Web APIs, and Core Engine internals explained with clear handwritten style diagrams.",
    topics: [
      "Execution Context, Call Stack & Hoisting",
      "Closures, Currying & Lexical Scope in depth",
      "Event Loop, Microtasks (Promises) vs Macrotasks (setTimeout)",
      "Prototypes, __proto__, Prototypal Inheritance & Class syntax",
      "Array Methods (map, filter, reduce, flatMap) Master table"
    ],
    samplePages: [
      {
        pageNumber: 1,
        title: "Event Loop & Microtask Execution Order",
        content: `console.log("1 - Start");

setTimeout(() => {
  console.log("2 - Macrotask (setTimeout)");
}, 0);

Promise.resolve().then(() => {
  console.log("3 - Microtask (Promise)");
});

console.log("4 - End");

// ⚡ Output Order: 1 -> 4 -> 3 -> 2
// Explanation: Microtask queue is processed IMMEDIATELY after Call Stack empties, before any Macrotask!`
      },
      {
        pageNumber: 2,
        title: "Closures & Memoization Pattern",
        content: `function memoize(fn) {
  const cache = {};
  return function(...args) {
    const key = JSON.stringify(args);
    if (cache[key]) return cache[key];
    const result = fn.apply(this, args);
    cache[key] = result;
    return result;
  };
}

// Memory diagram included in full PDF showing closure variable retention.`
      }
    ]
  },
  {
    id: "react-19-hooks-mastery",
    title: "React 19 & Hooks Architecture Cheatsheet",
    category: "Frontend",
    tag: "Trending",
    badgeColor: "#06b6d4",
    price: 50,
    originalPrice: 249,
    rating: 4.9,
    reviewsCount: 710,
    downloads: "4.1k+",
    pages: 48,
    format: "Color PDF (High Res)",
    description: "Master React Lifecycle, Virtual DOM vs Fiber, Reconciliation, useState, useEffect, useMemo, useCallback, custom hooks & React 19 Actions.",
    topics: [
      "Virtual DOM, Diffing Algorithm & React Fiber Tree",
      "useEffect vs useLayoutEffect vs useInsertionEffect",
      "useMemo vs useCallback: Performance optimization rules",
      "Custom Hooks design patterns with real-world examples",
      "State management: Context API vs Zustand vs Redux Toolkit"
    ],
    samplePages: [
      {
        pageNumber: 1,
        title: "useCallback vs useMemo Decision Tree",
        content: `// 🎯 Rule of Thumb:
// useMemo: Caches the RETURN VALUE of a calculation
const calculatedTotal = useMemo(() => {
  return cart.reduce((acc, item) => acc + item.price, 0);
}, [cart]);

// useCallback: Caches the FUNCTION REFERENCE itself (stops re-renders of memoized child)
const handleItemClick = useCallback((id) => {
  setSelectedId(id);
}, []); // Empty deps = stable reference across renders!`
      },
      {
        pageNumber: 2,
        title: "Custom Hook: useDebounce Implementation",
        content: `import { useState, useEffect } from 'react';

export function useDebounce(value, delay = 300) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer); // Cleanup on rapid typing
  }, [value, delay]);

  return debouncedValue;
}`
      }
    ]
  },
  {
    id: "nodejs-express-backend",
    title: "Node.js & Express.js Backend Architecture Notes",
    category: "Backend",
    tag: "Most Popular",
    badgeColor: "#22c55e",
    price: 50,
    originalPrice: 199,
    rating: 4.8,
    reviewsCount: 540,
    downloads: "3.2k+",
    pages: 44,
    format: "Color PDF (High Res)",
    description: "Libuv, Event Loop threads, Streams, Buffers, Express Middleware pipelines, JWT Authentication, Error Handling & RESTful standard architectures.",
    topics: [
      "Node.js Architecture: V8, Libuv, Thread Pool & Worker Threads",
      "Streams & Buffers: Handling large files without memory crashes",
      "Express Middleware Architecture & Global Error Handlers",
      "JWT Authentication, Refresh Tokens & Cookie Security",
      "Rate Limiting, Helmet, CORS & API Security Checklist"
    ],
    samplePages: [
      {
        pageNumber: 1,
        title: "Express Centralized Error Handling Pipeline",
        content: `// Custom Error Class
class AppError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
    this.status = \`\${statusCode}\`.startsWith('4') ? 'fail' : 'error';
    this.isOperational = true;
  }
}

// Global Error Middleware (Must have 4 arguments!)
app.use((err, req, res, next) => {
  err.statusCode = err.statusCode || 500;
  res.status(err.statusCode).json({
    status: err.status || 'error',
    message: err.message
  });
});`
      },
      {
        pageNumber: 2,
        title: "JWT Access + Refresh Token Flow",
        content: `// 1. Client logs in -> Server sends short-lived Access Token (15m) + HttpOnly Refresh Token (7d)
// 2. Client sends Access Token in Authorization header: Bearer <token>
// 3. When Access Token expires (401), client calls /api/auth/refresh to get new Access Token.`
      }
    ]
  },
  {
    id: "mongodb-mongoose-mastery",
    title: "MongoDB & Mongoose Schema Design & Aggregations",
    category: "Database",
    tag: "High Yield",
    badgeColor: "#10b981",
    price: 50,
    originalPrice: 199,
    rating: 4.9,
    reviewsCount: 380,
    downloads: "2.5k+",
    pages: 36,
    format: "Color PDF (High Res)",
    description: "Indexing strategies, Aggregation Pipelines ($match, $group, $lookup, $unwind), Embedding vs Referencing, and Mongoose Hooks & Virtuals.",
    topics: [
      "Embedding (1:Few) vs Referencing (1:Many) design rules",
      "Compound Indexes, ESR Rule (Equality, Sort, Range)",
      "Aggregation Pipeline step-by-step visual blueprint",
      "Mongoose Pre/Post Middleware & Virtual Population",
      "Transactions & ACID compliance in MongoDB"
    ],
    samplePages: [
      {
        pageNumber: 1,
        title: "Aggregation Pipeline Blueprint ($lookup + $group)",
        content: `// Calculate total revenue per student
db.orders.aggregate([
  { $match: { status: "PAID" } },
  { 
    $group: {
      _id: "$userId",
      totalSpent: { $sum: "$amount" },
      notesPurchased: { $push: "$noteTitle" }
    }
  },
  { $sort: { totalSpent: -1 } },
  { $limit: 10 }
]);`
      },
      {
        pageNumber: 2,
        title: "Compound Indexing: The ESR Rule",
        content: `/* ESR Rule: Equality -> Sort -> Range */
// If query is: db.notes.find({ category: "Frontend", price: { $lte: 100 } }).sort({ rating: -1 })
// Optimal Index:
db.notes.createIndex({
  category: 1,  // E (Equality)
  rating: -1,   // S (Sort)
  price: 1      // R (Range)
});`
      }
    ]
  },
  {
    id: "aws-cloud-developers",
    title: "AWS Cloud for MERN Developers (S3, EC2, IAM)",
    category: "Cloud",
    tag: "Top Rated",
    badgeColor: "#f59e0b",
    price: 50,
    originalPrice: 299,
    rating: 5.0,
    reviewsCount: 650,
    downloads: "3.9k+",
    pages: 60,
    format: "Color PDF (High Res)",
    description: "Practical AWS for full-stack developers: S3 private buckets & Pre-signed URLs, EC2 setup with Nginx reverse proxy, IAM Least Privilege, and CloudFront CDN.",
    topics: [
      "AWS S3: Private bucket security, CORS, & Pre-signed URL generation",
      "AWS EC2: Ubuntu instance, SSH, PM2 process manager & Nginx Reverse Proxy",
      "AWS IAM: Roles, Policies, Access Keys & Security Best Practices",
      "AWS CloudFront & SSL Certificate (Route 53 + ACM)",
      "CI/CD with GitHub Actions direct to EC2"
    ],
    samplePages: [
      {
        pageNumber: 1,
        title: "AWS S3 Pre-Signed URL Generator Code",
        content: `import { S3Client, GetObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from '@aws-sdk/s3-request-presigner';

const s3 = new S3Client({ region: process.env.AWS_REGION });

export async function getSecureDownloadUrl(s3FileKey) {
  const command = new GetObjectCommand({
    Bucket: process.env.AWS_S3_BUCKET_NAME,
    Key: s3FileKey,
  });

  // URL valid for only 10 minutes (600 seconds)
  return await getSignedUrl(s3, command, { expiresIn: 600 });
}`
      },
      {
        pageNumber: 2,
        title: "Nginx Reverse Proxy Configuration for Node.js",
        content: `server {
    listen 80;
    server_name api.revise-x.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}`
      }
    ]
  },
  {
    id: "java-core-oops-dsa",
    title: "Java Core, OOPs & Collections Cheatsheet",
    category: "Java",
    tag: "Interview Special",
    badgeColor: "#ef4444",
    price: 50,
    originalPrice: 249,
    rating: 4.8,
    reviewsCount: 490,
    downloads: "3.1k+",
    pages: 52,
    format: "Color PDF (High Res)",
    description: "Master OOPs 4 Pillars with real-world examples, JVM Internals (Heap/Stack/Garbage Collection), Java Collections Framework time complexities, and Multithreading.",
    topics: [
      "OOPs 4 Pillars (Encapsulation, Polymorphism, Abstraction, Inheritance)",
      "JVM Memory Model: Heap, Stack, Method Area & Garbage Collectors",
      "Java Collections Framework: ArrayList vs LinkedList, HashMap internals",
      "Multithreading, Synchronization, Volatile vs Atomic, ExecutorService",
      "Java 8 Streams, Lambda expressions & Optional class"
    ],
    samplePages: [
      {
        pageNumber: 1,
        title: "HashMap Internal Working in Java (Bucket Array & Red-Black Tree)",
        content: `// 1. Hash computation: hash = key.hashCode() ^ (hash >>> 16)
// 2. Index computation: index = (n - 1) & hash (where n is bucket length, default 16)
// 3. Collision Resolution: Linked List until threshold = 8, then converts to Red-Black Tree for O(log N) lookup!`
      },
      {
        pageNumber: 2,
        title: "Java 8 Streams Common Interview Snippets",
        content: `// Find frequency of each character in a String
String input = "developer";
Map<Character, Long> freq = input.chars()
    .mapToObj(c -> (char) c)
    .collect(Collectors.groupingBy(Function.identity(), Collectors.counting()));

// Output: {p=1, d=1, r=1, e=3, v=1, l=1, o=1}`
      }
    ]
  },
  {
    id: "mern-super-bundle",
    title: "🔥 All-in-One Complete MERN + AWS Mastery Bundle",
    category: "Bundles",
    tag: "Value Pack (Save 60%)",
    badgeColor: "#a855f7",
    price: 199,
    originalPrice: 499,
    rating: 5.0,
    reviewsCount: 1250,
    downloads: "6.8k+",
    pages: 280,
    format: "7 Color PDFs + Bonus Cheatsheet",
    description: "Includes ALL 6 Guides (HTML/CSS, JavaScript, React, Node.js, MongoDB, AWS) + Bonus System Design & 200+ Top Tech Interview Questions Pack.",
    topics: [
      "Includes all 6 individual study note PDFs (280+ total pages)",
      "Bonus: System Design & Microservices visual guide",
      "Bonus: 200+ HR & Technical Interview Q&A booklet",
      "Lifetime updates whenever new notes or topics are added"
    ],
    samplePages: [
      {
        pageNumber: 1,
        title: "Full MERN Architecture Flow Diagram",
        content: `[React UI / Tailwind / Vite]
         ▲
         │ (Axios / Fetch REST API calls)
         ▼
[Node.js + Express REST Controller]
         │ (Mongoose ODM)
         ▼
[MongoDB Atlas Clusters]
         │
[AWS S3 Private Storage for Media & PDFs]`
      },
      {
        pageNumber: 2,
        title: "System Design: Scaling to 100k Users",
        content: `1. DNS & CDN (CloudFront / Cloudflare) for static assets.
2. Load Balancer (AWS ALB) distributing traffic across EC2 instances.
3. Redis Cache layer for high-frequency database reads.
4. MongoDB Replica Sets for read-scaling and automated failover.`
      }
    ]
  }
];

export const CATEGORIES = [
  "All",
  "Frontend",
  "Backend",
  "Database",
  "Cloud",
  "Java",
  "Bundles"
];

export const TESTIMONIALS = [
  {
    name: "Rahul Sharma",
    role: "Placed at TCS Digital (Package: 7.5 LPA)",
    college: "SRM University",
    text: "The ₹50 JavaScript and React notes saved my life. I revised the entire Event Loop and Hooks lifecycle in 2 hours before my technical round. Cleared it smoothly!",
    avatar: "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?auto=format&fit=crop&w=120&q=80"
  },
  {
    name: "Pooja Patel",
    role: "Frontend Intern @ FinTech Startup",
    college: "VIT Vellore",
    text: "The handwritten-style diagrams in the CSS and MERN notes are unmatched. Most college slides are boring, but Revise-X makes revision crisp and enjoyable.",
    avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=120&q=80"
  },
  {
    name: "Aditya Verma",
    role: "MERN Stack Developer",
    college: "Anna University",
    text: "I bought the ₹199 Super Bundle. The AWS S3 Pre-signed URL notes alone are worth 10x the price. Very practical and directly applicable to production apps.",
    avatar: "https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?auto=format&fit=crop&w=120&q=80"
  }
];

export const FAQS = [
  {
    q: "How will I receive my notes after paying ₹50?",
    a: "Immediately upon successful payment, you get an instant high-speed download button on screen, plus a secure link sent to your email. You can also view them anytime in your account."
  },
  {
    q: "Can I print these notes or read them on my tablet / iPad?",
    a: "Yes! All notes are high-resolution, vector-crisp PDFs formatted perfectly for both mobile screens, tablets (Notability / GoodNotes), and standard A4 printing."
  },
  {
    q: "What payment methods are supported?",
    a: "We support all Indian UPI apps (Google Pay, PhonePe, Paytm, CRED, BHIM), all Debit & Credit Cards, Net Banking, and Wallets via secure Razorpay checkout."
  },
  {
    q: "Are the notes updated for the latest 2026 tech versions?",
    a: "Yes, all notes include modern standards like React 19, Node.js latest LTS, AWS SDK v3, Java 21 LTS features, and modern CSS3 Grid/Subgrid."
  }
];
