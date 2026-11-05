/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // LITAN brand palette — adjust once visual identity is confirmed
        primary: {
          50:  '#f0f4ff',
          100: '#dce8ff',
          200: '#b9d3ff',
          500: '#3b6fd4',
          600: '#2a58b8',
          700: '#1e4096',
          900: '#112163',
        },
        accent: '#e8701a',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
