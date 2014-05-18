define [], ->
  class PhotoEditView extends Backbone.View
    className: 'photo hidden'

    attributes:
      'draggable': true

    events:
      'click': 'toggle_selected'

    initialize: ->
      console.log @model
      img_url = @model.get('thumbnail_url')
      # Load image before showing it in view
      $('<img>', src: img_url).on 'load', => @$el.removeClass('hidden')
      thumbnail_url = "url(#{img_url})".replace /\s/, "%20"
      @$el.css('background-image', thumbnail_url)

    # Checks if photo is selected
    #
    # @return [Boolean]
    is_selected: ->
      @$el.is(':visible') and @$el.hasClass('selected')

    toggle_selected: ->
      @$el.toggleClass('selected')
      @trigger 'selected_toggle'

    delete_photo: ->
      @model.destroy()
      @remove()
