class ApplicationRecord < ActiveRecord::Base
  self.abstract_class = true
  # class << self
  #   private

  #   def timestamp_attributes_for_create
  #     super << 'created'
  #   end

  #   def timestamp_attributes_for_update
  #     super << 'modified'
  #   end
  # end
end
