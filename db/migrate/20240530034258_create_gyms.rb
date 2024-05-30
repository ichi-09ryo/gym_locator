class CreateGyms < ActiveRecord::Migration[7.0]
  def change
    create_table :gyms do |t|
      t.string :gym_name
      t.string :address
      t.float :latitude
      t.float :longitude

      t.timestamps
    end
  end
end
