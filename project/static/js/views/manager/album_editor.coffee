define [], ->
  class AlbumEditor extends Backbone.View
    el: '#album-editor'

    events:
      'submit form': 'save_album'
      'click #new-album': 'open_new_album_form'

    initialize: ->
      @collection.fetch success: => @render()

    render: ->
      @collection.each (album) =>
        @$('.albums').prepend($('<a>', text: album.get('title')))
      @collection.on 'add', (album) =>
        @$('.albums').prepend($('<a>', text: album.get('title')))

    open_new_album_form: ->
      @$('form').toggleClass('hidden')

    save_album: ->
      event.preventDefault()
      input = @$('input[name=title]')
      @$('form').addClass('hidden')
      @collection.create title: input.val()
      input.val('')
