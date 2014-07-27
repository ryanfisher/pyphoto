class PhotoPage extends Backbone.View
  el: '.photo-container'

  initialize: ->
    image = $('<img>', src: @model.get('optimized_url'), class: 'hidden')
    image.on 'load', => image.removeClass('hidden')
    @$el.prepend(image)
    window_height = $(window).height()
    content_width = $('#content').width()
    width = @model.width_from(window_height)
    width = content_width if width > content_width
    @$('img').width(width)
