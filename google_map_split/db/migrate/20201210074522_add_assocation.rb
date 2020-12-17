class AddAssocation < ActiveRecord::Migration[5.2]
  def change
  	add_reference :agency_locations, :agency
  	add_reference :agency_categories, :agency
  	add_reference :agency_categories, :category
  end
end
