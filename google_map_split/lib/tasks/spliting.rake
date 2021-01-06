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
      agency=''
  		puts "\n -----record No. #{count} -----\n"
  		count+=1
      if record.url.present? 
        puts "  Contain url  #{record.url}"
  			exists_check = { url: record.url.strip }
  			agency=Agency.find_by(exists_check)
  			
        if agency.present?
          puts "  Agency Already Present "

          location_obj=AgencyLocation.find_by(agency_id: agency.id ,phone: record.phone_number, street: record.street ,city: record.city,
            state: record.state , zipcode: record.zip_code ,country: record.country , agency_category: record.business_category ,gmaps_review_score: record.review_score ,
             gmaps_reviews: record.number_of_reviews)
          if !location_obj.present?
            AgencyLocation.find_or_create_by(agency_id: agency.id ,phone: record.phone_number ,email: record.email , street: record.street ,city: record.city,
            state: record.state , zipcode: record.zip_code ,country: record.country , agency_category: record.business_category , lat: record.latitude ,
            lng: record.longitude , gmap_reference: record.maps_reference , gmaps_review_score: record.review_score , gmaps_reviews: record.number_of_reviews)
            puts "  New AgencyLocation Created "
          end
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
            email = doc.text.downcase.match?(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}/i) ? doc.text.downcase.match(/[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}/i)[0] : ''

    		end
   			create_param = {name: record.name.strip , logo: record.logo , url: record.url.strip ,facebook: facebook_url ,linkedin: linkedin_url}
    		obj =Agency.create(create_param)
        puts "  New Agency Created "
  			AgencyLocation.find_or_create_by(agency_id: obj.id ,phone: record.phone_number , email: email , street: record.street ,city: record.city,
  						state: record.state , zipcode: record.zip_code ,country: record.country , agency_category: record.business_category , lat: record.latitude ,
  						lng: record.longitude , gmap_reference: record.maps_reference , gmaps_review_score: record.review_score , gmaps_reviews: record.number_of_reviews )
        puts "  New AgencyLocation created For New Agency " 			
  			if doc.present? 
  				formatted_response = doc.text.downcase
  				if formatted_response.index('car insurance').present? or formatted_response.index('auto insurance').present?
  					AgencyCategory.find_or_create_by(agency_id: obj.id, category_id: 1,status: 'Active' )
  				end
  				if formatted_response.index('health insurance').present?
  					AgencyCategory.find_or_create_by(agency_id: obj.id , category_id: 2,status: 'Active' )
  				end
  				if formatted_response.index('life insurance').present?
  					AgencyCategory.find_or_create_by(agency_id: obj.id , category_id: 3,status: 'Active' )
  				end
  				if formatted_response.index('home insurance').present? or formatted_response.index('renters insurance').present? or formatted_response.index('property insurance').present?
  					AgencyCategory.find_or_create_by(agency_id: obj.id , category_id: 4,status: 'Active' )
  				end
			  end
  		else
        puts "  Record Not contain url  "
  			exists_check = {name: record.name.strip,url:'' }
  			agency = Agency.find_by(exists_check)
  			if agency.present?
          puts "  Agency Already Present "
          location_obj =AgencyLocation.find_by(agency_id: agency.id ,phone: record.phone_number , street: record.street ,city: record.city,
            state: record.state , zipcode: record.zip_code ,country: record.country , agency_category: record.business_category , gmaps_review_score: record.review_score ,
             gmaps_reviews: record.number_of_reviews)

          if !location_obj.present?
    				AgencyLocation.find_or_create_by(agency_id: agency.id ,phone: record.phone_number ,email: record.email , street: record.street ,city: record.city,
              state: record.state , zipcode: record.zip_code ,country: record.country , agency_category: record.business_category , lat: record.latitude ,
              lng: record.longitude , gmap_reference: record.maps_reference , gmaps_review_score: record.review_score , gmaps_reviews: record.number_of_reviews)
            puts "  New AgencyLocation Created "
          end
          next
        end
        create_param = {name: record.name.strip,logo: record.logo , url: '' ,facebook: '' ,linkedin: ''}
        obj = Agency.find_or_create_by(create_param)
        puts "  New Agency Created "
        AgencyLocation.find_or_create_by(agency_id: obj.id ,phone: record.phone_number ,email: record.email , street: record.street ,city: record.city,
          state: record.state , zipcode: record.zip_code ,country: record.country , agency_category: record.business_category , lat: record.latitude ,
          lng: record.longitude , gmap_reference: record.maps_reference , gmaps_review_score: record.review_score , gmaps_reviews: record.number_of_reviews)
        puts "  New AgencyLocation created For New Agency "
		  end ## main if else 
  	end ## google loop
  end ## Env
end ## Module 
