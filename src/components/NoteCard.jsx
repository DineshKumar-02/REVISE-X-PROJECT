import React from 'react';
import { Eye, ShoppingCart, Star, FileText, Check, Download, Layers } from 'lucide-react';

export default function NoteCard({ note, onPreview, onAddToCart, isInCart }) {
  // Select icon background based on category
  const getCategoryIcon = (category) => {
    switch (category) {
      case 'Frontend': return '⚡';
      case 'Backend': return '🚀';
      case 'Database': return '🍃';
      case 'Cloud': return '☁️';
      case 'Java': return '☕';
      case 'Bundles': return '🔥';
      default: return '📖';
    }
  };

  const discountPercent = Math.round(((note.originalPrice - note.price) / note.originalPrice) * 100);

  return (
    <div className={`note-card ${note.category === 'Bundles' ? 'bundle-highlight-card' : ''}`}>
      {/* Top Banner Tag */}
      <div className="card-header-bar">
        <span className="card-category-tag" style={{ borderColor: note.badgeColor, color: note.badgeColor }}>
          <span className="cat-icon">{getCategoryIcon(note.category)}</span>
          {note.category}
        </span>
        {note.tag && (
          <span className="card-special-badge" style={{ backgroundColor: `${note.badgeColor}22`, color: note.badgeColor, borderColor: `${note.badgeColor}55` }}>
            {note.tag}
          </span>
        )}
      </div>

      {/* Title & Description */}
      <div className="card-body">
        <h3 className="card-title">{note.title}</h3>
        <p className="card-description">{note.description}</p>

        {/* Note Metadata (Pages, Rating, Downloads) */}
        <div className="card-meta-grid">
          <div className="meta-pill">
            <FileText size={14} className="meta-icon" />
            <span>{note.pages} Pages</span>
          </div>
          <div className="meta-pill">
            <Star size={14} className="meta-icon star-filled" />
            <span>{note.rating} ({note.reviewsCount})</span>
          </div>
          <div className="meta-pill">
            <Download size={14} className="meta-icon" />
            <span>{note.downloads}</span>
          </div>
        </div>

        {/* Syllabus / Key Highlights */}
        <div className="card-syllabus">
          <div className="syllabus-heading">
            <Layers size={13} />
            <span>What's inside:</span>
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

      {/* Pricing & Call to Actions */}
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
          {/* Preview Button */}
          <button 
            onClick={() => onPreview(note)} 
            className="btn-preview"
            title="Preview 2 sample pages"
          >
            <Eye size={16} />
            <span>Preview</span>
          </button>

          {/* Add to Cart / Buy Button */}
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
