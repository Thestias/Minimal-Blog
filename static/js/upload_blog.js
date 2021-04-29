window.onload = function () {
    let submitted_files = document.querySelector('#fileu')
    let markdown_editor = document.querySelector('#id_markdown')
    let reader = new FileReader();


    submitted_files.addEventListener('change', function () {

        let file = submitted_files.files[0]


        reader.addEventListener('load', function (e) {
            markdown_editor.value = e.target.result
        })

        reader.readAsText(file)
    })

}