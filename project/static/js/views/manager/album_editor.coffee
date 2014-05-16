define [], ->
  class AlbumEditor extends Backbone.View
    el: '#album-editor'

    events:
      'click': 'close_editor'

    initialize: ->
      @$('.title').text @model.get('title')
      @$('.photos').text @model.get('photos')
      @$el.addClass('open')

    close_editor: ->
      @$el.removeClass('open')
