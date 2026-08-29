import React, { useState, useMemo } from 'react';
import NoteCard from './NoteCard';
import { CATEGORIES } from '../data/notesData';
import { Filter, SlidersHorizontal, Sparkles, BookOpen } from 'lucide-react';

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
  const [sortBy, setSortBy] = useState('popular');

  // Filter and Sort logic
  const filteredNotes = useMemo(() => {
    let result = notes.filter((note) => {
      const matchesCategory = activeCategory === 'All' || note.category === activeCategory;
      const matchesSearch = 
        note.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        note.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
        note.topics.some(t => t.toLowerCase().includes(searchQuery.toLowerCase()));
      return matchesCategory && matchesSearch;
    });

    // Sorting
    if (sortBy === 'price-low') {
      result.sort((a, b) => a.price - b.price);
    } else if (sortBy === 'price-high') {
      result.sort((a, b) => b.price - a.price);
    } else if (sortBy === 'rating') {
      result.sort((a, b) => b.rating - a.rating);
    } else if (sortBy === 'pages') {
      result.sort((a, b) => b.pages - a.pages);
    }

    return result;
  }, [notes, activeCategory, searchQuery, sortBy]);

  return (
    <section id="notes-catalog" className="catalog-section">
      <div className="catalog-container">
        {/* Section Header */}
        <div className="section-header-center">
          <div className="section-pill">
            <BookOpen size={14} />
            <span>Complete Revision Library</span>
          </div>
          <h2 className="section-title">
            Explore Handcrafted <span className="text-gradient">Study Notes & Cheatsheets</span>
          </h2>
          <p className="section-subtitle">
            Every guide is distilled into visual flowcharts, interview-frequently-asked concepts, and zero fluff. Micro-priced at ₹50 for every developer.
          </p>
        </div>

        {/* Filter Toolbar (Category Tabs + Sort Dropdown) */}
        <div className="catalog-toolbar">
          {/* Category Pills */}
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

          {/* Sort Selector */}
          <div className="sort-controls">
            <SlidersHorizontal size={16} className="sort-icon" />
            <span className="sort-label">Sort by:</span>
            <select 
              value={sortBy} 
              onChange={(e) => setSortBy(e.target.value)}
              className="sort-dropdown"
            >
              <option value="popular">🔥 Most Popular</option>
              <option value="rating">⭐ Highest Rated</option>
              <option value="price-low">💰 Price: Low to High</option>
              <option value="pages">📄 Most Pages</option>
            </select>
          </div>
        </div>

        {/* Active Filter Indicators */}
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

        {/* Notes Grid */}
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
          <div className="no-results-box">
            <div className="no-results-icon">🔍</div>
            <h3>No notes found matching your criteria</h3>
            <p>Try searching for a different keyword like "React", "AWS", "Java", or "MongoDB".</p>
            <button 
              onClick={() => { setActiveCategory('All'); setSearchQuery(''); }}
              className="btn-primary"
            >
              View All Notes
            </button>
          </div>
        )}
      </div>
    </section>
  );
}
