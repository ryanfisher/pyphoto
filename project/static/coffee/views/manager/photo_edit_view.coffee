class PhotoEditView extends Backbone.View
  className: 'photo hidden'

  events:
    'click': 'toggle_selected'
    'click .edit': 'open_photo_editor'
    # 'mouseenter': 'expand_size'
    # 'mouseleave': 'restore_size'

  initialize: ->
    img_url = @model.get('thumbnail_url')
    # Load image before showing it in view
    $('<img>', src: img_url).on 'load', => @$el.removeClass('hidden')
    thumbnail_url = "url(#{img_url})".replace /\s/, "%20"
    @$el.css('background-image', thumbnail_url)
    @$el.append($('<div>', class: 'edit', text: 'edit'))

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

  expand_size: ->
    top = @$el.position().top
    left = @$el.position().left
    far_right = left + @model.get('width')
    @$el.css('position', 'absolute')
    @placeholder = $('<div>', class: 'photo')
    @placeholder.insertAfter @$el
    if far_right > @$el.parent().width()
      @$el.css('right', 10)
    else
      @$el.css('left', left)
    @$el.css('top', top)
    @$el.css('z-index', 2)
    width = _.min([@model.get('width'), @$el.parent().width() - 40])
    height = @model.height_from(width)
    @$el.width(width)
    @$el.height(height)

  restore_size: ->
    @placeholder.remove()
    @$el.css('z-index', '')
    @$el.height('')
    @$el.width('')
    @$el.css('position', '')

  delete_photo: ->
    @model.destroy()
    @remove()
