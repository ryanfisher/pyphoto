class UserPhotos extends Backbone.Collection
  url: '/api/photos'
  model: UserPhoto

  initialize: ->
    @sort_key = 'id'

  sort_by: (type) ->
    @sort_key = switch type
      when 'upload-date' then 'id' # TODO get upload date into model
      when 'date-taken' then 'taken'
    @sort()

  comparator: (model1, model2) ->
    @value1 = model1.get(@sort_key)
    @value2 = model2.get(@sort_key)
    if @value1 > @value2 then 1 else -1
