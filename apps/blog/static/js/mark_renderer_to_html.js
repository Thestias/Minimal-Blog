window.onload = function() {
    let mark = new Remarkable();

    let div_select = document.querySelector('.mark_preview');

    let textarea_select = document.querySelector('textarea');

    function change_html(e) {
      let rendered_text = mark.render(textarea_select.value)
      div_select.innerHTML = rendered_text
    };

    textarea_select.addEventListener("input", change_html);
};