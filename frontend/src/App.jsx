import { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import NotesCatalog from './components/NotesCatalog';
import PreviewModal from './components/PreviewModal';
import CartDrawer from './components/CartDrawer';
import CheckoutModal from './components/CheckoutModal';
import FreeCheatsheetModal from './components/FreeCheatsheetModal';
import Footer from './components/Footer';
import { NOTES_DATA } from './data/notesData';
import './App.css';

export default function App() {
  const [notes] = useState(NOTES_DATA);
  const [activeCategory, setActiveCategory] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  
  const [cartItems, setCartItems] = useState(() => {
    try {
      const saved = localStorage.getItem('revise_x_cart');
      return saved ? JSON.parse(saved) : [];
    } catch {
      return [];
    }
  });

  const [isCartOpen, setIsCartOpen] = useState(false);
  const [previewNote, setPreviewNote] = useState(null);
  const [isCheckoutOpen, setIsCheckoutOpen] = useState(false);
  const [checkoutTotal, setCheckoutTotal] = useState(0);
  const [checkoutItems, setCheckoutItems] = useState([]);
  const [isFreeModalOpen, setIsFreeModalOpen] = useState(false);
  const [toastMessage, setToastMessage] = useState('');

  useEffect(() => {
    localStorage.setItem('revise_x_cart', JSON.stringify(cartItems));
  }, [cartItems]);

  const showToast = (msg) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(''), 3000);
  };

  const handleAddToCart = (note) => {
    const exists = cartItems.find((item) => item.id === note.id);
    if (!exists) {
      setCartItems((prev) => [...prev, note]);
    }
    // Open cart drawer immediately so user can proceed to pay
    setIsCartOpen(true);
    showToast(`"${note.title}" added to cart! Proceeding to checkout...`);
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

  const handleSelectCategory = (category) => {
    setActiveCategory(category);
    handleScrollToCatalog();
  };

  return (
    <div className="app-root">
      {toastMessage && (
        <div className="toast-notification">
          <span>{toastMessage}</span>
        </div>
      )}

      <Navbar 
        cartCount={cartItems.length}
        onOpenCart={() => setIsCartOpen(true)}
        searchQuery={searchQuery}
        setSearchQuery={setSearchQuery}
        onOpenFreeModal={() => setIsFreeModalOpen(true)}
      />

      <main>
        <Hero 
          onExploreClick={handleScrollToCatalog}
          onOpenFreeModal={() => setIsFreeModalOpen(true)}
          onSelectCategory={handleSelectCategory}
          onPreviewAws={() => {
            const awsNote = notes.find(n => n.id === 'aws-cloud-core');
            if (awsNote) setPreviewNote(awsNote);
          }}
          onAddToCart={handleAddToCart}
          isAwsInCart={cartItems.some(item => item.id === 'aws-cloud-core')}
        />

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
      </main>

      <Footer onOpenFreeModal={() => setIsFreeModalOpen(true)} />

      {previewNote && (
        <PreviewModal 
          note={previewNote}
          onClose={() => setPreviewNote(null)}
          onAddToCart={handleAddToCart}
          isInCart={cartItems.some(item => item.id === previewNote.id)}
        />
      )}

      <CartDrawer 
        isOpen={isCartOpen}
        onClose={() => setIsCartOpen(false)}
        cartItems={cartItems}
        onRemoveItem={handleRemoveFromCart}
        onClearCart={handleClearCart}
        onProceedCheckout={handleProceedCheckout}
      />

      <CheckoutModal 
        isOpen={isCheckoutOpen}
        onClose={() => setIsCheckoutOpen(false)}
        totalAmount={checkoutTotal}
        items={checkoutItems}
        onPaymentSuccess={handlePaymentSuccess}
      />

      <FreeCheatsheetModal 
        isOpen={isFreeModalOpen}
        onClose={() => setIsFreeModalOpen(false)}
      />
    </div>
  );
}