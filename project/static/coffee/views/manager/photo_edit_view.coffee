class PhotoEditView extends Backbone.View
  className: 'photo hidden'

  events:
    'click': 'toggle_selected'
    'click .edit': 'open_photo_editor'

  initialize: ->
    img_url = @model.get('thumbnail_url')
    # Load image before showing it in view
    $('<img>', src: img_url).on 'load', => @$el.removeClass('hidden')
    thumbnail_url = "url(#{img_url})".replace /\s/, "%20"
    @$el.css('background-image', thumbnail_url)
    @$el.append($('<div>', class: 'edit', text: 'edit'))
    @model.on 'destroy', => @remove()

  # Checks if photo is selected
  #
  # @return [Boolean]
  is_selected: ->
    @$el.is(':visible') and @$el.hasClass('selected')

  toggle_selected: (event) ->
    # Don't fire click event on photo manager feed
    event.stopPropagation()
    @$el.toggleClass('selected')
    @trigger 'selected_toggle'

  open_photo_editor: (event) ->
    event.stopPropagation()
    new PhotoEditor({@model})
