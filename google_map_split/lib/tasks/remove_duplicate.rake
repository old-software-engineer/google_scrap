namespace :remove_dup do
  desc "Remove_dup  From AWS DB ------"
  task update_db: :environment do
  	url_array=[]
  	count = 0
  	Agency.where("url != ''").group_by(&:url).each {|url,id|  puts"#{url} --> #{id.map(&:id)}"; url_array << url if id.count > 1}
  	puts "Total urls count #{url_array.count}"
  	url_array.each do |urls|
  		count=count+1
  		puts " count -->  #{count}"
  		ids=Agency.where(url: urls).ids
  		AgencyLocation.where(agency_id: ids).update_all(agency_id: ids[0])
  		ids.shift
  		Agency.where(id: ids).delete_all
  		AgencyCategory.where(agency_id: ids).delete_all
  	end
  end
end