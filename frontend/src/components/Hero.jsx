import React from 'react';
import { Sparkles, Download, CheckCircle2, ArrowRight, Zap, Info } from 'lucide-react';

/**
 * Hero Component - Welcome banner for Revise-X
 * 
 * Clean, human-coded component introducing the platform:
 * - Left side: Title, value propositions, call-to-action buttons, subject tags
 * - Right side: AWS PDF study guide diagram showcase with reference caption
 */
export default function Hero({ 
  onExploreClick, 
  onOpenFreeModal, 
  onSelectCategory 
}) {
  // Quick subject tags for one-click catalog filtering
  const quickTags = [
    { label: "HTML5", cat: "Frontend" },
    { label: "CSS3", cat: "Frontend" },
    { label: "React", cat: "Frontend" },
    { label: "MongoDB", cat: "Database" },
    { label: "AWS Core", cat: "Cloud" }
  ];

  return (
    <section id="home" className="hero-section">
      <div className="hero-container">
        
        {/* Left Column: Headline and Call-to-Actions */}
        <div className="hero-content">
          <div className="hero-pill-badge">
            <Sparkles size={14} className="pill-icon" />
            <span>Developer Study Guides & Cheatsheets</span>
          </div>

          <h1 className="hero-title">
            Revise Fast. Crack Interviews. <br />
            <span className="hero-gradient-text">All Tech Notes at just ₹50.</span>
          </h1>

          <p className="hero-description">
            Cut through 600-page textbooks and 40-hour video playlists. Get distilled, 
            high-resolution study notes covering <strong>HTML5, CSS3, React, MongoDB, and AWS Cloud</strong>.
          </p>

          {/* Quick value propositions */}
          <div className="hero-props">
            <div className="prop-item">
              <CheckCircle2 size={16} className="prop-icon" />
              <span>Instant Vector PDF Downloads</span>
            </div>
            <div className="prop-item">
              <CheckCircle2 size={16} className="prop-icon" />
              <span>Visual Architecture Diagrams</span>
            </div>
            <div className="prop-item">
              <CheckCircle2 size={16} className="prop-icon" />
              <span>Lifetime Offline Access</span>
            </div>
          </div>

          {/* Primary Action Buttons */}
          <div className="hero-actions">
            <button onClick={onExploreClick} className="btn-primary">
              <Zap size={18} />
              <span>Explore All Notes (₹50)</span>
              <ArrowRight size={18} className="btn-arrow" />
            </button>

            <button onClick={onOpenFreeModal} className="btn-secondary">
              <Download size={18} />
              <span>Free Sample Cheatsheet</span>
            </button>
          </div>

          {/* Quick Subject Chips */}
          <div className="hero-quick-tags">
            <span className="tags-label">Quick Subjects:</span>
            {quickTags.map((tag) => (
              <button 
                key={tag.label}
                onClick={() => onSelectCategory(tag.cat)}
                className="tag-chip"
              >
                #{tag.label}
              </button>
            ))}
          </div>
        </div>

        {/* Right Column: AWS Diagram Image Showcase & Reference */}
        <div className="hero-preview-wrapper">
          <div className="aws-showcase-card">
            
            {/* Diagram Image Alone */}
            <div className="aws-image-frame">
              <img 
                src="/images/aws-preview-ec2.png" 
                alt="AWS EC2 Virtual Server Architecture Diagram"
                className="aws-showcase-img"
              />
            </div>

            {/* Reference Caption under Image */}
            <div className="aws-image-reference">
              <Info size={16} className="ref-icon" />
              <span>
                <strong>Ref:</strong> AWS Cloud Core Notes — EC2 Virtual Server Architecture Diagram (Page 7)
              </span>
            </div>

          </div>
        </div>

      </div>
    </section>
  );
}
