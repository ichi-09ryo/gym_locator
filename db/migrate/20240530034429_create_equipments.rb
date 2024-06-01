class CreateEquipments < ActiveRecord::Migration[7.0]
  def change
    create_table :equipments do |t|
      t.string :equipment_name, null: false

      t.timestamps
    end
  end
end