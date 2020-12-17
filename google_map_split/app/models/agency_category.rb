class AgencyCategory < ApplicationRecord
	belongs_to :agencies
	belongs_to :categories
end
