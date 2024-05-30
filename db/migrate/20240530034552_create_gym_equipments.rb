class CreateGymEquipments < ActiveRecord::Migration[7.0]
  def change
    create_table :gym_equipments do |t|
      t.references :gym, null: false, foreign_key: true
      t.references :equipment, null: false, foreign_key: true

      t.timestamps
    end
  end
end