function setSidebarMaxHeight(sidebarId) {
    // Sets height of the sidebar on the post page to make the sidebar scrollable.
    // Not in use any more, since the same functionality is achieved with CSS.
    $('#' + sidebarId).css('max-height', $(window).height() - $('#' + sidebarId).offset().top);
}


function highlightCategories(){
    // First clear all highlights.
    $('#blog-categories').children('a').each(function(j, category){
        $(category).removeClass('list-group-item-primary');
    });
    // Highlight the current categories tags in the categories list.
    $('.post').mostVisible().find('a.post-category').each(function(i, postCategory){
        // For each category go through all categories on the sidebar and highlight it
        $('#blog-categories').children('a').each(function(j, category){
            if($(category).attr('data-slug') == $(postCategory).attr('data-slug')){
                $(category).addClass('list-group-item-primary');
            }
        });
    });
}


function highlightTags() {
    // First clear all highlights.
    $('#tag-cloud').children('a').each(function(j, tag){
        $(tag).removeClass('font-italic text-underline');
    });
    // Highlight the current post tags in tag cloud.
    $('.post').mostVisible().find('a.post-tag').each(function(i, postTag){
        // For each category go through all categories on the sidebar and highlight it
        $('#tag-cloud').children('a').each(function(j, tag){
            if($(tag).attr('data-slug') == $(postTag).attr('data-slug')){
                $(tag).addClass('font-italic text-underline');
            }
        });
    });
}


function generateContents() {
    // To keep the heading of screen when the content hash link
    // is clicked. Needed due to sticky menu.
    if ($('#nav-contents').length) {

        $(window).on('hashchange', function() {
            window.scrollTo(0, window.pageYOffset - 60);
        });

        $('.post-body').find('*').filter(':header').each(function(idx, header) {
            $(header).attr('id', 'section-' + idx);
            var padding = 0;
            var fontSize = 1.5;
            if($(header).prop('tagName') == "H1"){
                padding = 0; fontSize = 1.5;
            }
            if($(header).prop('tagName') == 'H2') {
                padding = 1; fontSize = 1.4;
            }
            if($(header).prop('tagName') == 'H3') {
                padding = 2; fontSize = 1.3;
            }
            if($(header).prop('tagName') == 'H4') {
                padding = 3; fontSize = 1.2;
            }
            if($(header).prop('tagName') == 'H5') {
                padding = 4; fontSize = 1.1;
            }
            if($(header).prop('tagName') == 'H6') {
                padding = 5; fontSize = 1.0;
            }
            var link = $('<a></a>')
                .attr('href', '#section-' + idx)
                .addClass('text-dark')
                .css({'padding-left': padding + 'em', 'font-size': fontSize + 'em'})
                .text($(header).text())

            if($('#nav-contents').length){
                $('#nav-contents').append(link);
            }   
        });
    }
}


function replaceTextWithDocumentLinks() {
    // Replaces the text inside any .post-body child elements
    // and link to refwith link to document.
    $('.doc-link').each(function(doc_idx, docElem) {
        $('.post-body').each(function(post_idx, postElem) {
            $(postElem).find('*').each(function(idx, elem) {
                var linkText = $(docElem).text();
                if($(elem).text().indexOf(linkText) > -1) {
                    $(elem).html($(elem).html().replace(
                        new RegExp(linkText, 'g'),
                        '<a href="' + $(docElem).attr('href') + '">' + linkText + '</a>'
                    ));
                }
            });
        });
    });
}


function applyTableClass() {
    $('table').each(function(idx, elem) {
        $(elem).addClass('table');
    });
}