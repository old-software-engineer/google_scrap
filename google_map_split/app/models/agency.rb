class Agency < ApplicationRecord
	has_many :agency_categories 
	has_many :agency_locations
end
