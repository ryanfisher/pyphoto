class PhotoEditor extends Backbone.View
  el: '#photo-editor'

  events:
    'click .close-button': 'close_editor'
    'click .save-photo': 'save_photo'

  initialize: ->
    @reset_editor()
    img = @$('img')
    img.prop('src', @model.get('optimized_url'))
    img.on 'load', -> img.removeClass('hidden')
    @$('input[name="public-tags"]').val(@model.get('public_tags'))
    @$el.addClass('open')

  reset_editor: ->
    @$('img').prop('src', '').addClass('hidden')
    @$('input').val('')

  close_editor: ->
    @$el.removeClass('open')
    @$el.removeData().unbind()
    @undelegateEvents()

  save_photo: ->
    public_tags = @$('input[name="public-tags"]').val().split(',')
    @model.save {public_tags: public_tags}, success: ->
      Notification.show('Photo saved successfully!')
