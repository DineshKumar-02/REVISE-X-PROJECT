import React from 'react';
import { ShoppingCart, Search } from 'lucide-react';
import { ReviseXLogoMark } from './Logo';

/**
 * Navbar Component - Sticky navigation header for Revise-X
 * 
 * Clean, human-coded navigation bar featuring:
 * - Brand logo with link to home
 * - Live instant search input
 * - Links to notes catalog, free sample, and FAQs
 * - Interactive cart button with active items counter
 */
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
        
        {/* Brand Logo & Name */}
        <a href="#home" className="nav-brand" aria-label="Revise-X Home">
          <div className="brand-icon-box">
            <ReviseXLogoMark size={28} />
          </div>
          <div className="brand-text-group">
            <span className="brand-name">Revise<span className="brand-accent">-X</span></span>
            <span className="brand-badge">₹50 Notes Hub</span>
          </div>
        </a>

        {/* Live Search Input */}
        <div className="nav-search-wrapper">
          <Search className="search-icon" size={17} />
          <input 
            type="text" 
            placeholder="Search notes (e.g. React, AWS, MongoDB)..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="nav-search-input"
          />
          {searchQuery && (
            <button 
              className="search-clear-btn"
              onClick={() => setSearchQuery('')}
              aria-label="Clear search"
            >
              ✕
            </button>
          )}
        </div>

        {/* Navigation Action Links */}
        <nav className="nav-actions">
          <a href="#notes-catalog" className="nav-link">Study Notes</a>
          <button onClick={onOpenFreeModal} className="nav-link free-sample-btn">
            Free Sample
          </button>

          {/* Cart Button */}
          <button 
            onClick={onOpenCart}
            className="nav-cart-btn"
            aria-label="View Cart"
          >
            <ShoppingCart size={19} />
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
