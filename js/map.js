$('body').tooltip({selector: '[title],[data-title],[data-original-title]', container: 'body', html: true, animated: 'fade'})

    var w = 600;
    var h = 600;
    var proj = d3.geo.mercator()
    .scale(6700)
    .translate([-1220, 750]);

    var path = d3.geo.path().projection(proj);

    var rateById = d3.map();

    var svg = d3.select("#chart")
    .append("svg")
    .attr("width", w)
    .attr("height", h)

    var map = svg.append("g").attr("class", "states")

    var colorRamp = ['#ffbf80','#e67300'];

    $(document).ready(function(){
      $.ajax({
        type: 'GET',
        url: '/data',
        beforeSend: function(){
          $('.loader').show()
        },
      })
      .done(function(data){

        _.each(data['response'], function(d){ rateById.set(d.State, +d.Aadhaar_Count)});
        max = _.max(_.map(data['response'], function(d){ return parseInt(d.Aadhaar_Count); }))

        var color = d3.scaleLinear()
        .domain([0, max])
        .range(colorRamp);

        // var table_data = _.map(data['response'], function(d){ return [d.State, d.Population, d.Aadhaar_Count] });

        // $("#aadhaar_table").DataTable({
        //   data: table_data,
        //   // bPaginate: false,
        //   bInfo: false,
        //   pageLength: 13,
        //   lengthChange: false,
        //   columns: [
        //     {title: "STATE NAME"},
        //     {title: "POPULATION"},
        //     {title: "UIDIA COUNT"},
        //   ],
        //   order: false,
        // })

      d3.json("data/india.json", function(json){
        map.selectAll("path")
        .data(topojson.feature(json, json.objects.polygons).features)
        .enter().append("path")
        .on('click', function(d){ insights(d.properties.st_nm) })
        .attr("d", path)
        .transition().duration(1000)
        .style("fill", function(d) { return color(rateById.get(d.properties.st_nm))})
        .attr('data-placement', 'right')
        .attr('data-toggle', 'popover')
        .attr('data-title', function(d){
          return d.properties.st_nm.toUpperCase() + ' : '+ rateById.get(d.properties.st_nm)
        })

        svg.append("path")
          .attr("class", "state-borders")
          .attr("d", path(topojson.mesh(json, json.objects.polygons, function(a, b) { return a !== b; })));
      });

      $('.loader').hide();
      $('.card1').show();
      })
      .fail(function(error){
        console.log(error);
      })

      function insights(state){
        $.ajax({
          type: 'GET',
          url:  '/insight?state='+state,
        })
        .done(function(res){
          console.log(res.response)
          var insight_tmplt = _.template($("#insight-script").html());
          var insight_html = insight_tmplt({ data: res.response, state: state });
          $("#insights").html(insight_html);
        })
        .fail(function(error){
          console.log(error);
        });
      }
    });

    // d3.queue()
    //   .defer(d3.json, "data/india.json")
    //   // .defer(d3.csv, "data/aadhaar_data.csv")
    //   // .defer(d3.request, "/data")
    //   .await(ready);
