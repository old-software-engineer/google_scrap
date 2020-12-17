# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 2020_12_15_113521) do

  create_table "agencies", options: "ENGINE=InnoDB DEFAULT CHARSET=latin1", force: :cascade do |t|
    t.text "name"
    t.text "logo"
    t.text "url"
    t.text "facebook"
    t.text "linkedin"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "agency_categories", options: "ENGINE=InnoDB DEFAULT CHARSET=latin1", force: :cascade do |t|
    t.string "status"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.bigint "agency_id"
    t.bigint "category_id"
    t.index ["agency_id"], name: "index_agency_categories_on_agency_id"
    t.index ["category_id"], name: "index_agency_categories_on_category_id"
  end

  create_table "agency_locations", options: "ENGINE=InnoDB DEFAULT CHARSET=latin1", force: :cascade do |t|
    t.text "phone"
    t.text "email"
    t.string "street"
    t.string "city"
    t.string "state"
    t.string "zipcode"
    t.string "country"
    t.string "agency_category"
    t.string "lat"
    t.string "lng"
    t.text "gmap_reference"
    t.integer "gmaps_review_score"
    t.float "gmaps_reviews"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.bigint "agency_id"
    t.index ["agency_id"], name: "index_agency_locations_on_agency_id"
  end

  create_table "categories", options: "ENGINE=InnoDB DEFAULT CHARSET=latin1", force: :cascade do |t|
    t.string "name"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "googles", options: "ENGINE=InnoDB DEFAULT CHARSET=latin1", force: :cascade do |t|
    t.text "name"
    t.text "phone_number"
    t.text "email"
    t.text "business_category"
    t.text "maps_reference"
    t.float "review_score"
    t.bigint "number_of_reviews"
    t.text "url"
    t.text "logo"
    t.text "facebook_page"
    t.text "linkedin_page"
    t.text "zip_code"
    t.text "street"
    t.text "city"
    t.text "country"
    t.text "state"
    t.text "latitude"
    t.text "longitude"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

end
