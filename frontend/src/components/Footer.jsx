import React from 'react';
import { Heart } from 'lucide-react';
import { ReviseXLogoMark } from './Logo';

/**
 * Footer Component - Authentic, clean footer for Revise-X
 * 
 * Free of fake guarantees, placeholder policies, or dead links.
 * Focuses on direct navigation and real developer project links.
 */
export default function Footer({ onOpenFreeModal }) {
  return (
    <footer className="footer-section">
      <div className="footer-container">
        <div className="footer-top-grid">
          
          {/* Brand & Project Info */}
          <div className="footer-brand-col">
            <div className="nav-brand">
              <div className="brand-icon-box">
                <ReviseXLogoMark size={28} withTile={false} />
              </div>
              <span className="brand-name">Revise<span className="brand-accent">-X</span></span>
            </div>
            <p className="footer-bio">
              Distilled, visual cheatsheets and revision study notes for developers preparing for technical interviews and exams.
            </p>
            <div className="footer-social-links">
              <a 
                href="https://github.com/DineshKumar-02/REVISE-X-PROJECT" 
                target="_blank" 
                rel="noreferrer" 
                className="social-btn github-btn" 
                title="View on GitHub"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"></path>
                  <path d="M9 18c-4.51 2-5-2-7-2"></path>
                </svg>
                <span>GitHub Repository</span>
              </a>
            </div>
          </div>

          {/* Quick Navigation Links */}
          <div className="footer-links-col">
            <h4>Quick Links</h4>
            <ul>
              <li><a href="#home">Home</a></li>
              <li><a href="#notes-catalog">All Study Notes (₹50)</a></li>
              <li><button onClick={onOpenFreeModal} className="link-btn">Free Sample Cheatsheet</button></li>
            </ul>
          </div>

          {/* Subjects / Notes Covered */}
          <div className="footer-links-col">
            <h4>Study Notes</h4>
            <ul>
              <li><a href="#notes-catalog">HTML5 (Typed Edition)</a></li>
              <li><a href="#notes-catalog">CSS3 (Typed Edition)</a></li>
              <li><a href="#notes-catalog">React Architecture</a></li>
              <li><a href="#notes-catalog">MongoDB & Aggregation</a></li>
              <li><a href="#notes-catalog">AWS Cloud Core (EC2, S3, IAM)</a></li>
            </ul>
          </div>

        </div>

        {/* Bottom Bar: Copyright & Attribution */}
        <div className="footer-bottom-bar">
          <p>© {new Date().getFullYear()} Revise-X • Built by Dinesh Kumar S with <Heart size={14} className="heart-icon" /> for tech students.</p>
        </div>
      </div>
    </footer>
  );
}
