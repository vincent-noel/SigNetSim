{% load tags %}





function loadReactionGraph () {

  $('#reactions_graph').cytoscape({
    layout: {
      name: 'concentric',
     // padding: 20,
    },

    style: cytoscape.stylesheet()
      .selector('node')
        .css({
          'shape': 'roundrectangle',
          'padding-left': 20,
          'padding-right': 20,
          'padding-bottom': 20,
          'padding-top': 20,
          'content': 'data(name)',
          'text-valign': 'center',
          'text-outline-width': 2,
          'text-outline-color': '#fff',
          'background-color': '#fff',
          'color': '#000'
        })
      .selector(':selected')
        .css({
          'border-width': 3,
          'border-color': '#333'
        })
      .selector('edge')
        .css({
          'curve-style': 'bezier',
          'opacity': 0.666,
          'width': 'mapData(50, 70, 100, 2, 6)',
          'target-arrow-shape': 'tee',
          'source-arrow-shape': 'none',
          'line-color': '#000"',
          'source-arrow-color': '#000',
          'target-arrow-color': '#000'
        })

      .selector('edge.positive')
        .css({
          'target-arrow-shape': 'triangle'
        })

      .selector('edge.negative')
        .css({
          'target-arrow-shape': 'tee'
        })

      .selector('edge.questionable')
        .css({
          'line-style': 'dotted',
          'target-arrow-shape': 'triangle'
        })

      .selector('.faded')
        .css({
          'opacity': 0.25,
          'text-opacity': 0
        }),
 elements: {
      nodes: [
        {% for species in list_of_species %}
          { data: { id: '{{species.getSbmlId}}', name: '{{species.getName}}'} },
        {% endfor %}
        {% for reaction in list_of_reactions %}
          { data: { id: '{{reaction.getSbmlId}}', name: '{{reaction.getName}}'} },
        {% endfor %}
      ],
      edges: [
        {% for reaction in list_of_reactions %}
            {% for reactant in reaction.listOfReactants.values %}

            {
                data: {
                    source: '{{reactant.getSpecies.getSbmlId}}',
                    target: '{{reaction.getSbmlId}}'
                },
                classes: 'positive',

            },
            {% endfor %}
        {% endfor %}

        {% for reaction in list_of_reactions %}
            {% for product in reaction.listOfProducts.values %}

            {
                data: {
                    source: '{{reaction.getSbmlId}}',
                    target: '{{product.getSpecies.getSbmlId}}'
                },
                classes: 'positive',

            },
            {% endfor %}
        {% endfor %}
      ]
    },

  });

}


$(window).on('load',function()
{
  $("#reactions_graph").css({ height: $(window).height() - $(".navbar-header").height() - 150 + "px" });
  loadReactionGraph();
  //alert("Loading reaction graph");
}); // on dom ready




