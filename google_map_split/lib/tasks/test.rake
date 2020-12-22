require 'nokogiri'
require 'open-uri'
namespace :test do
  desc "test Spliting table"
  task test: :environment do
  	facebook_reg ='(?:(?:http|https):\/\/)?(?:www.)?facebook.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[?\w\-]*\/)?(?:profile.php\?id=(?=\d.*))?([\w\-]*)?'
  	linkedin_reg = '^https?://((www|\w\w)\.)?linkedin.com/((in/[^/]+/?)|(pub/[^/]+/((\w|\d)+/?){3}))$'
  	facebook_url = ''
  	linkedin_url = ''
  	Google.find_each do |record|
  		# debugger
  		doc = Nokogiri::HTML(open('http://'+record.url.strip).read)
  		urls = doc.search('a').map{ |tag|
  			case tag.name.downcase 
  			when 'a'
  				tag['href'].to_s
  			end 	}
  		urls.each do |facebook|
  			facebook_url = facebook.match?(facebook_reg) ? facebook : '' 
  			break if facebook_url.present? 
  		end
  		
  		urls.each do |linkedin|
  			linkedin_url = linkedin.match?(linkedin_reg) ? linkedin : ''
  			break if linkedin_url.present? 
  		end

  		puts urls
  		debugger
  	end
  end
end


# facebook=> (?:(?:http|https):\/\/)?(?:www.)?facebook.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[?\w\-]*\/)?(?:profile.php\?id=(?=\d.*))?([\w\-]*)?
# linkedin=> ^https?://((www|\w\w)\.)?linkedin.com/((in/[^/]+/?)|(pub/[^/]+/((\w|\d)+/?){3}))$