import { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import NotesCatalog from './components/NotesCatalog';
import PreviewModal from './components/PreviewModal';
import CartDrawer from './components/CartDrawer';
import CheckoutModal from './components/CheckoutModal';
import FreeCheatsheetModal from './components/FreeCheatsheetModal';
import Testimonials from './components/Testimonials';
import FAQSection from './components/FAQSection';
import Footer from './components/Footer';
import { NOTES_DATA } from './data/notesData';
import './App.css';

function App() {
  const [notes] = useState(NOTES_DATA);
  const [activeCategory, setActiveCategory] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  
  // Cart state persisted in localStorage
  const [cartItems, setCartItems] = useState(() => {
    try {
      const saved = localStorage.getItem('revise_x_cart');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  // Modal states
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [previewNote, setPreviewNote] = useState(null);
  const [isCheckoutOpen, setIsCheckoutOpen] = useState(false);
  const [checkoutTotal, setCheckoutTotal] = useState(0);
  const [checkoutItems, setCheckoutItems] = useState([]);
  const [isFreeModalOpen, setIsFreeModalOpen] = useState(false);
  const [toastMessage, setToastMessage] = useState('');

  // Persist cart to localStorage
  useEffect(() => {
    localStorage.setItem('revise_x_cart', JSON.stringify(cartItems));
  }, [cartItems]);

  const showToast = (msg) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(''), 3000);
  };

  const handleAddToCart = (note) => {
    const exists = cartItems.find((item) => item.id === note.id);
    if (exists) {
      setIsCartOpen(true);
    } else {
      setCartItems((prev) => [...prev, note]);
      showToast(`Added "${note.title}" to cart! 🛒`);
    }
  };

  const handleRemoveFromCart = (noteId) => {
    setCartItems((prev) => prev.filter((item) => item.id !== noteId));
  };

  const handleClearCart = () => {
    setCartItems([]);
  };

  const handleProceedCheckout = (total, items) => {
    setCheckoutTotal(total);
    setCheckoutItems(items);
    setIsCartOpen(false);
    setIsCheckoutOpen(true);
  };

  const handlePaymentSuccess = () => {
    setCartItems([]);
  };

  const handleScrollToCatalog = () => {
    const catalogEl = document.getElementById('notes-catalog');
    if (catalogEl) {
      catalogEl.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handleSelectCategoryFromHero = (category) => {
    setActiveCategory(category);
    handleScrollToCatalog();
  };

  return (
    <div className="app-root">
      {/* Toast Notification Banner */}
      {toastMessage && (
        <div className="toast-notification">
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Main Navbar */}
      <Navbar 
        cartCount={cartItems.length}
        onOpenCart={() => setIsCartOpen(true)}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        onOpenFreeModal={() => setIsFreeModalOpen(true)}
      />

      <main>
        {/* Hero Section */}
        <Hero 
          onExploreClick={handleScrollToCatalog}
          onOpenFreeModal={() => setIsFreeModalOpen(true)}
          onSelectCategory={handleSelectCategoryFromHero}
        />

        {/* Complete Notes Catalog (Categories, ₹50 Cards, Previews) */}
        <NotesCatalog 
          notes={notes}
          activeCategory={activeCategory}
          setActiveCategory={setActiveCategory}
          searchQuery={searchQuery}
          setSearchQuery={setSearchQuery}
          onPreview={(note) => setPreviewNote(note)}
          onAddToCart={handleAddToCart}
          cartItems={cartItems}
        />

        {/* Social Proof & Student Placements */}
        <Testimonials />

        {/* FAQs */}
        <FAQSection />
      </main>

      {/* Footer */}
      <Footer onOpenFreeModal={() => setIsFreeModalOpen(true)} />

      {/* Interactive Sample Preview Modal */}
      {previewNote && (
        <PreviewModal 
          note={previewNote}
          onClose={() => setPreviewNote(null)}
          onAddToCart={handleAddToCart}
          isInCart={cartItems.some(item => item.id === previewNote.id)}
        />
      )}

      {/* Cart Drawer */}
      <CartDrawer 
        isOpen={isCartOpen}
        onClose={() => setIsCartOpen(false)}
        cartItems={cartItems}
        onRemoveItem={handleRemoveFromCart}
        onClearCart={handleClearCart}
        onProceedCheckout={handleProceedCheckout}
      />

      {/* Razorpay Simulation Checkout Modal */}
      <CheckoutModal 
        isOpen={isCheckoutOpen}
        onClose={() => setIsCheckoutOpen(false)}
        totalAmount={checkoutTotal}
        items={checkoutItems}
        onPaymentSuccess={handlePaymentSuccess}
      />

      {/* Free Sample Cheatsheet Modal */}
      <FreeCheatsheetModal 
        isOpen={isFreeModalOpen}
        onClose={() => setIsFreeModalOpen(false)}
      />
    </div>
  );
}

export default App;
