import React from 'react';

/**
 * ReviseXLogoMark - Clean, Modern Developer Brand Logo
 * 
 * Simple, human-coded SVG icon representing a developer's
 * revision notebook with an illuminated code 'X'.
 */
export function ReviseXLogoMark({ size = 32, className = "" }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 40 40"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={`logo-svg ${className}`}
      aria-label="Revise-X Logo"
    >
      {/* Background Rounded Squircle */}
      <rect width="40" height="40" rx="10" fill="#0f172a" />
      <rect x="0.75" y="0.75" width="38.5" height="38.5" rx="9.25" stroke="#38bdf8" strokeOpacity="0.4" strokeWidth="1.5" />
      
      {/* Left Cheatsheet Page */}
      <path
        d="M11 11H25C26.1 11 27 11.9 27 13V29H13C11.9 29 11 28.1 11 27V11Z"
        fill="#2563eb"
        fillOpacity="0.25"
        stroke="#38bdf8"
        strokeWidth="1.5"
      />
      
      {/* Ruled lines inside notebook */}
      <line x1="15" y1="16" x2="23" y2="16" stroke="#93c5fd" strokeWidth="1.5" strokeLinecap="round" />
      <line x1="15" y1="20" x2="21" y2="20" stroke="#93c5fd" strokeWidth="1.5" strokeLinecap="round" />
      
      {/* Foreground Illuminated 'X' / Code Bracket */}
      <path
        d="M20 14L28 26M28 14L20 26"
        stroke="#38bdf8"
        strokeWidth="2.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <circle cx="24" cy="20" r="2" fill="#60a5fa" />
    </svg>
  );
}

export default ReviseXLogoMark;
