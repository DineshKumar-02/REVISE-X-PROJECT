import React from 'react';
import { TESTIMONIALS } from '../data/notesData';
import { Star, Quote, Award } from 'lucide-react';

export default function Testimonials() {
  return (
    <section className="testimonials-section">
      <div className="testimonials-container">
        <div className="section-header-center">
          <div className="section-pill">
            <Award size={14} />
            <span>Proven Student Success</span>
          </div>
          <h2 className="section-title">
            Loved by <span className="text-gradient">3,800+ Students & Developers</span>
          </h2>
          <p className="section-subtitle">
            See how engineering students and freshers cracked internships and placements with our ₹50 revision guides.
          </p>
        </div>

        <div className="testimonials-grid">
          {TESTIMONIALS.map((t, idx) => (
            <div key={idx} className="testimonial-card">
              <div className="testimonial-header">
                <img src={t.avatar} alt={t.name} className="student-avatar" />
                <div className="student-info">
                  <h4 className="student-name">{t.name}</h4>
                  <span className="student-role">{t.role}</span>
                  <span className="student-college">{t.college}</span>
                </div>
              </div>

              <div className="star-rating">
                {[...Array(5)].map((_, i) => (
                  <Star key={i} size={15} className="star-icon" />
                ))}
              </div>

              <p className="testimonial-text">"{t.text}"</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
