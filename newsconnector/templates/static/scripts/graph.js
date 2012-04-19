function init(min_date, default_min_date, data_url, is_staff, next){
    $('#filter').keyup(function() {
            delay(function(){
              var q = $('#filter').val().toLowerCase();
                      
              if(q == '') {
                      $('#keywordscloud li').show();
              }else{
                      var keys = $('#keywordscloud li');
                      keys.filter('[key*="'+q+'"]').show();
                      keys.not('[key*="'+q+'"]').hide();
              }
            }, 500 );
    });
    
    var options = {
        bounds: {min: min_date, max: new Date()},
        defaultValues: {min: default_min_date, max: new Date()},
        formatter: function(value){ 
                var d = new Date(value)
                return d.toString('MMM dd');
                }
        };
			
    function getDelKeyword(is_admin, id, next){
        if(is_admin){
            return " <small class='del-keyword'><a href='/keyword/delete/"+ id +"/?next="+next+"'>[del]</small>";
        }
        return '';
    }
    
    $("#date-slider").dateRangeSlider(options).bind('valuesChanging', function(sender,event) {
        var one_day=1000*60*60*24;
        var span = Math.round((event.values.max - event.values.min)/one_day);
        $(".ui-rangeSlider-bar").html(span + " days");
    }).bind('valuesChanged', function(sender,event) {
            $("#keys").html('<div id="loading">loading...</div>');
            $.get(data_url + event.values.min.getTime() + '/' + event.values.max.getTime() + '/', function(data) {
                var keys = $("<ul class='xmpl' id='keywordscloud'></ul>");
                $.each(data.children, function(i, value){
                    var keyword = $("<li value='" + value.data.count +
                                    "' id='key" + value.id + "' key='"+ value.name + 
                                    "'>" + value.name +
                                    getDelKeyword(is_staff, value.id, next) +
                                    "</li>")
                                  .data('articles', value.data.articles)
                                  .click(function(){
                                          var data = $(this).data('articles');
                                          if(data){
                                              var html = '<div class="h1"><label>'+$(this).text()+'<br/><small>'+value.data.count+' items</small></label></div>';
                                              count = 0;
                                              for(var i in data){
                                                      article = data[i]
                                                      if (article.data.id) {
                                                              //checked = count == 0 ? 'checked' : '';
                                                              checked = ''
                                                              html += '<div><input id="ac-' + article.data.id + '" name="accordion-1" type="radio" ' + checked + '/>' +
                                                                    '<label for="ac-' + article.data.id + '">' + article.data.title + '</label>' +
                                                                    '<article class="ac-small">' +
                                                                    '<p>[' + article.data.source + '] - ' + article.data.date + '<br/>' + article.data.description + 
                                                                    ' <a target="_blank" href="' + article.data.link +'">more...</a></p>' +
                                                                    '</article></div>';
                                                      }
                                                      count++;
                                              }
                                              $('#article-details').html(html).data('node_id',$(this).attr('id')); 
                                            }
                                  });
                    keys.append(keyword)
                });
				
                $("#keys").html(keys);                                
                keys.tagcloud({height:500, type:"sphere",sizemin:12, sizemax:50,colormin:"fff",colormax:"18e"});				
            });
    });
}
