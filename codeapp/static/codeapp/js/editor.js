/*----------------
    editor script
-----------------*/

var editor;
var editor_id = JSON.parse(document.getElementById("editor_id").textContent);
var LANGS = JSON.parse(document.getElementById("langs").textContent);
var THEMES = [
    {value: 'light', display: 'Light'},
    {value: 'dark', display: 'Dark'},
    {value: 'high-contrast', display: 'High Contrast'}
];
var datakey = "key";
var localdata = localDataStorage("codeapp.code");
if (!localdata.get(datakey)) {
    localdata.set(datakey, {
        user_theme: THEMES[0].value
    })
}

$(document).ready(async function () {

    /** wait until editor loaded */
    while (window[editor_id + "_monaco_editor"] === undefined) {
        await sleep(100)
    }
    editor = window[editor_id + "_monaco_editor"];
    personalizeThemes();

    let savedData = localdata.get(datakey);
    changeEditorTheme(savedData.user_theme);

    themePickerListener(savedData.user_theme);
    langPickerListener();
    showEditor();
});

function showEditor() {
    $(".loader").css({'display': 'none'});
    $(".code-area").removeClass('invisible')
}

function personalizeThemes() {
    /** Create personalized themes inheriting monaco default themes (vs, vs-dark, hc-black)*/
    monaco.editor.defineTheme(THEMES[0].value, {
        base: 'vs',
        inherit: true,
        rules: [{background: 'FFFFFF'}],
        colors: {
            'editor.lineHighlightBackground': '#00A1FF0F'
        }
    });
    monaco.editor.defineTheme(THEMES[1].value, {
        base: 'vs-dark',
        inherit: true,
        rules: [],
        colors: {
            'editor.lineHighlightBackground': '#00A1FF0F'
        }
    });
    monaco.editor.defineTheme(THEMES[2].value, {
        base: 'hc-black',
        inherit: true,
        rules: [],
        colors: {}
    });
}

function changeEditorTheme(theme) {
    monaco.editor.setTheme(theme);
}

function changeEditorLanguage(lang) {
    monaco.editor.setModelLanguage(editor.getModel(), lang);
}

function updateLocalData(key, value) {
    /** Update local data (saved in browser cache)*/
    let data = localdata.get(datakey);
    data[key] = value;
    localdata.set(datakey, data);
}

function themePickerListener(user_theme) {
    /** Populate dom select object with themes options */
    THEMES.forEach(theme => {
        var option = document.createElement('option');
        option.value = theme.value;
        option.textContent = theme.display;
        if (theme.value === user_theme) {
            option.selected = true;
        }
        $("#theme-picker").append(option);
    });
    /** on change listener */
    $("#theme-picker").change(function () {
        changeEditorTheme(this.value);
        updateLocalData('user_theme', this.value)
    });
}

function getLangIconClass(lang) {
    var icon_class = "devicons devicons-";
    if (lang === 'javascript')
        return icon_class + 'nodejs_small'; // return icon_class + 'javascript';
    if (lang === 'c' || lang === 'cpp' || lang === 'typescript')
        return "fas fa-code";
    else
        return icon_class + lang;
}

function langPickerListener() {
    /** Populate dom select object with programming languages options */
    LANGS.forEach(lang => {
        var option = document.createElement('option');
        option.value = lang.value;
        option.textContent = lang.display;
        if (LANGS.indexOf(lang) === 0) {
            option.selected = true;
            changeEditorLanguage(lang.value);
            $("#lang-icon").attr('class', getLangIconClass(lang.value));
        }
        $("#lang-picker").append(option);
    });
    /** on change listener */
    $("#lang-picker").change(function () {
        changeEditorLanguage(this.value);
        $("#lang-icon").attr('class', getLangIconClass(this.value));
    });
}

function sleep(millis) {
    return new Promise(resolve => setTimeout(resolve, millis));
}

