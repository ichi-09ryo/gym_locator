class CreateGymEquipments < ActiveRecord::Migration[7.0]
  def change
    create_table :gym_equipments do |t|
      t.bigint :gym_id, null: false, foreign_key: true
      t.bigint :equipment_id, null: false, foreign_key: true

      t.timestamps
    end

    add_foreign_key :gym_equipments, :gyms
    add_foreign_key :gym_equipments, :equipments
  end
end