class PhotoInfo extends Backbone.View
  className: 'info'

  events:
    'click a': 'goto_profile_page'

  initialize: ->
    @$el.append $('<span>'
      html: "photographer: <a>#{@model.get('username')}</a>"
    )

  goto_profile_page: (event) ->
    event.stopPropagation()
    window.location = "/profile/#{@model.get('username')}"
