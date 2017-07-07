{% load tags %}





function loadReactionGraph () {
  var cy = window.cy = cytoscape({
    container: document.getElementById('reactions_graph'),
    layout: {
        name: 'cose-bilkent',
        idealEdgeLength: 100,
        nodeOverlap: 20
    },

    style: cytoscape.stylesheet()
      .selector('node')
        .css({
          'padding-left': 10,
          'padding-right': 10,
          'padding-bottom': 10,
          'padding-top': 10,
          'color': '#000',
          'border-width': 2,
          'border-color': '#000',
          'background-color': '#fff'

        })
      .selector(':selected')
        .css({
          'border-width': 3,
          'border-color': '#333'
        })
      .selector('node.reaction')
        .css({
            'shape': 'rectangle',
            'width': '5',
            'height': '5'
        })

      .selector('node.species')
        .css({
            'shape': 'roundrectangle',
            'content': 'data(name)',
            'text-valign': 'center',
            'text-outline-width': 2,
            'text-outline-color': '#fff',
            'width': 'label',
            'height': 'label'
        })
      .selector('edge')
        .css({
          'curve-style': 'bezier',
          'opacity': 0.666,
          'width': 'mapData(50, 70, 100, 2, 6)',
          'target-arrow-shape': 'tee',
          'source-arrow-shape': 'none',
          'line-color': '#000',
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
      .selector('edge.regulation')
        .css({
          'target-arrow-shape': 'circle'
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
          { data: { id: '{{species.getSbmlId}}', name: '{{species.getNameOrSbmlId}}'}, classes: 'species' },
        {% endfor %}
        {% for reaction in list_of_reactions %}
          { data: { id: '{{reaction.getSbmlId}}', name: '{{reaction.getNameOrSbmlId}}'}, classes: 'reaction' },
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
            {% for modifier in reaction.listOfModifiers.values %}

            {
                data: {
                    source: '{{modifier.getSpecies.getSbmlId}}',
                    target: '{{reaction.getSbmlId}}'
                },
                classes: 'regulation',

            },
            {% endfor %}
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




