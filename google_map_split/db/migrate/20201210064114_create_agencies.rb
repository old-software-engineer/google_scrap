class CreateAgencies < ActiveRecord::Migration[5.2]
  def change
    create_table :agencies do |t|
      t.text :name
      t.text :logo
      t.text :url
      t.text :facebook
      t.text :linkedin
      t.timestamps
    end
  end
end
