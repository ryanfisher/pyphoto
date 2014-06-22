define [], ->
  class PhotoInfo extends Backbone.View
    className: 'info'

    initialize: ->
      @$el.append $('<span>'
        html: "photographer: #{@model.get('username')}"
      )
