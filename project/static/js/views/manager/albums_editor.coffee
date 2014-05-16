define [], ->
  class AlbumsEditor extends Backbone.View
    el: '#album-editor'

    events:
      'submit form': 'save_album'
      'click #new-album': 'open_new_album_form'

    initialize: ->
      @collection.fetch success: => @render()

    render: ->
      @collection.each (album) => @add_album(album)
      @collection.on 'add', (album) => @add_album(album)

    add_album: (album) ->
      title = $('<a>', text: album.get('title'))
      title.on 'click', => @edit_album(album)
      @$('.albums').prepend(title)

    edit_album: (album) ->
      console.log "edit album #{album.get('title')}"

    open_new_album_form: ->
      @$('form').toggleClass('hidden')

    save_album: ->
      event.preventDefault()
      input = @$('input[name=title]')
      @$('form').addClass('hidden')
      @collection.create title: input.val()
      input.val('')
