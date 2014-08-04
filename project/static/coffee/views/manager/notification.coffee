class Notification extends Backbone.View
  el: '#notification'

  events: 'click': 'hide_notification'

  default_delay: 3000 # in milliseconds

  @show: (text) -> (new Notification).show(text)

  show: (text) ->
    @$el.text(text).addClass('open')
    setTimeout (=> @hide_notification()), @default_delay

  hide_notification: ->
    @$el.removeClass('open')
    # make instance available for garbage collection
    @$el.removeData().unbind()
