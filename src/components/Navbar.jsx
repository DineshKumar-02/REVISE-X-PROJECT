import React from 'react';
import { BookOpen, ShoppingCart, Sparkles, Search } from 'lucide-react';

export default function Navbar({ 
  cartCount, 
  onOpenCart, 
  searchQuery, 
  setSearchQuery,
  onOpenFreeModal
}) {
  return (
    <header className="navbar">
      <div className="nav-container">
        {/* Brand Logo */}
        <a href="#home" className="nav-brand">
          <div className="brand-icon-box">
            <BookOpen className="brand-icon" size={22} />
          </div>
          <div className="brand-text-group">
            <span className="brand-name">Revise<span className="brand-accent">-X</span></span>
            <span className="brand-badge">₹50 Notes Hub</span>
          </div>
        </a>

        {/* Global Live Search */}
        <div className="nav-search-wrapper">
          <Search className="search-icon" size={18} />
          <input 
            type="text" 
            placeholder="Search notes (e.g. React, AWS S3, Java, MongoDB)..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="nav-search-input"
          />
          {searchQuery && (
            <button 
              className="search-clear-btn"
              onClick={() => setSearchQuery('')}
            >
              ✕
            </button>
          )}
        </div>

        {/* Navigation Links & Actions */}
        <nav className="nav-actions">
          <a href="#notes-catalog" className="nav-link">Notes</a>
          <a href="#bundles" className="nav-link highlight-pill">
            <Sparkles size={14} className="sparkle-icon" /> Bundles (Save 60%)
          </a>
          <button onClick={onOpenFreeModal} className="nav-link free-sample-btn">
            Free Sample
          </button>
          <a href="#faqs" className="nav-link hide-mobile">FAQ</a>

          {/* Cart Trigger */}
          <button 
            onClick={onOpenCart}
            className="nav-cart-btn"
            aria-label="View Cart"
          >
            <ShoppingCart size={20} />
            <span className="cart-btn-label">Cart</span>
            {cartCount > 0 && (
              <span className="cart-badge-counter">{cartCount}</span>
            )}
          </button>
        </nav>
      </div>
    </header>
  );
}
