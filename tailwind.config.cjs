/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ['./src/**/*.{html,js,svelte,ts}'],
    theme: {
        extend: {
            fontFamily: {
                title: [`Life Savers`, `cursive`],
                headers: [`Unna`, `serif`],
                body: [`Frank Ruhl Libre`, `serif`]   
            },
            colors: {
                background: "#F7F0F0",
                text: "#484349",
                light_blue: "#8AF3FF",
                dark_blue: "#18A999",
                green: "#109648"
            },
        },
    },
    plugins: [],
}
