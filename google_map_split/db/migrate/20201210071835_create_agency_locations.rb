class CreateAgencyLocations < ActiveRecord::Migration[5.2]
  def change
    create_table :agency_locations do |t|
      t.text :phone
      t.text :email
      t.string :street
      t.string :city
      t.string :state
      t.string :zipcode
      t.string :country
      t.string :agency_category
      t.string :lat
      t.string :lng
      t.text :gmap_reference
      t.integer :gmaps_review_score
      t.float :gmaps_reviews
      t.timestamps
    end
  end
end
