class PhotoImage extends Backbone.View
  tagName: 'img'
  className: 'hidden'

  initialize: ->
    @$el.on 'load', => @$el.removeClass('hidden')
    @$el.attr('src', @model.get('thumbnail_url'))
