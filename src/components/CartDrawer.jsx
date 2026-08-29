import React, { useState } from 'react';
import { X, Trash2, ShoppingBag, ArrowRight, ShieldCheck, Tag, Check, Zap } from 'lucide-react';

export default function CartDrawer({ 
  isOpen, 
  onClose, 
  cartItems, 
  onRemoveItem, 
  onClearCart, 
  onProceedCheckout 
}) {
  const [couponCode, setCouponCode] = useState('');
  const [appliedDiscount, setAppliedDiscount] = useState(0);
  const [couponError, setCouponError] = useState('');
  const [couponSuccess, setCouponSuccess] = useState('');

  if (!isOpen) return null;

  const subtotal = cartItems.reduce((acc, item) => acc + item.price, 0);
  const originalSubtotal = cartItems.reduce((acc, item) => acc + item.originalPrice, 0);
  const couponSavings = Math.round(subtotal * (appliedDiscount / 100));
  const finalTotal = Math.max(0, subtotal - couponSavings);

  const handleApplyCoupon = (e) => {
    e.preventDefault();
    setCouponError('');
    setCouponSuccess('');

    const cleanCode = couponCode.trim().toUpperCase();
    if (cleanCode === 'REVISE20' || cleanCode === 'STUDENT20') {
      setAppliedDiscount(20);
      setCouponSuccess('20% Student Discount Applied! 🎉');
    } else if (cleanCode === 'FREEFIRST') {
      setAppliedDiscount(50);
      setCouponSuccess('Special 50% Flat Discount Applied! 🚀');
    } else {
      setCouponError('Invalid coupon. Try "REVISE20" for 20% OFF!');
    }
  };

  return (
    <div className="cart-overlay-backdrop" onClick={onClose}>
      <div className="cart-drawer-container" onClick={(e) => e.stopPropagation()}>
        {/* Cart Header */}
        <div className="cart-drawer-header">
          <div className="cart-title-box">
            <ShoppingBag size={20} className="cart-title-icon" />
            <h3>Your Revision Cart</h3>
            <span className="cart-count-pill">{cartItems.length} items</span>
          </div>
          <button onClick={onClose} className="cart-close-btn" aria-label="Close cart">
            <X size={20} />
          </button>
        </div>

        {/* Cart Body */}
        {cartItems.length > 0 ? (
          <div className="cart-drawer-body">
            {/* List of Cart Items */}
            <div className="cart-items-list">
              {cartItems.map((item) => (
                <div key={item.id} className="cart-item-card">
                  <div className="cart-item-info">
                    <span className="item-cat-pill" style={{ color: item.badgeColor, borderColor: item.badgeColor }}>
                      {item.category}
                    </span>
                    <h4 className="item-title">{item.title}</h4>
                    <span className="item-pages-text">{item.pages} Pages PDF • Instant Access</span>
                  </div>

                  <div className="cart-item-right">
                    <div className="item-pricing">
                      <span className="item-price">₹{item.price}</span>
                      <span className="item-orig-price">₹{item.originalPrice}</span>
                    </div>
                    <button 
                      onClick={() => onRemoveItem(item.id)}
                      className="btn-remove-item"
                      title="Remove note"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {/* Student Coupon Box */}
            <div className="coupon-box-card">
              <div className="coupon-title">
                <Tag size={15} />
                <span>Have a Student Promo Code?</span>
              </div>
              <form onSubmit={handleApplyCoupon} className="coupon-form">
                <input 
                  type="text" 
                  placeholder="Try 'REVISE20'"
                  value={couponCode}
                  onChange={(e) => setCouponCode(e.target.value)}
                  className="coupon-input"
                />
                <button type="submit" className="btn-apply-coupon">
                  Apply
                </button>
              </form>
              {couponSuccess && <p className="coupon-msg-success">{couponSuccess}</p>}
              {couponError && <p className="coupon-msg-error">{couponError}</p>}
            </div>

            {/* Price Summary Breakdown */}
            <div className="cart-summary-card">
              <div className="summary-row">
                <span>Original Total:</span>
                <span className="strikethrough">₹{originalSubtotal}</span>
              </div>
              <div className="summary-row highlight-green">
                <span>Store Discount:</span>
                <span>- ₹{originalSubtotal - subtotal}</span>
              </div>
              {appliedDiscount > 0 && (
                <div className="summary-row highlight-green">
                  <span>Student Promo ({appliedDiscount}%):</span>
                  <span>- ₹{couponSavings}</span>
                </div>
              )}
              <div className="summary-divider"></div>
              <div className="summary-row final-row">
                <span>Final Payable:</span>
                <span className="final-price">₹{finalTotal}</span>
              </div>
            </div>

            {/* Security Guarantee Note */}
            <div className="cart-trust-badge">
              <ShieldCheck size={16} className="trust-icon" />
              <span>Instant direct PDF download after payment + Email delivery</span>
            </div>
          </div>
        ) : (
          <div className="empty-cart-view">
            <div className="empty-icon-box">🛒</div>
            <h4>Your cart is empty</h4>
            <p>Add individual ₹50 notes or the complete bundle to begin your quick revision!</p>
            <button onClick={onClose} className="btn-primary">
              <Zap size={16} />
              <span>Browse ₹50 Notes</span>
            </button>
          </div>
        )}

        {/* Cart Drawer Footer / Checkout Action */}
        {cartItems.length > 0 && (
          <div className="cart-drawer-footer">
            <button 
              onClick={() => onProceedCheckout(finalTotal, cartItems)}
              className="btn-checkout-now"
            >
              <span>Proceed to Pay ₹{finalTotal}</span>
              <ArrowRight size={18} />
            </button>
            <button onClick={onClearCart} className="btn-clear-cart">
              Clear Cart
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
