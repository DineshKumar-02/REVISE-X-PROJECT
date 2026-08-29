import React, { useState } from 'react';
import { X, ChevronLeft, ChevronRight, Lock, CheckCircle2, ShoppingCart, Sparkles, BookOpen } from 'lucide-react';

export default function PreviewModal({ note, onClose, onAddToCart, isInCart }) {
  const [currentPageIndex, setCurrentPageIndex] = useState(0);

  if (!note) return null;

  const samplePages = note.samplePages || [];
  const currentPage = samplePages[currentPageIndex] || {
    pageNumber: 1,
    title: "Overview Sample",
    content: "Sample content not available."
  };

  const handleNextPage = () => {
    if (currentPageIndex < samplePages.length - 1) {
      setCurrentPageIndex(currentPageIndex + 1);
    }
  };

  const handlePrevPage = () => {
    if (currentPageIndex > 0) {
      setCurrentPageIndex(currentPageIndex - 1);
    }
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-container preview-modal" onClick={(e) => e.stopPropagation()}>
        {/* Modal Top Navigation */}
        <div className="modal-header">
          <div className="modal-title-group">
            <span className="modal-badge" style={{ backgroundColor: `${note.badgeColor}22`, color: note.badgeColor }}>
              Free 2-Page Sample Preview
            </span>
            <h3 className="modal-note-title">{note.title}</h3>
          </div>
          <button onClick={onClose} className="modal-close-btn" aria-label="Close modal">
            <X size={20} />
          </button>
        </div>

        {/* Modal Main Layout: PDF Viewer on Left, Info on Right */}
        <div className="preview-body-grid">
          {/* Simulated PDF Document Canvas */}
          <div className="pdf-canvas-container">
            {/* PDF Toolbar */}
            <div className="pdf-toolbar">
              <div className="pdf-page-indicator">
                <span>Sample Page {currentPageIndex + 1} of {samplePages.length}</span>
                <span className="total-pages-hint">({note.pages} pages in full note)</span>
              </div>
              <div className="pdf-page-nav-btns">
                <button 
                  onClick={handlePrevPage} 
                  disabled={currentPageIndex === 0}
                  className="pdf-nav-btn"
                  title="Previous Page"
                >
                  <ChevronLeft size={18} />
                </button>
                <button 
                  onClick={handleNextPage} 
                  disabled={currentPageIndex === samplePages.length - 1}
                  className="pdf-nav-btn"
                  title="Next Page"
                >
                  <ChevronRight size={18} />
                </button>
              </div>
            </div>

            {/* Simulated Page Sheet */}
            <div className="pdf-page-sheet">
              {/* Security Watermark */}
              <div className="pdf-watermark">
                <span>REVISE-X SAMPLE • ₹50 COMPLETE NOTE</span>
              </div>

              {/* Page Header */}
              <div className="sheet-header">
                <div className="sheet-topic-badge">
                  <BookOpen size={13} />
                  <span>{note.category} Mastery • Page {currentPage.pageNumber}</span>
                </div>
                <h4 className="sheet-title">{currentPage.title}</h4>
              </div>

              {/* Page Content Code / Diagrams */}
              <div className="sheet-content-box">
                <pre className="sheet-code">
                  <code>{currentPage.content}</code>
                </pre>
              </div>

              {/* Next Page Locked Teaser if at last sample page */}
              {currentPageIndex === samplePages.length - 1 && (
                <div className="sheet-locked-notice">
                  <Lock size={16} className="lock-icon" />
                  <span>Remaining <strong>{note.pages - 2} pages</strong> with complete interview questions are unlocked in the full ₹50 PDF!</span>
                </div>
              )}
            </div>
          </div>

          {/* Right Sidebar: Syllabus & Buy Action */}
          <div className="preview-sidebar">
            <div className="sidebar-section">
              <h4 className="sidebar-heading">Included in this ₹50 Note:</h4>
              <ul className="sidebar-topics-list">
                {note.topics.map((topic, i) => (
                  <li key={i}>
                    <CheckCircle2 size={14} className="topic-check" />
                    <span>{topic}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="sidebar-specs-card">
              <div className="spec-row">
                <span className="spec-label">Format:</span>
                <span className="spec-val">High-Res Vector PDF</span>
              </div>
              <div className="spec-row">
                <span className="spec-label">Total Pages:</span>
                <span className="spec-val">{note.pages} Pages</span>
              </div>
              <div className="spec-row">
                <span className="spec-label">Delivery:</span>
                <span className="spec-val">Instant Download</span>
              </div>
              <div className="spec-row">
                <span className="spec-label">License:</span>
                <span className="spec-val">Personal Lifetime Access</span>
              </div>
            </div>

            {/* Buy CTA */}
            <div className="sidebar-cta-box">
              <div className="sidebar-price-row">
                <div className="sidebar-price">
                  <span className="currency">₹</span>
                  <span className="amount">{note.price}</span>
                  <span className="original">₹{note.originalPrice}</span>
                </div>
                <span className="discount-tag">Save ₹{note.originalPrice - note.price}</span>
              </div>

              <button 
                onClick={() => {
                  onAddToCart(note);
                  onClose();
                }}
                className={`btn-primary btn-full-width ${isInCart ? 'btn-in-cart' : ''}`}
              >
                <ShoppingCart size={18} />
                <span>{isInCart ? 'View in Cart' : `Unlock Full PDF for ₹${note.price}`}</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
