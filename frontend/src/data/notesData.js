export const NOTES_DATA = [
  {
    id: "html-notes",
    title: "HTML5 Complete Notes (Typed Edition)",
    category: "Frontend",
    tag: "Essential",
    badgeColor: "#ea580c",
    price: 50,
    originalPrice: 199,
    pages: 10,
    format: "Typed Digital PDF",
    pdfFileName: "html-notes.pdf",
    description: "Complete keyboard-typed study guide covering HTML5 document structure, semantic tags, tables, forms, character entities, multimedia, and common tag reference.",
    topics: [
      "Document Structure & <!DOCTYPE html> lifecycle",
      "Headings, Paragraphs, Links, Images & Lists",
      "Block vs Inline containers (div vs span)",
      "HTML Tables (thead, tbody, colspan, rowspan)",
      "HTML5 Forms & all input types with validation",
      "Semantic HTML5 (<header>, <nav>, <main>, <article>, <aside>, <footer>)",
      "Character Entities, Multimedia (<audio>, <video>) & Best Practices"
    ],
    samplePages: [
      {
        pageNumber: 1,
        title: "HTML5 Basic Skeleton",
        content: `<!DOCTYPE html>
<html>
  <head>
    <title>Revise-X Study Hub</title>
  </head>
  <body>
    <!-- Visible content rendered in browser -->
    <header><h1>Welcome to Revise-X</h1></header>
  </body>
</html>`
      },
      {
        pageNumber: 2,
        title: "Semantic HTML Elements",
        content: `<header>Website header</header>
<nav>Navigation links</nav>
<main>Main content</main>
<section>Section of content</section>
<article>Independent article</article>
<footer>Footer content</footer>`
      }
    ]
  },
  {
    id: "css-notes",
    title: "CSS3 Complete Notes (Typed Edition)",
    category: "Frontend",
    tag: "Core Styling",
    badgeColor: "#0284c7",
    price: 50,
    originalPrice: 199,
    pages: 7,
    format: "Typed Digital PDF",
    pdfFileName: "css-notes.pdf",
    description: "Complete keyboard-typed notes covering CSS syntax, Selectors, Combinators, Colors (RGB, RGBA, HSL, HSLA), Box Model, Positioning, Flexbox, Grid, and Media Queries.",
    topics: [
      "Introduction to CSS, History (1996) & Three Ways to Add CSS",
      "CSS Syntax, Simple Selectors & Combinators (> + ~)",
      "Colors in CSS (Named, HEX, RGB, RGBA, HSL, HSLA)",
      "CSS Box Model (Content, Padding, Border, Margin, box-sizing)",
      "Display property & Positioning (static, relative, absolute, fixed, sticky)",
      "CSS Flexbox (1D) & CSS Grid (2D) layout architectures",
      "Transitions, Transforms, Keyframe Animations & Media Queries"
    ],
    samplePages: [
      {
        pageNumber: 1,
        title: "CSS Combinators & Box Model Reset",
        content: `*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

div > p { /* Child selector */
  color: #ea580c;
}`
      },
      {
        pageNumber: 2,
        title: "Flexbox & Grid Layouts",
        content: `.flex-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.5rem;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}`
      }
    ]
  },
  {
    id: "mongodb-aggregation",
    title: "MongoDB & Aggregation Pipeline Guide",
    category: "Database",
    tag: "Comprehensive",
    badgeColor: "#15803d",
    price: 50,
    originalPrice: 199,
    pages: 27,
    format: "Digital PDF",
    pdfFileName: "mongodb-notes.pdf",
    description: "Master document schema design, indexing strategies, compound indexes, and multi-stage aggregation pipelines with visual queries.",
    topics: [
      "Document Schema Design (Embedding vs Referencing)",
      "Single-field, Compound & Text Indexes",
      "Aggregation Stages: $match, $group, $project, $lookup",
      "Facet queries, Pagination with $bucket and cursor",
      "Mongoose Middleware, Schema validation & Transactions"
    ],
    samplePages: [
      {
        pageNumber: 1,
        title: "Multi-Stage Aggregation Pipeline",
        content: `db.orders.aggregate([
  { $match: { status: "PAID" } },
  { $unwind: "$items" },
  { $group: {
      _id: "$items.noteId",
      totalRevenue: { $sum: "$items.price" },
      ordersCount: { $sum: 1 }
  }},
  { $sort: { ordersCount: -1 } }
]);`
      }
    ]
  },
  {
    id: "react-architecture",
    title: "React Architecture & State Management",
    category: "Frontend",
    tag: "Modern React",
    badgeColor: "#0284c7",
    price: 50,
    originalPrice: 199,
    pages: 62,
    format: "Digital PDF",
    pdfFileName: "react-notes.pdf",
    description: "Component lifecycle, Hooks (useState, useEffect, useMemo, useCallback), Custom Hooks, Context API, and state architecture patterns.",
    topics: [
      "Component hierarchy, Props & State encapsulation",
      "Hooks lifecycle: useState, useEffect & cleanup rules",
      "useMemo & useCallback performance optimization",
      "Custom hooks design patterns and code reuse",
      "Context API and scalable global state management"
    ],
    samplePages: [
      {
        pageNumber: 1,
        title: "Custom Hook for Local Storage",
        content: `function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    const saved = localStorage.getItem(key);
    return saved ? JSON.parse(saved) : initialValue;
  });

  useEffect(() => {
    localStorage.setItem(key, JSON.stringify(value));
  }, [key, value]);

  return [value, setValue];
}`
      }
    ]
  },
  {
    id: "aws-cloud-core",
    title: "AWS Cloud Core (IAM, S3 & EC2)",
    category: "Cloud",
    tag: "DevOps Ready",
    badgeColor: "#d97706",
    price: 50,
    originalPrice: 249,
    pages: 14,
    format: "Digital PDF",
    pdfFileName: "aws-services-notes.pdf",
    description: "Practical developer guide to AWS IAM policies & roles, S3 bucket security & pre-signed URLs, and EC2 instance deployment architecture.",
    topics: [
      "IAM: Users, Groups, Roles & JSON Policy structure",
      "S3: Bucket Policies, CORS, Pre-signed URLs for downloads",
      "EC2: Security Groups, Key Pairs, User Data scripts",
      "VPC basics: Public vs Private Subnets & Internet Gateways",
      "AWS CLI cheatsheet & Node.js AWS SDK v3 snippets"
    ],
    samplePages: [
      {
        pageNumber: 1,
        title: "IAM Least Privilege Policy",
        content: `{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:GetObject"],
      "Resource": "arn:aws:s3:::revisex-notes/*"
    }
  ]
}`
      }
    ]
  }
];

export const CATEGORIES = [
  "All",
  "Frontend",
  "Database",
  "Cloud"
];

export const FAQS = [
  {
    q: "How will I receive my notes after paying ₹50?",
    a: "Immediately after checkout, you get an instant download link on screen for your high-quality PDF study guide."
  },
  {
    q: "Can I read these notes on mobile, tablet, or print them?",
    a: "Yes. All notes are high-resolution PDFs designed to read clearly on mobile screens, tablets (Notability / GoodNotes), and standard A4 paper."
  },
  {
    q: "What topics are included in these notes?",
    a: "Our notes currently cover HTML5 (Typed Edition), CSS3 (Typed Edition), React Architecture, MongoDB, and AWS Core Services (IAM, S3, EC2)."
  },
  {
    q: "What payment methods are supported?",
    a: "We support UPI (Google Pay, PhonePe, Paytm, CRED), Debit/Credit Cards, and Net Banking."
  }
];
