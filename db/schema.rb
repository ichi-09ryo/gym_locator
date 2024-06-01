# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# This file is the source Rails uses to define your schema when running `bin/rails
# db:schema:load`. When creating a new database, `bin/rails db:schema:load` tends to
# be faster and is potentially less error prone than running all of your
# migrations from scratch. Old migrations may fail to apply correctly if those
# migrations use external dependencies or application code.
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema[7.0].define(version: 2024_05_30_034552) do
  create_table "equipments", charset: "utf8", force: :cascade do |t|
    t.string "equipment_name", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  create_table "gym_equipments", charset: "utf8", force: :cascade do |t|
    t.bigint "gym_id", null: false
    t.bigint "equipment_id", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
    t.index ["equipment_id"], name: "fk_rails_9b17b277a3"
    t.index ["gym_id"], name: "fk_rails_2417439a57"
  end

  create_table "gyms", charset: "utf8", force: :cascade do |t|
    t.string "gym_name"
    t.string "address"
    t.float "latitude"
    t.float "longitude"
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

  add_foreign_key "gym_equipments", "equipments"
  add_foreign_key "gym_equipments", "gyms"
end
