module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          light: '#ff7f7f', // Light red
          DEFAULT: '#ff0000', // Primary red
          dark: '#b30000', // Dark red
        },
        secondary: {
          light: '#e0e0e0', // Light gray
          DEFAULT: '#ffffff', // Primary white
          dark: '#c0c0c0', // Darker gray
        },
        accent: {
          light: '#4d4d4d', // Light black
          DEFAULT: '#000000', // Primary black
          dark: '#1a1a1a', // Dark black
        },
      },
      fontFamily: {
        sans: ['Roboto', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
