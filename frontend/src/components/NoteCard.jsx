import React from 'react';
import { Eye, ShoppingCart, FileText, Check, Layers, Sparkles } from 'lucide-react';

/**
 * NoteCard Component - Displays a single study guide card in the catalog
 * 
 * Clean, human-coded component showing note details, topics covered,
 * pricing, and action buttons to preview or add to cart.
 */
export default function NoteCard({ note, onPreview, onAddToCart, isInCart }) {
  // Category icon helper
  const getCategoryIcon = (category) => {
    switch (category) {
      case 'Frontend': return '⚡';
      case 'Database': return '🍃';
      case 'Cloud': return '☁️';
      case 'Bundles': return '🔥';
      default: return '📖';
    }
  };

  // Calculate percentage discount
  const discountPercent = Math.round(
    ((note.originalPrice - note.price) / note.originalPrice) * 100
  );

  return (
    <div className={`note-card ${note.category === 'Bundles' ? 'bundle-card' : ''}`}>
      {/* Card Header: Category & Special Tag */}
      <div className="card-header-bar">
        <span className="card-category-tag">
          <span className="cat-icon">{getCategoryIcon(note.category)}</span>
          {note.category}
        </span>
        {note.tag && (
          <span className="card-special-badge">
            {note.tag}
          </span>
        )}
      </div>

      {/* Card Body: Title, Description, Topics */}
      <div className="card-body">
        <h3 className="card-title">{note.title}</h3>
        <p className="card-description">{note.description}</p>

        {/* Note Metadata: Pages and Format */}
        <div className="card-meta-grid">
          <div className="meta-pill">
            <FileText size={14} className="meta-icon" />
            <span>{note.pages} Pages</span>
          </div>
          <div className="meta-pill">
            <Sparkles size={14} className="meta-icon" />
            <span>{note.format}</span>
          </div>
        </div>

        {/* Syllabus / Key Topics Summary */}
        <div className="card-syllabus">
          <div className="syllabus-heading">
            <Layers size={13} />
            <span>Topics Covered:</span>
          </div>
          <ul className="syllabus-list">
            {note.topics.slice(0, 3).map((topic, i) => (
              <li key={i}>
                <Check size={13} className="check-icon" />
                <span>{topic}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Card Footer: Pricing and Action Buttons */}
      <div className="card-footer">
        <div className="price-block">
          <div className="price-main">
            <span className="currency">₹</span>
            <span className="amount">{note.price}</span>
          </div>
          <div className="price-sub">
            <span className="original-price">₹{note.originalPrice}</span>
            <span className="discount-badge">{discountPercent}% OFF</span>
          </div>
        </div>

        <div className="card-actions">
          {/* Preview button */}
          <button 
            onClick={() => onPreview(note)} 
            className="btn-preview"
            title="Preview sample pages"
          >
            <Eye size={16} />
            <span>Preview</span>
          </button>

          {/* Add to Cart button */}
          <button 
            onClick={() => onAddToCart(note)} 
            className={`btn-buy ${isInCart ? 'btn-in-cart' : ''}`}
          >
            <ShoppingCart size={16} />
            <span>{isInCart ? 'In Cart ✓' : 'Buy Note'}</span>
          </button>
        </div>
      </div>
    </div>
  );
}
