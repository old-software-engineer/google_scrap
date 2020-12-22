class CreateZipcodes < ActiveRecord::Migration[5.2]
  def change
    create_table :zipcodes do |t|
    	t.string :zipcode ,   null: false
    	t.string :type,   null: false
    	t.string :city,   null: false
    	t.string :state,   null: false
    	t.string :county,   null: false
    	t.string :lat,   null: true
    	t.string :lng,   null: true
      	t.timestamps
    end
  end
end
