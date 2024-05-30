class CreateEquipment < ActiveRecord::Migration[7.0]
  def change
    create_table :equipment do |t|
      t.string :machine_name, null: false

      t.timestamps
    end
  end
end
