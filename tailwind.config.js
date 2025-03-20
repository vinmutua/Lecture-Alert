/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './apps/*/templates/**/*.html',
    './node_modules/flowbite/**/*.js'  // Add this line
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')  // Add this line
  ],
}

