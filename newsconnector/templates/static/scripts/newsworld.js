$(document).ready(function(){
    $('#tabs').tabs();

    $('div.article.news-cat label').click(function(){
        $('li.tabs-news a').click();
    });
    $('div.article.sports-cat label').click(function(){
        $('li.tabs-sports a').click();
    });
    $('div.article.entertainment-cat label').click(function(){
        $('li.tabs-entertainment a').click();
    });
    $('div.article.finance-cat label').click(function(){
        $('li.tabs-finance a').click();
    });

    $('#tabs ul li').hover(
       function(){ $(this).stop(true).addClass('hover', 100) },
       function(){ $(this).stop(true).removeClass('hover', 100) }
    );

    $('#tabs, #search-results').on('mouseover', '.article', function(event) {
        $(this).find('div.overlay').stop(true).addClass('show', 100);
    }).on('mouseout', '.article', function(event) {
        $(this).find('div.overlay').stop(true).removeClass('show', 100);
    });

    $('#read-related-close').click(function(event){
        event.preventDefault();
        $('#read-related').fadeOut(300, function(){
            $('#read-results').fadeIn(500);
        });
    });
    function load_more(href, sender){
        _ = sender
        var target = sender.parent().parent().find('#read-more');
        target.append('<a href="#section_top">Back to top</a>');
        $.get(href, function(data) {
            $.each(data.articles, function(i, value){
                var artilce_image_url = value.image_url;
                var image_tag = artilce_image_url != '' ? '<img src="'+artilce_image_url+'" width="64px"/>' : '<img src="/static/images/news2.png" width="64px"/>';

                target.append('<div id="tabs-news" class="ui-tabs-panel"><div class="article">'+
                image_tag +
                '<div class="article-content">'+
                '<span><a target="_blank" href="'+value.link+'">'+
                value.title+'</a></span><br/>'+value.content+'<br/>'+
                '<div class="article-footer">'+value.date+' | '+
                '<a target="_blank" href="'+value.link+'">'+value.source+'</a>'+
                '</div></div>'+
                '<div class="overlay">'+
                '<a class="goto" target="_blank" href="'+value.link+'">'+value.source+'</a>'+
                '<a class="related-button" target="_blank"'+
                'href="/related/'+value.hash_key+'/">View Related</a></div>'+
                '<br style="clear:both"/></div></div>');
                });
            if(data.has_next){
                _.attr('href','/more/'+_.attr('tag')+'/?page='+data.next_page);
            }
        });
    }
    $('a.read-more').click(function(event){
        event.preventDefault();
        var href = $(this).attr('href');
        load_more(href, $(this));
    });

    load_more(newsworld.finance_readmore_href, $('#tabs-finance a.read-more'));
    load_more(newsworld.sports_readmore_href, $('#tabs-sports a.read-more'));
    load_more(newsworld.entertainment_readmore_href, $('#tabs-entertainment a.read-more'));
});
