define ['cs!views/manager/photo_edit_view'], (PhotoManagerEditView) ->
  class PhotoManagerFeed extends Backbone.View
    el: '#photo-manager-feed'

    initialize: ->
      @photo_edit_views = []
      @collection.on 'add', (model) =>
        photo_edit_view = new PhotoManagerEditView({model})
        @photo_edit_views.push photo_edit_view
        @$('.feed').append(photo_edit_view.$el)
      @collection.once 'sync', =>
        @collection.off 'add'
        @collection.on 'add', (model) =>
          photo_edit_view = new PhotoManagerEditView({model})
          @photo_edit_views.push photo_edit_view
          @$('.feed').prepend(photo_edit_view.$el)

    delete_selected_photos: ->
      to_delete = _.filter @photo_edit_views, (view) -> view.is_selected()
      delete_count = to_delete.length
      return if delete_count == 0
      confirm_text = "Are you sure you want to delete the selected photo(s)?" +
                     "\n\n#{delete_count} selected"
      if window.confirm(confirm_text)
        _.each to_delete, (view) -> view.delete_photo()
