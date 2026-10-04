import React, { useState, useMemo } from 'react';
import NoteCard from './NoteCard';
import { CATEGORIES } from '../data/notesData';
import { SlidersHorizontal, BookOpen } from 'lucide-react';

/**
 * NotesCatalog Component - Filterable, searchable grid of revision guides
 * 
 * Human-coded, beginner-friendly component with:
 * - Category filter tabs
 * - Search query filtering
 * - Sorting by price, featured, or page count
 */
export default function NotesCatalog({ 
  notes, 
  activeCategory, 
  setActiveCategory, 
  searchQuery, 
  setSearchQuery,
  onPreview, 
  onAddToCart, 
  cartItems 
}) {
  const [sortBy, setSortBy] = useState('featured');

  // Filter notes based on active category and search query
  const filteredNotes = useMemo(() => {
    let result = notes.filter((note) => {
      const matchesCategory = activeCategory === 'All' || note.category === activeCategory;
      const query = searchQuery.toLowerCase().trim();
      const matchesSearch = !query || 
        note.title.toLowerCase().includes(query) ||
        note.description.toLowerCase().includes(query) ||
        note.topics.some(t => t.toLowerCase().includes(query));
      return matchesCategory && matchesSearch;
    });

    // Apply sorting
    if (sortBy === 'price-low') {
      result.sort((a, b) => a.price - b.price);
    } else if (sortBy === 'price-high') {
      result.sort((a, b) => b.price - a.price);
    } else if (sortBy === 'pages') {
      result.sort((a, b) => b.pages - a.pages);
    }

    return result;
  }, [notes, activeCategory, searchQuery, sortBy]);

  return (
    <section id="notes-catalog" className="catalog-section">
      <div className="catalog-container">
        
        {/* Section Heading */}
        <div className="section-header-center">
          <div className="section-pill">
            <BookOpen size={14} />
            <span>Developer Revision Library</span>
          </div>
          <h2 className="section-title">
            Explore Handcrafted <span className="text-gradient">Study Notes & Cheatsheets</span>
          </h2>
          <p className="section-subtitle">
            Every guide is distilled into visual flowcharts, code syntax, and core concepts. Micro-priced at ₹50 for quick revision.
          </p>
        </div>

        {/* Catalog Toolbar: Category Pills & Sort Dropdown */}
        <div className="catalog-toolbar">
          <div className="category-pills-list">
            {CATEGORIES.map((cat) => {
              const count = cat === 'All' 
                ? notes.length 
                : notes.filter(n => n.category === cat).length;

              return (
                <button
                  key={cat}
                  onClick={() => setActiveCategory(cat)}
                  className={`category-pill ${activeCategory === cat ? 'active' : ''}`}
                >
                  <span>{cat}</span>
                  <span className="pill-count">{count}</span>
                </button>
              );
            })}
          </div>

          <div className="sort-controls">
            <SlidersHorizontal size={16} className="sort-icon" />
            <span className="sort-label">Sort by:</span>
            <select 
              value={sortBy} 
              onChange={(e) => setSortBy(e.target.value)}
              className="sort-dropdown"
            >
              <option value="featured">⚡ Featured</option>
              <option value="price-low">💰 Price: Low to High</option>
              <option value="price-high">💎 Price: High to Low</option>
              <option value="pages">📄 Page Count</option>
            </select>
          </div>
        </div>

        {/* Active Filter Indicator */}
        {(activeCategory !== 'All' || searchQuery) && (
          <div className="active-filter-bar">
            <span>
              Showing results for: 
              {activeCategory !== 'All' && <strong> Category: {activeCategory}</strong>}
              {searchQuery && <strong> Search: "{searchQuery}"</strong>}
            </span>
            <button 
              onClick={() => { setActiveCategory('All'); setSearchQuery(''); }}
              className="btn-clear-filters"
            >
              Reset Filters ✕
            </button>
          </div>
        )}

        {/* Notes Grid Display */}
        {filteredNotes.length > 0 ? (
          <div className="notes-grid">
            {filteredNotes.map((note) => {
              const isInCart = cartItems.some((item) => item.id === note.id);
              return (
                <NoteCard 
                  key={note.id}
                  note={note}
                  onPreview={onPreview}
                  onAddToCart={onAddToCart}
                  isInCart={isInCart}
                />
              );
            })}
          </div>
        ) : (
          <div className="catalog-empty-state">
            <p>No notes found matching your search. Try another query or reset filters.</p>
            <button 
              onClick={() => { setActiveCategory('All'); setSearchQuery(''); }}
              className="btn-primary"
            >
              Show All Notes
            </button>
          </div>
        )}
      </div>
    </section>
  );
}
