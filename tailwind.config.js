module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      keyframes: {
        scroll: {
          '0%': { transform: 'translateX(100%)' },
          '100%': { transform: 'translateX(-100%)' },
        },
        spin: {
          '0%': { transform: 'rotate(0deg)' },
          '100%': { transform: 'rotate(360deg)' },
        },
      },
      animation: {
        scroll: 'scroll 10s linear infinite',
        spin: 'spin 1.5s linear infinite',
      },
      colors: {
        primary: {
          light: '#ff7f7f', 
          DEFAULT: '#ff0000', 
          dark: '#b30000', 
        },
        secondary: {
          light: '#e0e0e0', 
          DEFAULT: '#ffffff', 
          dark: '#c0c0c0', 
        },
        accent: {
          light: '#4d4d4d', 
          DEFAULT: '#000000', 
          dark: '#1a1a1a', 
        },
      },
      fontFamily: {
        sans: ['Roboto', 'sans-serif'],
      },
    },
  },
  plugins: [require('tailwind-scrollbar-hide')],
};
