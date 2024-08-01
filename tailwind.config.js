/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,js}"],
  theme: {
    extend: {
      fontFamily: {
        FiraMono: ["Fira Mono", "monospace"],
        Montserrat: ["Montserrat", "sans-serif"],
        DancingScript: ["Dancing Script", "cursive"],
        Poppins: ["Poppins", "sans-serif"],
        GillSansUltrabold: ["GillSansUltraBold", "sans-serif"],
      },
    },
  },
  plugins: [],
};
