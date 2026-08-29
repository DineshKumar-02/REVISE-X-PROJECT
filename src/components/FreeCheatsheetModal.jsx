import React, { useState } from 'react';
import { X, Download, CheckCircle2, Sparkles, BookOpen } from 'lucide-react';

export default function FreeCheatsheetModal({ isOpen, onClose }) {
  const [email, setEmail] = useState('');
  const [downloaded, setDownloaded] = useState(false);

  if (!isOpen) return null;

  const handleDownload = (e) => {
    e.preventDefault();
    if (!email) return;
    setDownloaded(true);
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-container free-sample-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title-group">
            <span className="modal-badge free-badge">
              <Sparkles size={14} /> 100% Free Developer Resource
            </span>
            <h3 className="modal-note-title">Top 50 Frontend & MERN Interview Cheatsheet</h3>
          </div>
          <button onClick={onClose} className="modal-close-btn">
            <X size={20} />
          </button>
        </div>

        {!downloaded ? (
          <div className="free-modal-body">
            <p className="free-desc">
              Get an instant 15-page sample cheatsheet covering the <strong>Top 50 Most Asked Frontend & Full Stack Interview Questions</strong> (Event loop, React Hooks rules, Flexbox vs Grid matrix, and REST conventions).
            </p>

            <ul className="free-features-list">
              <li><CheckCircle2 size={16} className="text-emerald" /> 15 High-Resolution Vector Pages</li>
              <li><CheckCircle2 size={16} className="text-emerald" /> Quick syntax refresher for quick 1-day revision</li>
              <li><CheckCircle2 size={16} className="text-emerald" /> Instant PDF download, no credit card required</li>
            </ul>

            <form onSubmit={handleDownload} className="free-download-form">
              <input 
                type="email" 
                placeholder="Enter your student email..."
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="form-input"
              />
              <button type="submit" className="btn-primary btn-full-width">
                <Download size={18} />
                <span>Download Free Sample PDF (15 Pages)</span>
              </button>
            </form>
          </div>
        ) : (
          <div className="free-modal-success">
            <div className="success-icon-box">
              <CheckCircle2 size={48} className="success-icon" />
            </div>
            <h4>Download Ready! 🚀</h4>
            <p>Your free 15-page cheatsheet is ready. Check your downloads folder or click below:</p>
            <button 
              onClick={() => alert('📥 Downloading Free 15-Page Sample Cheatsheet.pdf!')}
              className="btn-primary"
            >
              <Download size={18} />
              <span>Download PDF File Again</span>
            </button>
            <button onClick={onClose} className="btn-secondary" style={{ marginTop: '12px' }}>
              Explore ₹50 Full Notes
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
