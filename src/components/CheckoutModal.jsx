import React, { useState } from 'react';
import { X, QrCode, CreditCard, Landmark, ShieldCheck, CheckCircle2, Download, ArrowRight, Loader2, Sparkles, Smartphone } from 'lucide-react';
import confetti from 'canvas-confetti';

export default function CheckoutModal({ 
  isOpen, 
  onClose, 
  totalAmount, 
  items, 
  onPaymentSuccess 
}) {
  const [activeMethod, setActiveMethod] = useState('upi');
  const [studentName, setStudentName] = useState('');
  const [studentEmail, setStudentEmail] = useState('');
  const [upiId, setUpiId] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [isPaidSuccess, setIsPaidSuccess] = useState(false);
  const [orderId, setOrderId] = useState('');

  if (!isOpen) return null;

  const handleSimulatePayment = (e) => {
    e.preventDefault();
    if (!studentEmail) {
      alert('Please enter your email to receive your secure PDF download link!');
      return;
    }

    setIsProcessing(true);

    // Simulate backend payment verification & signature validation
    setTimeout(() => {
      setIsProcessing(false);
      setIsPaidSuccess(true);
      const generatedOrderId = `RZP_${Date.now().toString().slice(-8)}`;
      setOrderId(generatedOrderId);

      // Trigger Celebration Confetti!
      try {
        confetti({
          particleCount: 120,
          spread: 70,
          origin: { y: 0.6 }
        });
      } catch (err) {
        console.error('Confetti error:', err);
      }

      if (onPaymentSuccess) {
        onPaymentSuccess();
      }
    }, 1800);
  };

  const handleDownloadSamplePdf = (title) => {
    // Generates a mock download action
    alert(`📥 Downloading: "${title}.pdf"\n\nThank you for choosing Revise-X! A permanent backup copy was also sent to ${studentEmail}`);
  };

  return (
    <div className="modal-backdrop" onClick={!isProcessing ? onClose : null}>
      <div className="modal-container checkout-modal" onClick={(e) => e.stopPropagation()}>
        {/* Payment Gateway Header */}
        <div className="checkout-header">
          <div className="gateway-brand">
            <div className="gateway-badge">
              <ShieldCheck size={16} /> 256-Bit SSL Encrypted
            </div>
            <h3>Revise-X Checkout</h3>
          </div>
          {!isPaidSuccess && (
            <button onClick={onClose} className="modal-close-btn" disabled={isProcessing}>
              <X size={20} />
            </button>
          )}
        </div>

        {!isPaidSuccess ? (
          <form onSubmit={handleSimulatePayment} className="checkout-form">
            {/* Student Details */}
            <div className="checkout-section">
              <label className="input-label">Student Details (for PDF Delivery):</label>
              <div className="input-row">
                <input 
                  type="text" 
                  placeholder="Full Name"
                  required
                  value={studentName}
                  onChange={(e) => setStudentName(e.target.value)}
                  className="form-input"
                  disabled={isProcessing}
                />
                <input 
                  type="email" 
                  placeholder="Email Address (required for download link)"
                  required
                  value={studentEmail}
                  onChange={(e) => setStudentEmail(e.target.value)}
                  className="form-input"
                  disabled={isProcessing}
                />
              </div>
            </div>

            {/* Order Items Preview */}
            <div className="checkout-items-preview">
              <div className="items-preview-header">
                <span>Purchasing ({items.length} notes):</span>
                <span className="items-preview-total">Total: ₹{totalAmount}</span>
              </div>
              <div className="items-preview-tags">
                {items.map((item) => (
                  <span key={item.id} className="preview-item-chip">
                    {item.title} (₹{item.price})
                  </span>
                ))}
              </div>
            </div>

            {/* Payment Method Selector Tabs */}
            <div className="payment-methods-tabs">
              <button 
                type="button"
                onClick={() => setActiveMethod('upi')}
                className={`method-tab ${activeMethod === 'upi' ? 'active' : ''}`}
              >
                <Smartphone size={16} />
                <span>UPI (GPay / PhonePe / Paytm)</span>
              </button>
              <button 
                type="button"
                onClick={() => setActiveMethod('cards')}
                className={`method-tab ${activeMethod === 'cards' ? 'active' : ''}`}
              >
                <CreditCard size={16} />
                <span>Cards</span>
              </button>
              <button 
                type="button"
                onClick={() => setActiveMethod('netbanking')}
                className={`method-tab ${activeMethod === 'netbanking' ? 'active' : ''}`}
              >
                <Landmark size={16} />
                <span>Net Banking</span>
              </button>
            </div>

            {/* Payment Method Details */}
            <div className="payment-method-panel">
              {activeMethod === 'upi' && (
                <div className="upi-panel">
                  <div className="qr-scanner-box">
                    <div className="qr-dummy">
                      <QrCode size={110} className="qr-icon" />
                      <span className="qr-scan-text">Scan with any UPI App</span>
                    </div>
                    <div className="upi-apps-icons">
                      <span className="upi-app-badge gpay">GPay</span>
                      <span className="upi-app-badge phonepe">PhonePe</span>
                      <span className="upi-app-badge paytm">Paytm</span>
                      <span className="upi-app-badge cred">CRED</span>
                    </div>
                  </div>

                  <div className="upi-id-input-box">
                    <span className="or-text">— OR Enter UPI ID —</span>
                    <input 
                      type="text" 
                      placeholder="e.g. yourname@okhdfcbank or 9876543210@paytm"
                      value={upiId}
                      onChange={(e) => setUpiId(e.target.value)}
                      className="form-input"
                      disabled={isProcessing}
                    />
                  </div>
                </div>
              )}

              {activeMethod === 'cards' && (
                <div className="cards-panel">
                  <input 
                    type="text" 
                    placeholder="Card Number (XXXX XXXX XXXX XXXX)"
                    defaultValue="4111 2222 3333 4444"
                    className="form-input"
                    disabled={isProcessing}
                  />
                  <div className="input-row">
                    <input 
                      type="text" 
                      placeholder="MM / YY" 
                      defaultValue="12/28"
                      className="form-input"
                      disabled={isProcessing}
                    />
                    <input 
                      type="password" 
                      placeholder="CVV" 
                      defaultValue="123"
                      maxLength={3}
                      className="form-input"
                      disabled={isProcessing}
                    />
                  </div>
                </div>
              )}

              {activeMethod === 'netbanking' && (
                <div className="netbanking-panel">
                  <select className="form-input" disabled={isProcessing}>
                    <option>HDFC Bank</option>
                    <option>State Bank of India (SBI)</option>
                    <option>ICICI Bank</option>
                    <option>Axis Bank</option>
                    <option>Kotak Mahindra Bank</option>
                  </select>
                </div>
              )}
            </div>

            {/* Pay Button */}
            <div className="checkout-submit-box">
              <button 
                type="submit" 
                disabled={isProcessing}
                className="btn-pay-secure"
              >
                {isProcessing ? (
                  <>
                    <Loader2 size={20} className="spinner" />
                    <span>Verifying Secure Payment (₹{totalAmount})...</span>
                  </>
                ) : (
                  <>
                    <ShieldCheck size={20} />
                    <span>Pay ₹{totalAmount} via Secure UPI / Card</span>
                  </>
                )}
              </button>

              <div className="payment-security-footer">
                <span>🔒 Mock Razorpay Checkout • Instant PDF Delivery</span>
              </div>
            </div>
          </form>
        ) : (
          /* Payment Success View */
          <div className="payment-success-view">
            <div className="success-icon-box">
              <CheckCircle2 size={54} className="success-icon" />
            </div>

            <h3 className="success-title">Payment Successful! 🎉</h3>
            <p className="success-msg">
              Thank you <strong>{studentName || 'Student'}</strong>! Your order <code>{orderId}</code> has been confirmed.
            </p>
            <p className="delivery-notice">
              📧 PDF download links and receipts have also been dispatched to <strong>{studentEmail}</strong>.
            </p>

            {/* List of purchased downloads */}
            <div className="purchased-downloads-list">
              <h4>Your Unlocked Revision Notes:</h4>
              {items.map((item) => (
                <div key={item.id} className="download-item-row">
                  <div className="download-item-info">
                    <span className="dl-title">{item.title}</span>
                    <span className="dl-specs">{item.pages} Pages • Full High-Res PDF</span>
                  </div>
                  <button 
                    onClick={() => handleDownloadSamplePdf(item.title)}
                    className="btn-download-pdf"
                  >
                    <Download size={16} />
                    <span>Download PDF</span>
                  </button>
                </div>
              ))}
            </div>

            <div className="success-actions">
              <button onClick={onClose} className="btn-primary">
                Return to Notes Catalog
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
