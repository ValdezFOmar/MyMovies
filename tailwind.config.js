/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ['./MyMovies/movies/templates/*/*.{html,js}'],
    theme: {
        extend: {},
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
    ],
}

