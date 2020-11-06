/** get saved theme */
let ui_theme = localStorage.getItem('theme');
ui_theme == null ? setTheme('green') : setTheme(ui_theme);

function setTheme(theme) {
    document.getElementById('theme-style').href = themes_path + theme.toLowerCase() + '.css';
    localStorage.setItem('theme', theme.toLowerCase())
}