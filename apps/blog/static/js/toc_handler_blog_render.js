function addTOC() {
    var tocElement, bodyContent, mainElement;

    tocElement = document.createElement('nav');
    tocElement.setAttribute('id', 'toc');

    bodyContent = document.body.innerHTML;

    mainElement = document.createElement('main');
    mainElement.insertAdjacentHTML('afterbegin', bodyContent);

    generateTOC(tocElement, mainElement);

    document.body.innerHTML = '';
    document.body.insertAdjacentHTML('afterbegin', tocElement.outerHTML);
    document.body.insertAdjacentHTML('beforeend', mainElement.outerHTML);
    document.body.classList.add('toc-loaded');

    // FUNCTIONS

    function generateTOC(tocElement, mainElement) {
        var headlineElements, currentElement, currentHeadlineElement, currentHeadlineLinkElement, i;

        headlineElements = mainElement.querySelectorAll('h1, h2, h3, h4, h5, h6');

        for (i = 0; i < headlineElements.length; i++) {
            currentElement = headlineElements[i];
            currentElement.setAttribute('id', i);

            currentHeadlineLinkElement = document.createElement('a');
            currentHeadlineLinkElement.setAttribute('href', '#' + i);
            currentHeadlineLinkElement.innerHTML = currentElement.innerHTML;

            currentHeadlineElement = document.createElement('div');
            currentHeadlineElement.classList.add(currentElement.tagName.replace('H', 'level-'));
            currentHeadlineElement.insertAdjacentHTML('afterbegin', currentHeadlineLinkElement.outerHTML);

            tocElement.insertAdjacentHTML('beforeend', currentHeadlineElement.outerHTML);
        }
    }
};

document.addEventListener('DOMContentLoaded', addTOC, false);

window.onload = function() { // This tells to wait until the DOM has loaded to execute!

    // THIS RENDERS MARKDOWN TO HTML! //
    let mark = new Remarkable();

    let to_render = document.querySelector('.toRender');

    let to_display = document.querySelector('.toDisplay');

    let rendered_text = mark.render(to_render.textContent);
    to_display.innerHTML = rendered_text

    let body_Tag = document.querySelector('body');
    let nav_Tag = document.querySelector('#toc');
    let main_Tag = document.querySelector('main');

    // Creation and Positioning of BUTTON
    let div_fbtn = document.createElement('DIV');
    document.body.insertBefore(div_fbtn, main_Tag);
    div_fbtn.classList.add('btn_div_for')
    div_fbtn.style.height = '100%'

    let btn = document.createElement('BUTTON');
    btn.innerHTML = 'Show<br>TOC';
    btn.classList = 'show_hide_toc';
    // document.body.insertBefore(btn, main_Tag);
    div_fbtn.appendChild(btn);
    hide_toc();

    // SHOW / HIDE FUNCTIONS
    function hide_toc() {
        btn.innerHTML = 'Show<br>TOC';
        nav_Tag.style.display = 'none';

    };

    function show_toc() {
        btn.innerHTML = 'Hide<br>TOC';
        nav_Tag.style.display = '';

    };

    // SHOW OR HIDE - EVENT LISTENER!
    btn.addEventListener('click', function() {
        if (this.innerHTML == 'Hide<br>TOC') {
            hide_toc()
        }
        else {
            show_toc()
    }});

};