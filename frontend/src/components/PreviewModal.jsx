import React, { useState } from 'react';
import { X, ChevronLeft, ChevronRight, Lock, CheckCircle2, ShoppingCart, BookOpen } from 'lucide-react';

/**
 * PreviewModal Component - Interactive 2-Page Sample Viewer
 * 
 * Clean, human-coded modal that allows students to inspect real
 * code snippets and syllabus from the note before purchasing.
 */
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
      setCurrentPageIndex(prev => prev + 1);
    }
  };

  const handlePrevPage = () => {
    if (currentPageIndex > 0) {
      setCurrentPageIndex(prev => prev - 1);
    }
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-container preview-modal" onClick={(e) => e.stopPropagation()}>
        
        {/* Modal Header */}
        <div className="modal-header">
          <div className="modal-title-group">
            <span className="modal-badge">
              Free 2-Page Sample Preview
            </span>
            <h3 className="modal-note-title">{note.title}</h3>
          </div>
          <button onClick={onClose} className="modal-close-btn" aria-label="Close modal">
            <X size={20} />
          </button>
        </div>

        {/* Modal Body: Sample Page Viewer & Sidebar */}
        <div className="preview-body-grid">
          
          {/* Left Column: Sample PDF Sheet */}
          <div className="pdf-canvas-container">
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

            <div className="pdf-page-sheet">
              <div className="pdf-watermark">
                <span>REVISE-X SAMPLE • ₹50 COMPLETE NOTE</span>
              </div>

              <div className="sheet-header">
                <div className="sheet-topic-badge">
                  <BookOpen size={13} />
                  <span>{note.category} • Page {currentPage.pageNumber}</span>
                </div>
                <h4 className="sheet-title">{currentPage.title}</h4>
              </div>

              <div className="sheet-content-box">
                <pre className="sheet-code">
                  <code>{currentPage.content}</code>
                </pre>
              </div>

              {currentPageIndex === samplePages.length - 1 && (
                <div className="sheet-locked-notice">
                  <Lock size={16} className="lock-icon" />
                  <span>
                    Remaining <strong>{note.pages - 2} pages</strong> with detailed diagrams & interview Q&As are unlocked in the full ₹50 PDF!
                  </span>
                </div>
              )}
            </div>
          </div>

          {/* Right Column: Note Syllabus & Direct Cart Action */}
          <div className="preview-sidebar">
            <div className="sidebar-section">
              <h4 className="sidebar-heading">Included in this ₹50 Note:</h4>
              <ul className="sidebar-topics-list">
                {note.topics.map((t, idx) => (
                  <li key={idx}>
                    <CheckCircle2 size={14} className="text-emerald" />
                    <span>{t}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="sidebar-pricing-card">
              <div className="sidebar-price-row">
                <span className="sidebar-price-label">Price:</span>
                <div className="sidebar-price-values">
                  <span className="sidebar-curr-price">₹{note.price}</span>
                  <span className="sidebar-orig-price">₹{note.originalPrice}</span>
                </div>
              </div>

              <button 
                onClick={() => {
                  onAddToCart(note);
                  onClose();
                }}
                className={`btn-primary btn-full-width ${isInCart ? 'btn-in-cart' : ''}`}
              >
                <ShoppingCart size={17} />
                <span>{isInCart ? 'Already In Cart ✓' : 'Add to Cart (₹50)'}</span>
              </button>
            </div>
          </div>

        </div>

      </div>
    </div>
  );
}
