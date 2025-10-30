/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: ['./src/**/*.{svelte,ts,js}'],
  theme: {
    fontFamily: {
      display: ["Fleur De Leah", "cursive"],
    },
    extend: {
      colors: {
        brand: {
          DEFAULT: '#13b981',
          dark: '#0f9b6b'
        }
      },
    },
  },
  plugins: [require('@tailwindcss/forms'), require('@tailwindcss/typography')]
};
