require "test_helper"

class PagesControllerTest < ActionDispatch::IntegrationTest
  test "should get about" do
    get pages_about_url
    assert_response :success
  end

  test "should get gym_activity" do
    get pages_gym_activity_url
    assert_response :success
  end

  test "should get magazine" do
    get pages_magazine_url
    assert_response :success
  end
end
