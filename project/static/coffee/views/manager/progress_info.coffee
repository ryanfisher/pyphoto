class ProgressInfo extends Backbone.View
  className: 'progress-info'

  events:
    'click': 'remove_if_done'

  initialize: (@file) ->
    @bar = $('<div>', class: 'bar animated')
    progress = $('<div>', class: 'progress').append(@bar)
    @$el.append(progress)
    uploading_text = $('#progress-bars').data('uploading-message')
    @message = $('<p>', class: 'message', text: uploading_text + @file.name)
    @$el.prepend(@message)
    $('#progress-bars').prepend(@$el)

  update_bar: (percent_uploaded) ->
    @bar.css('width', "#{percent_uploaded}%")

  display_message: (status) ->
    message = switch status
      when 200 then 'success'
      when 409 then 'error409'
      else 'error'
    display_text = $('#progress-bars').data(message)
    @message.addClass(message).text(display_text + @file.name)

  stop_animation: ->
    @bar.removeClass('animated')

  remove_if_done: ->
    return if @bar.hasClass('animated')
    @remove()
