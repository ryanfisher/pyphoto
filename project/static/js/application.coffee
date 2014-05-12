(->
  _sync = Backbone.sync
  Backbone.sync = (method, model, options) ->
    options.beforeSend = (xhr) ->
      token = $('meta[name="csrf-token"]').attr("content")
      xhr.setRequestHeader "X-CSRFToken", token
      return
    _sync method, model, options
)()

define [
  'cs!collections/user_photos'
  'cs!views/photo_manager'
  'cs!views/photo_feed'
], (UserPhotos, PhotoManager, PhotoFeed) ->

  class App extends Backbone.View

    initialize: ->
      collection = new UserPhotos
      new PhotoFeed({collection}) if $('#photo-feed').length
      new PhotoManager({collection}) if $('#photo-manager').length
      collection.fetch()

  jQuery('document').ready ->
    App = new App()
