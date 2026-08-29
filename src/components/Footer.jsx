import React from 'react';
import { BookOpen, ShieldCheck, Heart, Globe, Share2, Code2 } from 'lucide-react';

export default function Footer({ onOpenFreeModal }) {
  return (
    <footer className="footer-section">
      <div className="footer-container">
        <div className="footer-top-grid">
          {/* Brand Col */}
          <div className="footer-brand-col">
            <div className="nav-brand">
              <div className="brand-icon-box">
                <BookOpen className="brand-icon" size={20} />
              </div>
              <span className="brand-name">Revise<span className="brand-accent">-X</span></span>
            </div>
            <p className="footer-bio">
              High-yield, visual cheatsheets and revision guides for developers and students preparing for technical interviews and university exams.
            </p>
            <div className="footer-social-links">
              <a href="https://github.com/DineshKumar-02/REVISE-X-PROJECT" target="_blank" rel="noreferrer" className="social-btn" title="GitHub">
                <Code2 size={18} />
              </a>
              <a href="https://linkedin.com" target="_blank" rel="noreferrer" className="social-btn" title="LinkedIn">
                <Share2 size={18} />
              </a>
              <a href="https://revise-x.com" target="_blank" rel="noreferrer" className="social-btn" title="Website">
                <Globe size={18} />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div className="footer-links-col">
            <h4>Quick Links</h4>
            <ul>
              <li><a href="#home">Home</a></li>
              <li><a href="#notes-catalog">All ₹50 Notes</a></li>
              <li><a href="#notes-catalog">MERN & AWS Bundles</a></li>
              <li><button onClick={onOpenFreeModal} className="link-btn">Free 15-Page Sample</button></li>
              <li><a href="#faqs">Frequently Asked Questions</a></li>
            </ul>
          </div>

          {/* Categories */}
          <div className="footer-links-col">
            <h4>Topics Covered</h4>
            <ul>
              <li><a href="#notes-catalog">HTML5 & Modern CSS3</a></li>
              <li><a href="#notes-catalog">JavaScript (ES6+ & Async)</a></li>
              <li><a href="#notes-catalog">React 19 & Hooks</a></li>
              <li><a href="#notes-catalog">Node.js & Express Architecture</a></li>
              <li><a href="#notes-catalog">MongoDB & Aggregation</a></li>
              <li><a href="#notes-catalog">AWS (S3, EC2, IAM)</a></li>
              <li><a href="#notes-catalog">Java Core & Collections</a></li>
            </ul>
          </div>

          {/* Trust & Guarantee */}
          <div className="footer-trust-col">
            <h4>Student Guarantee</h4>
            <div className="trust-card">
              <ShieldCheck size={24} className="text-emerald" />
              <div>
                <h5>100% Satisfaction Guarantee</h5>
                <p>If you don't find these notes helpful for your revision, contact us within 24 hours for a full refund.</p>
              </div>
            </div>
            <div className="price-reminder-pill">
              <span>⚡ Every Single Note is just <strong>₹50</strong></span>
            </div>
          </div>
        </div>

        <div className="footer-bottom-bar">
          <p>© {new Date().getFullYear()} Revise-X. Handcrafted with <Heart size={14} className="heart-icon" /> for Indian Tech Students & Developers.</p>
          <div className="footer-policy-links">
            <a href="#">Privacy Policy</a>
            <span>•</span>
            <a href="#">Terms of Service</a>
            <span>•</span>
            <a href="#">Refund Policy</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
