define [], ->
  class AlbumEditor extends Backbone.View
    el: '#album-editor'

    events:
      'submit form': 'save_album'

    initialize: ->
      @collection.fetch success: => @render()

    render: ->
      @collection.each (album) =>
        @$('.albums').prepend($('<a>', text: album.get('title')))
      @collection.on 'add', (album) =>
        @$('.albums').prepend($('<a>', text: album.get('title')))

    save_album: ->
      event.preventDefault()
      input = @$('input[name=title]')
      @$('form').addClass('hidden')
      @collection.create title: input.val()
      input.val('')
