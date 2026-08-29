import React from 'react';
import { Sparkles, Download, CheckCircle2, ArrowRight, ShieldCheck, Zap } from 'lucide-react';

export default function Hero({ onExploreClick, onOpenFreeModal, onSelectCategory }) {
  const quickTags = [
    { label: "React 19 Hooks", cat: "Frontend" },
    { label: "AWS S3 & EC2", cat: "Cloud" },
    { label: "Node & Express", cat: "Backend" },
    { label: "Java Collections", cat: "Java" },
    { label: "MongoDB Pipeline", cat: "Database" },
  ];

  return (
    <section id="home" className="hero-section">
      <div className="hero-container">
        {/* Left Side: Copywriting & CTAs */}
        <div className="hero-content">
          <div className="hero-pill-badge">
            <span className="pill-dot"></span>
            <Sparkles size={14} className="pill-icon" />
            <span>High-Yield Revision Notes for Indian Students & Devs</span>
          </div>

          <h1 className="hero-title">
            Revise Fast. Crack Interviews. <br />
            <span className="hero-gradient-text">All Tech Notes at just ₹50.</span>
          </h1>

          <p className="hero-description">
            Cut through 500-page textbooks and 40-hour video tutorials. Get handcrafted visual cheatsheets, real code snippets, and interview questions for <strong>HTML, CSS, JS, React, Node, Express, MongoDB, AWS & Java</strong>.
          </p>

          {/* Value Props Grid */}
          <div className="hero-props">
            <div className="prop-item">
              <CheckCircle2 size={16} className="prop-icon" />
              <span>Instant High-Res PDF</span>
            </div>
            <div className="prop-item">
              <CheckCircle2 size={16} className="prop-icon" />
              <span>Visual Architecture Diagrams</span>
            </div>
            <div className="prop-item">
              <CheckCircle2 size={16} className="prop-icon" />
              <span>Lifetime Access & Updates</span>
            </div>
          </div>

          {/* Action Buttons */}
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

          {/* Quick Search Chips */}
          <div className="hero-quick-tags">
            <span className="tags-label">Popular Topics:</span>
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

        {/* Right Side: Interactive Visual Card Preview */}
        <div className="hero-preview-wrapper">
          <div className="hero-card-glow"></div>
          <div className="hero-preview-card">
            <div className="card-top-bar">
              <div className="window-dots">
                <span className="dot red"></span>
                <span className="dot yellow"></span>
                <span className="dot green"></span>
              </div>
              <span className="preview-label">React 19 & Hooks • Cheatsheet Page #1</span>
              <span className="price-tag-pill">₹50 ONLY</span>
            </div>

            <div className="code-card-body">
              <div className="code-line comment">// 🔥 React 19 State Management & Action Hooks</div>
              <div className="code-line">
                <span className="kw">const</span> [state, formAction, isPending] = <span className="fn">useActionState</span>(async (prev, formData) =&gt; &#123;
              </div>
              <div className="code-line indent">
                <span className="kw">const</span> res = <span className="kw">await</span> <span className="fn">verifyPayment</span>(formData.<span className="fn">get</span>(<span className="str">'orderId'</span>));
              </div>
              <div className="code-line indent">
                <span className="kw">return</span> res.data; <span className="comment">// ⚡ Instant optimistic UI</span>
              </div>
              <div className="code-line">&#125;, null);</div>

              <div className="preview-mini-diagram">
                <div className="diagram-node node-a">Student Action</div>
                <div className="diagram-arrow">➔</div>
                <div className="diagram-node node-b">Optimistic UI</div>
                <div className="diagram-arrow">➔</div>
                <div className="diagram-node node-c">Server Sync</div>
              </div>
            </div>

            <div className="card-footer-info">
              <div className="student-stats">
                <div className="avatar-group">
                  <span className="avatar">👨‍💻</span>
                  <span className="avatar">👩‍🎓</span>
                  <span className="avatar">🧑‍💻</span>
                </div>
                <span className="stats-text"><strong>3,800+</strong> students purchased</span>
              </div>
              <div className="guarantee-badge">
                <ShieldCheck size={16} /> 100% Student Verified
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
