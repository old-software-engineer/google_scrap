require 'nokogiri'
require 'open-uri'
namespace :spliting do
  desc "Spliting table"
  task spliting: :environment do
  	count=1
    facebook_reg ='(?:(?:http|https):\/\/)?(?:www.)?facebook.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[?\w\-]*\/)?(?:profile.php\?id=(?=\d.*))?([\w\-]*)?'
    linkedin_reg = '^https?://((www|\w\w)\.)?linkedin.com/((in/[^/]+/?)|(pub/[^/]+/((\w|\d)+/?){3}))$'
    facebook_url = ''
    linkedin_url = ''
    Google.find_each do |record|
  		puts "record No. #{count}"
  		count+=1
  		if record.url.present? 
        puts "  record contain url  "
  			exists_check = {name: record.name,logo: record.logo , url: record.url.strip }
  			agency=Agency.find_by(exists_check)
        
  			if agency.present?
          puts "Agency Already Present "
  				AgencyLocation.find_or_create_by(agency_id: agency.id ,phone: record.phone_number ,email: record.email , street: record.street ,city: record.city,
						state: record.state , zipcode: record.zip_code ,country: record.country , agency_category: record.business_category , lat: record.latitude ,
						lng: record.longitude , gmap_reference: record.maps_reference , gmaps_review_score: record.review_score , gmaps_reviews: record.number_of_reviews)
          next
  			end

  			begin
  				doc = Nokogiri::HTML(open('http://'+record.url.strip).read)
          puts " Nokogiri Done"
  			rescue  Exception => e
  				puts e.message
  				doc = ''
  			end
			
  			if doc.present?
  				urls = doc.search('a').map{ |tag| case tag.name.downcase 
    					when 'a'
  						tag['href'].to_s
    					end }

    				urls.each do |facebook|
    					facebook_url = facebook.match?(facebook_reg) ? facebook : '' 
    					break if facebook_url.present? 
    				end
    		
    				urls.each do |linkedin|
    					linkedin_url = linkedin.match?(linkedin_reg) ? linkedin : ''
    					break if linkedin_url.present? 
    				end
    		end
   			create_param = {name: record.name,logo: record.logo , url: record.url.strip ,facebook: facebook_url ,linkedin: linkedin_url}
    		obj =Agency.create(create_param)
        puts "New Agency Created"
  			AgencyLocation.create(agency_id: obj.id ,phone: record.phone_number ,email: record.email , street: record.street ,city: record.city,
  						state: record.state , zipcode: record.zip_code ,country: record.country , agency_category: record.business_category , lat: record.latitude ,
  						lng: record.longitude , gmap_reference: record.maps_reference , gmaps_review_score: record.review_score , gmaps_reviews: record.number_of_reviews )
        puts "New Agency AgencyLocation created" 			
  			if doc.present? 
  				formatted_response = doc.text.downcase
  				if formatted_response.index('car insurance').present?
  					AgencyCategory.create(agency_id: obj.id, category_id: 1,status: 'Active' )
  				end
  				if formatted_response.index('health insurance').present?
  					AgencyCategory.create(agency_id: obj.id , category_id: 2,status: 'Active' )
  				end
  				if formatted_response.index('life insurance').present?
  					AgencyCategory.create(agency_id: obj.id , category_id: 3,status: 'Active' )
  				end
  				if formatted_response.index('home insurance').present?
  					AgencyCategory.create(agency_id: obj.id , category_id: 4,status: 'Active' )
  				end
			  end
  		else
        puts "record Not contain url  "
  			exists_check = {name: record.name , logo: record.logo }
  			agency = Agency.find_by(exists_check)
  			if agency.present?
          puts "Agency Already Present "
  				AgencyLocation.find_or_create_by(agency_id: agency.id ,phone: record.phone_number ,email: record.email , street: record.street ,city: record.city,
            state: record.state , zipcode: record.zip_code ,country: record.country , agency_category: record.business_category , lat: record.latitude ,
            lng: record.longitude , gmap_reference: record.maps_reference , gmaps_review_score: record.review_score , gmaps_reviews: record.number_of_reviews)
          next
        end
        create_param = {name: record.name,logo: record.logo , url: '' ,facebook: '' ,linkedin: ''}
        agency = Agency.create(create_param)
        puts "New Agency Created"
        AgencyLocation.create(agency_id: agency.id ,phone: record.phone_number ,email: record.email , street: record.street ,city: record.city,
          state: record.state , zipcode: record.zip_code ,country: record.country , agency_category: record.business_category , lat: record.latitude ,
          lng: record.longitude , gmap_reference: record.maps_reference , gmaps_review_score: record.review_score , gmaps_reviews: record.number_of_reviews)
		  end ## main if else 
  	end ## google loop
  end ## Env
end ## Module 
