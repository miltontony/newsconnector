var labelType, useGradients, nativeTextSupport, animate;

(function() {
  var ua = navigator.userAgent,
      iStuff = ua.match(/iPhone/i) || ua.match(/iPad/i),
      typeOfCanvas = typeof HTMLCanvasElement,
      nativeCanvasSupport = (typeOfCanvas == 'object' || typeOfCanvas == 'function'),
      textSupport = nativeCanvasSupport 
        && (typeof document.createElement('canvas').getContext('2d').fillText == 'function');
  //I'm setting this based on the fact that ExCanvas provides text support for IE
  //and that as of today iPhone/iPad current text support is lame
  labelType = (!nativeCanvasSupport || (textSupport && !iStuff))? 'Native' : 'HTML';
  nativeTextSupport = labelType == 'Native';
  useGradients = nativeCanvasSupport;
  animate = !(iStuff || !nativeCanvasSupport);
})();


function init(min_date, default_min_date){
    $("#tooltip").dialog({ autoOpen: false });
    
    //init data
    //var json = data;
    
    var infovis = document.getElementById('infovis');
    var w = infovis.offsetWidth - 50, h = infovis.offsetHeight - 50;
    //init Hypertree
    ht = new $jit.Hypertree({
      //id of the visualization container
      injectInto: 'infovis',
      //type: '3D',
      //canvas width and height
      width: w,
      height: h,
      //Change node and edge styles such as
      //color, width and dimensions.
      Node: {
          dim: 10,
          color: "#f33",
          type: "circle",
          transform: true,
          overridable: true,
      },
      Edge: {
          lineWidth: 1,
          color: "#ccf",
          type: "hyperline"
      },
      Navigation: {  
        enable: true,  
        panning: 'avoid nodes',  
        zooming: 20  
      },
      //Attach event handlers and add text to the
      //labels. This method is only triggered on label
      //creation
      onCreateLabel: function(domElement, node){
          domElement.innerHTML = node.name;
          if(node.id == 'main_node'){
              $("#center").click(function(){
                    var x=ht.graph.getNode(node.id).pos.getc(true);
                    ht.move(x,{ onComplete: function() {
                              ht.controller.onComplete();
                          } })
              })
          }
          $jit.util.addEvent(domElement, 'click', function () {
              if(node.data.description){
                  $("#ac-"+node.data.id).click()
                  return;
              }
              ht.onClick(node.id, {
                  onComplete: function() {                        
                        if(node.data.count){
                          var html = "";
                          count = 0;
                          node.eachAdjacency(function(adj){
                              var child = adj.nodeTo;
                              if (child.data.id) {
                                  checked = count == 0 ? 'checked' : '';
                                  html += '<div><input id="ac-' + child.data.id + '" name="accordion-1" type="radio" ' + checked + '/>' +
                                        '<label for="ac-' + child.data.id + '">' + child.data.title + '</label>' +
                                        '<article class="ac-small">' +
                                        '<p>[' + child.data.source + ']<br/>' + child.data.description + 
                                        ' <a target="_blank" href="' + child.data.link +'">more...</a></p>' +
                                        '</article></div>';
                              }
                              count++;
                          });
                          $('#article-details').html(html).data('node_id',node.id); 
                        }
                  }
              });
          });
      },
      //Change node styles when labels are placed
      //or moved.
      onPlaceLabel: function(domElement, node){
          var style = domElement.style;
          style.display = '';
          style.cursor = 'pointer';
          if (node._depth == 0) {
              style.fontSize = "1em";
              style.color = "#000";

          } else if (node._depth == 1) {
              style.fontSize = "0.8em";
              style.color = "#333";

          /*} else if(node._depth == 2){
              style.fontSize = "0.7em";
              style.color = "#aaa";
            */
          } else {
              style.display = 'none';
          }

          var left = parseInt(style.left);
          var w = domElement.offsetWidth;
          style.left = (left - w / 2) + 'px';
      },
    });

    
    $("#zoom-in").click(function(){
        x = 1.2;
        ht.canvas.scale(x,x)
    });
    
    $("#zoom-out").click(function(){
        x = 0.8;
        ht.canvas.scale(x,x)
    });
    
    $("#infovis").click(function(){
        $("#tooltip").dialog('close')
    });
    
    var options = {
            bounds: {min: min_date, max: new Date()},
            defaultValues: {min: default_min_date, max: new Date()},
            };
    
    $("#date-slider").dateRangeSlider(options).bind('valuesChanging', function(sender,event) {
            var one_day=1000*60*60*24;
            var span = Math.round((event.values.max - event.values.min)/one_day);
                    
            $(".ui-rangeSlider-bar").html(span + " days")
    }).bind('valuesChanged', function(sender,event) {
            $.get('/data/'+event.values.min.getTime() + '/' + event.values.max.getTime() + '/', function(data) {
                    ht.loadJSON(data);
                    ht.refresh();
                    ht.controller.onComplete();
                    $("#"+$('#article-details').data('node_id')).click();
            });
    });
}
