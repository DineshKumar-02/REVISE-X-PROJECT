import React, { useState } from 'react';
import { X, QrCode, CreditCard, Landmark, ShieldCheck, CheckCircle2, Download, Smartphone } from 'lucide-react';
import confetti from 'canvas-confetti';

/**
 * CheckoutModal Component - Realistic simulated checkout flow
 * 
 * Clean, human-coded payment modal featuring:
 * - Student name & email collection for PDF delivery
 * - Multiple payment methods: UPI, QR Code, Debit/Credit Card, NetBanking
 * - Instant celebratory success screen with direct PDF download button
 */
export default function CheckoutModal({ 
  isOpen, 
  onClose, 
  totalAmount, 
  items = [], 
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

  // Handle simulated payment verification
  const handleSimulatePayment = (e) => {
    e.preventDefault();
    if (!studentEmail) {
      alert('Please enter your email to receive your PDF download link.');
      return;
    }

    setIsProcessing(true);
    const genOrderId = `REVX_${Date.now().toString().slice(-8)}`;

    setTimeout(() => {
      setIsProcessing(false);
      setIsPaidSuccess(true);
      setOrderId(genOrderId);

      // Pop-up message explicitly requested by user
      alert(`🎉 Payment Successful!\n\nOrder ID: ${genOrderId}\nTotal Paid: ₹${totalAmount}\n\nYour study notes are ready! Click OK to download your PDFs.`);

      try {
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.6 }
        });
      } catch {
        // Safe fallback if confetti canvas is not supported
      }

      if (onPaymentSuccess) {
        onPaymentSuccess();
      }
    }, 600);
  };

  // Trigger client-side PDF download
  const handleDownloadPdf = (note) => {
    const fileName = note.pdfFileName || `${note.id}.pdf`;
    const link = document.createElement('a');
    link.href = `/notebooks/${fileName}`;
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="modal-backdrop" onClick={!isProcessing ? onClose : null}>
      <div className="modal-container checkout-modal" onClick={(e) => e.stopPropagation()}>
        
        {/* Modal Header */}
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

        {/* Modal Body: Payment Form OR Success Screen */}
        {!isPaidSuccess ? (
          <form onSubmit={handleSimulatePayment} className="checkout-form">
            
            {/* Student Contact Info */}
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
                  placeholder="Email Address"
                  required
                  value={studentEmail}
                  onChange={(e) => setStudentEmail(e.target.value)}
                  className="form-input"
                  disabled={isProcessing}
                />
              </div>
            </div>

            {/* Payment Method Selector Tabs */}
            <div className="checkout-section">
              <label className="input-label">Select Payment Method:</label>
              <div className="payment-tabs">
                <button
                  type="button"
                  onClick={() => setActiveMethod('upi')}
                  className={`payment-tab-btn ${activeMethod === 'upi' ? 'active' : ''}`}
                >
                  <Smartphone size={16} />
                  <span>UPI Apps</span>
                </button>

                <button
                  type="button"
                  onClick={() => setActiveMethod('qr')}
                  className={`payment-tab-btn ${activeMethod === 'qr' ? 'active' : ''}`}
                >
                  <QrCode size={16} />
                  <span>QR Code</span>
                </button>

                <button
                  type="button"
                  onClick={() => setActiveMethod('card')}
                  className={`payment-tab-btn ${activeMethod === 'card' ? 'active' : ''}`}
                >
                  <CreditCard size={16} />
                  <span>Card</span>
                </button>

                <button
                  type="button"
                  onClick={() => setActiveMethod('netbanking')}
                  className={`payment-tab-btn ${activeMethod === 'netbanking' ? 'active' : ''}`}
                >
                  <Landmark size={16} />
                  <span>NetBanking</span>
                </button>
              </div>
            </div>

            {/* Selected Method Details */}
            <div className="payment-method-details">
              {activeMethod === 'upi' && (
                <div className="tab-pane-content">
                  <div className="upi-apps-row">
                    <span className="upi-app-chip">GPay</span>
                    <span className="upi-app-chip">PhonePe</span>
                    <span className="upi-app-chip">Paytm</span>
                    <span className="upi-app-chip">CRED</span>
                  </div>
                  <input 
                    type="text" 
                    placeholder="Enter UPI ID (e.g. student@okhdfcbank)"
                    value={upiId}
                    onChange={(e) => setUpiId(e.target.value)}
                    className="form-input"
                    disabled={isProcessing}
                  />
                </div>
              )}

              {activeMethod === 'qr' && (
                <div className="tab-pane-content text-center">
                  <div className="qr-preview-box">
                    <QrCode size={90} className="qr-icon" />
                    <p className="qr-caption">Scan with any UPI app to pay ₹{totalAmount}</p>
                  </div>
                </div>
              )}

              {activeMethod === 'card' && (
                <div className="tab-pane-content">
                  <input type="text" placeholder="Card Number (XXXX XXXX XXXX XXXX)" className="form-input" disabled={isProcessing} />
                  <div className="input-row" style={{ marginTop: '8px' }}>
                    <input type="text" placeholder="MM/YY" className="form-input" disabled={isProcessing} />
                    <input type="password" placeholder="CVV" maxLength="3" className="form-input" disabled={isProcessing} />
                  </div>
                </div>
              )}

              {activeMethod === 'netbanking' && (
                <div className="tab-pane-content">
                  <select className="form-input" disabled={isProcessing}>
                    <option>State Bank of India (SBI)</option>
                    <option>HDFC Bank</option>
                    <option>ICICI Bank</option>
                    <option>Axis Bank</option>
                    <option>Kotak Mahindra Bank</option>
                  </select>
                </div>
              )}
            </div>

            {/* Total Summary and Submit Button */}
            <div className="checkout-footer">
              <div className="checkout-total-pill">
                <span>Total Payable:</span>
                <strong>₹{totalAmount}</strong>
              </div>

              <button 
                type="submit" 
                className="btn-primary btn-full-width"
                disabled={isProcessing}
              >
                {isProcessing ? (
                  <span>Verifying Payment...</span>
                ) : (
                  <span>Pay ₹{totalAmount} & Get Notes</span>
                )}
              </button>
            </div>

          </form>
        ) : (
          /* Payment Success State */
          <div className="checkout-success-view">
            <div className="success-icon-box">
              <CheckCircle2 size={52} className="success-check-icon" />
            </div>
            
            <h3 className="success-title">Payment Successful! 🎉</h3>
            <p className="success-subtitle">Order ID: <strong>{orderId}</strong></p>
            <p className="success-desc">
              Thank you, <strong>{studentName || 'Developer'}</strong>! A confirmation email was simulated to <strong>{studentEmail}</strong>. 
              Click below to download your notes right now:
            </p>

            {/* List of Purchased Notes for Instant Download */}
            <div className="purchased-downloads-list">
              {items.map((item) => (
                <div key={item.id} className="download-item-row">
                  <div className="download-item-info">
                    <span className="download-item-title">{item.title}</span>
                    <span className="download-item-pages">{item.pages} Pages • Vector PDF</span>
                  </div>
                  <button 
                    type="button"
                    onClick={() => handleDownloadPdf(item)}
                    className="btn-download-note"
                  >
                    <Download size={15} />
                    <span>Download PDF</span>
                  </button>
                </div>
              ))}
            </div>

            <button onClick={onClose} className="btn-secondary btn-full-width" style={{ marginTop: '16px' }}>
              Close & Back to Notes
            </button>
          </div>
        )}

      </div>
    </div>
  );
}
